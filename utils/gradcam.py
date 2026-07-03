from __future__ import annotations

import io
import traceback

import numpy as np
import cv2
import tensorflow as tf
from PIL import Image


# ─────────────────────── ERROR TYPE ───────────────────────────
class GradCAMError(Exception):
    """
    Raised when Grad-CAM cannot be computed by any strategy.
    `trace` holds the concatenated tracebacks of every attempt made,
    so the calling UI can display the real failure reason instead of
    a generic message.
    """
    def __init__(self, message: str, trace: str = ""):
        super().__init__(message)
        self.trace = trace


# ─────────────────────── LAYER DETECTION ─────────────────────
def _is_conv2d(layer) -> bool:
    """
    Version-tolerant Conv2D check.

    Prefers isinstance, but falls back to matching the class name.
    This matters because a model trained with one Keras/TF version
    and reloaded on a host with a *different* installed version
    (very common on Streamlit Cloud, where the deployed
    tensorflow==X.Y.Z may differ from whatever was used to train
    and export the .h5/.keras file) can end up with layer objects
    whose isinstance check against tf.keras.layers.Conv2D silently
    fails even though the layer is functionally a Conv2D.
    """
    if isinstance(layer, tf.keras.layers.Conv2D):
        return True
    return type(layer).__name__ == "Conv2D"


def _iter_conv_candidates(model, _owner=None, _depth=0, _max_depth=8):
    """
    Recursively walk `model` and yield (owner, conv_layer) for every
    Conv2D-like layer found at ANY nesting depth — not just one level.

    A plain EfficientNet/MobileNet/ResNet backbone wrapped as a single
    layer is one level of nesting, but some architectures (e.g. a
    backbone wrapped inside a custom feature-extractor layer, or a
    model reloaded from SavedModel format) can be nested two or more
    levels deep. The previous version of this function only checked
    one level down, which is why "Could not locate a Conv2D layer"
    was being raised even though the model clearly has Conv2D layers
    somewhere inside it.

    `owner` in the yielded tuple is always the *immediate* Keras
    layer/model that directly contains the Conv2D (used later to
    look up its index for Strategy B).
    """
    owner = _owner if _owner is not None else model
    layers = getattr(model, "layers", None) or []
    for layer in layers:
        if _is_conv2d(layer):
            yield owner, layer
        sub_layers = getattr(layer, "layers", None)
        if sub_layers and _depth < _max_depth:
            yield from _iter_conv_candidates(layer, _owner=layer, _depth=_depth + 1)


def _find_layer_by_name(model, name, _depth=0, _max_depth=8):
    """
    Recursively find a layer by name anywhere inside `model`,
    including inside nested submodels. Unlike `model.get_layer(name)`
    (which only searches the top-level layer list), this will find a
    layer buried inside a backbone at any depth.
    """
    for layer in getattr(model, "layers", None) or []:
        if layer.name == name:
            return layer
        sub_layers = getattr(layer, "layers", None)
        if sub_layers and _depth < _max_depth:
            found = _find_layer_by_name(layer, name, _depth=_depth + 1, _max_depth=_max_depth)
            if found is not None:
                return found
    return None


def _find_last_conv_layer(model) -> str:
    """Kept for backward compatibility with any external callers."""
    _, name, _ = _locate_last_conv_layer(model)
    return name


def _locate_last_conv_layer(model):
    """
    Find the last (deepest-in-forward-order) Conv2D layer anywhere in
    `model`, including inside nested submodels at any depth.

    Returns
    -------
    (owner, layer_name, owner_index)
        owner       : the Keras Model/Layer that directly *contains*
                       the Conv2D layer. Equal to `model` itself if
                       the conv layer isn't nested.
        layer_name  : name of the Conv2D layer.
        owner_index : index of `owner` inside `model.layers` (top
                       level only), or `None` if `owner is model` or
                       if `owner` is nested more than one level deep
                       (in which case Strategy B is skipped and we
                       rely on Strategy A, which now works at any
                       depth via direct tensor connection).
    """
    candidates = list(_iter_conv_candidates(model))
    if not candidates:
        raise ValueError("No Conv2D layer found in model (including nested submodels).")

    owner, layer = candidates[-1]

    if owner is model:
        return model, layer.name, None

    try:
        owner_index = model.layers.index(owner)
    except ValueError:
        owner_index = None  # owner is nested more than one level deep

    return owner, layer.name, owner_index


# ─────────────────────── GRAD-CAM STRATEGIES ──────────────────
def _gradcam_direct(model, img_array, class_index, layer_name):
    """
    Strategy A — build the grad model by connecting the target conv
    layer's output tensor directly to `model.inputs`.

    This works regardless of nesting depth as long as the backbone
    was invoked functionally when the outer model was built (i.e.
    `base_model(some_input_tensor)`), because the Keras functional
    API tracks the *entire* computation graph, including tensors
    produced deep inside nested sub-models. The previous version of
    this function used `model.get_layer(layer_name)`, which only
    searches the *top-level* layer list and raises immediately for
    any nested layer — that was the real reason nested backbones
    were falling through to Strategy B (or failing entirely).
    """
    target_layer = _find_layer_by_name(model, layer_name)
    if target_layer is None:
        raise ValueError(f"Layer '{layer_name}' not found in model (including nested submodels).")

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[target_layer.output, model.output],
    )
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array, training=False)
        loss = predictions[:, class_index]
    grads = tape.gradient(loss, conv_outputs)
    return conv_outputs, grads


def _gradcam_nested_two_stage(model, img_array, class_index, owner, layer_name, owner_index):
    """
    Strategy B — fallback for the rare case where the target Conv2D
    layer lives inside a submodel that is NOT part of the same
    functional graph as `model.inputs` (e.g. built with Sequential
    rather than Functional API, so tensor identity is lost). Rebuilds
    the forward pass explicitly as two connected stages:

        1. feature_extractor : raw image  -> conv activations
        2. classifier_model  : activations -> final prediction
                                (replays every layer that originally
                                came AFTER the backbone in `model`)

    Only usable when `owner_index` is known, i.e. the backbone is
    exactly one level deep. Deeper nesting relies on Strategy A.
    """
    if owner_index is None:
        raise ValueError(
            "owner_index unknown (backbone nested more than one level deep); "
            "Strategy B requires a top-level backbone layer."
        )

    feature_extractor = tf.keras.models.Model(
        inputs=owner.input,
        outputs=owner.get_layer(layer_name).output,
    )

    remaining_layers = model.layers[owner_index + 1:]
    if not remaining_layers:
        raise ValueError("No layers found after the backbone to rebuild the classifier head.")

    conv_shape = feature_extractor.output_shape[1:]
    classifier_input = tf.keras.Input(shape=conv_shape)
    x = classifier_input
    for layer in remaining_layers:
        x = layer(x)
    classifier_model = tf.keras.models.Model(classifier_input, x)

    with tf.GradientTape() as tape:
        conv_outputs = feature_extractor(img_array, training=False)
        tape.watch(conv_outputs)
        predictions = classifier_model(conv_outputs, training=False)
        loss = predictions[:, class_index]
    grads = tape.gradient(loss, conv_outputs)
    return conv_outputs, grads


# ─────────────────────── GRAD-CAM CORE ───────────────────────
def compute_gradcam(
    model,
    img_array: np.ndarray,
    class_index: int,
    layer_name: str | None = None,
) -> np.ndarray:
    """
    Compute Grad-CAM heatmap for a given class index.

    Tries multiple construction strategies so the result is robust
    across TensorFlow/Keras versions and works whether the target
    conv layer is nested (e.g. an EfficientNet backbone) or not, and
    regardless of nesting depth. Drop-in replacement — same
    signature, same return type as before.

    Parameters
    ----------
    model       : loaded Keras model
    img_array   : preprocessed image (1, H, W, 3) float32
    class_index : predicted class index
    layer_name  : optional — pin a specific target conv layer name.
                  Left as None (recommended) to auto-detect.

    Returns
    -------
    heatmap : np.ndarray (H, W) normalised 0-1

    Raises
    ------
    GradCAMError — if every strategy fails. `err.trace` contains the
    full tracebacks of every attempt, for debugging.
    """
    attempts_trace = []

    # 1. Locate the layer (and, if nested exactly one level, its owner).
    try:
        if layer_name is not None:
            owner, found_name, owner_index = model, layer_name, None
            try:
                _, _, real_owner_index = _locate_last_conv_layer(model)
                if real_owner_index is not None:
                    owner_index = real_owner_index
                    owner = model.layers[real_owner_index]
            except Exception:
                pass
        else:
            owner, found_name, owner_index = _locate_last_conv_layer(model)
    except Exception:
        raise GradCAMError(
            "Could not locate a Conv2D layer in the model.",
            trace=traceback.format_exc(),
        )

    # 2. Strategy A: direct tensor connection (now works at any depth)
    try:
        conv_outputs, grads = _gradcam_direct(model, img_array, class_index, found_name)
        return _finalize_heatmap(conv_outputs, grads)
    except Exception:
        attempts_trace.append("Strategy A (direct layer access) failed:\n" + traceback.format_exc())

    # 3. Strategy B: nested two-stage rebuild (only if backbone is one level deep)
    try:
        conv_outputs, grads = _gradcam_nested_two_stage(
            model, img_array, class_index, owner, found_name, owner_index
        )
        return _finalize_heatmap(conv_outputs, grads)
    except Exception:
        attempts_trace.append("Strategy B (nested two-stage rebuild) failed:\n" + traceback.format_exc())

    # 4. All strategies failed
    raise GradCAMError(
        "Grad-CAM could not be computed with any available strategy.",
        trace="\n\n".join(attempts_trace),
    )


def _finalize_heatmap(conv_outputs, grads) -> np.ndarray:
    if grads is None:
        raise GradCAMError(
            "Gradient computation returned None — the conv output and "
            "model output are disconnected in the graph."
        )

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # ReLU + normalise
    heatmap = tf.nn.relu(heatmap).numpy()
    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()

    return heatmap.astype(np.float32)


# ─────────────────────── OVERLAY ─────────────────────────────
def overlay_heatmap(
    original_image: Image.Image,
    heatmap: np.ndarray,
    alpha: float = 0.45,
    colormap: int = cv2.COLORMAP_JET,
) -> Image.Image:
    """
    Overlay a Grad-CAM heatmap onto the original PIL image.

    Returns
    -------
    PIL Image with the coloured heatmap blended onto the original.
    """
    orig_w, orig_h = original_image.size
    orig_rgb = np.array(original_image.convert("RGB"))

    # Resize heatmap to match original image
    heatmap_resized = cv2.resize(heatmap, (orig_w, orig_h))

    # Convert heatmap to uint8 colour map
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, colormap)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)

    # Blend
    overlay = cv2.addWeighted(orig_rgb, 1 - alpha, heatmap_colored, alpha, 0)

    return Image.fromarray(overlay)


# ─────────────────────── CONVENIENCE ─────────────────────────
def generate_gradcam(
    model,
    pil_image: Image.Image,
    class_index: int,
) -> tuple[Image.Image, Image.Image]:
    """
    Full pipeline: preprocess → Grad-CAM → overlay.

    Returns
    -------
    (original_image, overlaid_image) — both as PIL Images (224×224)

    Raises
    ------
    GradCAMError — propagated from `compute_gradcam` if every strategy
    fails, so the caller (app.py) can show the real diagnostic instead
    of a generic message.
    """
    from utils.predict import preprocess  # avoid circular import

    img_array = preprocess(pil_image)

    heatmap = compute_gradcam(model, img_array, class_index)
    resized = pil_image.resize((224, 224), Image.LANCZOS)
    overlaid = overlay_heatmap(resized, heatmap)

    return resized, overlaid


def pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert a PIL Image to raw bytes for Streamlit download."""
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()
