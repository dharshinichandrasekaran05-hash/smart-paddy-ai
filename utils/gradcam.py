"""
utils/gradcam.py — Smart Paddy AI: Grad-CAM Explainability
Place at: smart_paddy_ai/utils/gradcam.py

Generates heatmaps highlighting infected regions on a paddy leaf image.
Compatible with EfficientNetB0 (last conv layer = "top_conv").
"""

import numpy as np
import cv2
import tensorflow as tf
from PIL import Image
import io


# ─────────────────────── LAYER DETECTION ─────────────────────
def _find_last_conv_layer(model) -> str:
    """
    Walk layers in reverse and return the first Conv2D name found.
    Works for EfficientNetB0 and most CNN architectures.
    """
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
        # EfficientNet wraps in a sub-model
        if hasattr(layer, "layers"):
            for sub in reversed(layer.layers):
                if isinstance(sub, tf.keras.layers.Conv2D):
                    return sub.name
    raise ValueError("No Conv2D layer found in model.")


# ─────────────────────── GRAD-CAM CORE ───────────────────────
def compute_gradcam(
    model,
    img_array: np.ndarray,
    class_index: int,
    layer_name: str | None = None,
) -> np.ndarray:
    """
    Compute Grad-CAM heatmap for a given class index.

    Parameters
    ----------
    model       : loaded Keras model
    img_array   : preprocessed image (1, 224, 224, 3) float32
    class_index : predicted class index
    layer_name  : target conv layer (auto-detected if None)

    Returns
    -------
    heatmap : np.ndarray (224, 224) normalised 0–1
    """
    if layer_name is None:
        layer_name = _find_last_conv_layer(model)

    # Build gradient model
    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[
            model.get_layer(layer_name).output,
            model.output,
        ],
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array, training=False)
        loss = predictions[:, class_index]

    # Gradient of class score w.r.t. conv feature maps
    grads       = tape.gradient(loss, conv_outputs)            # (1, H, W, C)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))       # (C,)

    conv_outputs = conv_outputs[0]                             # (H, W, C)
    heatmap      = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap      = tf.squeeze(heatmap)                         # (H, W)

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
    heatmap_uint8   = np.uint8(255 * heatmap_resized)
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
    """
    from utils.predict import preprocess   # avoid circular import

    img_array = preprocess(pil_image)

    heatmap  = compute_gradcam(model, img_array, class_index)
    resized  = pil_image.resize((224, 224), Image.LANCZOS)
    overlaid = overlay_heatmap(resized, heatmap)

    return resized, overlaid


def pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert a PIL Image to raw bytes for Streamlit download."""
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()