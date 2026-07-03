```python
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
def _find_last_conv_layer(model) -> str:
    """
    Walk layers in reverse and return the name of the first Conv2D
    layer found. Kept for backward compatibility with any external
    callers — internally this now just delegates to
    `_locate_last_conv_layer`, which also tracks the owning submodel
    (needed for nested EfficientNet backbones).
    """
    _, name, _ = _locate_last_conv_layer(model)
    return name


def _locate_last_conv_layer(model):
    """
    Recursively search `model` (and any nested Keras model/layer, e.g.
    an EfficientNetB0 backbone wrapped as a single layer) for the last
    Conv2D layer.

    Returns
    -------
    (owner, layer_name, owner_index)
        owner       : the Keras Model/Layer that directly *contains*
                       the Conv2D layer. Equal to `model` itself if
                       the conv layer isn't nested; otherwise the
                       nested submodel (e.g. the EfficientNetB0
                       backbone object).
        layer_name  : name of the Conv2D layer.
        owner_index : index of `owner` inside `model.layers`, or
                       `None` if `owner is model` (not nested). Used
                       to know which layers come *after* the backbone
                       for two-stage reconstruction.
    """
    for rev_idx, layer in enumerate(reversed(model.layers)):
        real_idx = len(model.layers) - 1 - rev_idx
        if isinstance(layer, tf.keras.layers.Conv2D):
            return model, layer.name, None
        sub_layers = getattr(layer, "layers", None)
        if sub_layers:
            for sub in reversed(sub_layers):
                if isinstance(sub, tf.keras.layers.Conv2D):
                    return layer, sub.name, real_idx
    raise ValueError("No Conv2D layer found in model (including nested submodels).")


# ─────────────────────── GRAD-CAM STRATEGIES ──────────────────
def _gradcam_direct(model, img_array, class_index, layer_name):
    """
    Strategy A — target Conv2D layer sits directly in `model.layers`
    (no nesting). Every tensor belongs to the same functional graph,
    so this simple reconstruction is safe across TF/Keras versions.
    """
    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[model.get_layer(layer_name).output, model.output],
    )
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array, training=False)
        loss = predictions[:, class_index]
    grads = tape.gradient(loss, conv_outputs)
    return conv_outputs, grads


def _gradcam_nested_two_stage(model, img_array, class_index, owner, layer_name, owner_index):
    """
    Strategy B — target Conv2D layer lives inside a nested submodel
    (e.g. EfficientNetB0 used as a single "layer" inside your outer
    model). Rebuilds the forward pass explicitly as two connected
    stages so no tensor is borrowed from a foreign call context:

        1. feature_extractor : raw image  -> conv activations
        2. classifier_model  : activations -> final prediction
                                (replays every layer that originally
                                came AFTER the backbone in `model`,
                                e.g. GAP -> BN -> Dense -> Dropout ->
                                Dense -> Softmax)
    """
    # Build feature extractor
    feature_extractor = tf.keras.models.Model(
        inputs=owner.input,
        outputs=owner.get_layer(layer_name).output,
    )

    # Build classifier head with remaining layers
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
    conv layer is nested (EfficientNet backbone) or not. This is a
    drop-in replacement — same signature, same return type as before.

    Parameters
    ----------
    model       : loaded Keras model
    img_array   : preprocessed image (1, 224, 224, 3) float32
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

    # 1. Locate the layer (and, if nested, its owning submodel).
    try:
        if layer_name is not None:
            owner, found_name, owner_index = model, layer_name, None
            # Try to get the owner of the layer
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

    # 2. Strategy A: directly access layer if possible
    try:
        conv_outputs, grads = _gradcam_direct(model, img_array, class_index, found_name)
        return _finalize_heatmap(conv_outputs, grads)
    except Exception:
        attempts_trace.append("Strategy A (direct layer access) failed:\n" + traceback.format_exc())

    # 3. Strategy B: nested two-stage rebuild
    try:
        if owner_index is None:
            raise ValueError(
                "Conv layer is not nested inside a submodel; "
                "Strategy A should have succeeded — see its error above."
            )
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
```
