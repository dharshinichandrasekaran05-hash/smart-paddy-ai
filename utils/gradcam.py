"""
utils/gradcam.py — Smart Paddy AI: Grad-CAM Explainability

Uses the loaded model's actual input dimensions. The existing app.py flow is
unchanged: generate_gradcam() returns the original and overlay images, while
compute_gradcam() returns a heatmap for severity and explainability reports.
"""

import io

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image


def _find_last_conv_layer(model) -> str:
    """Return the last available Conv2D layer name."""
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name

        if hasattr(layer, "layers"):
            for sublayer in reversed(layer.layers):
                if isinstance(sublayer, tf.keras.layers.Conv2D):
                    return sublayer.name

    raise ValueError("No Conv2D layer found in model; Grad-CAM is unavailable.")


def _model_input_size(model):
    """Return (width, height, channels) from model.input_shape."""
    shape = model.input_shape

    if isinstance(shape, list):
        shape = shape[0]
    if isinstance(shape, dict):
        shape = next(iter(shape.values()))

    if shape is None or len(shape) != 4:
        raise ValueError(f"Unsupported model input shape: {shape}")

    _, height, width, channels = shape
    if height is None or width is None:
        raise ValueError(f"Dynamic spatial input shape is unsupported: {shape}")

    return int(width), int(height), int(channels or 3)


def _preprocess_for_model(pil_image: Image.Image, model) -> np.ndarray:
    """Create a tensor with exactly the model's expected shape."""
    width, height, channels = _model_input_size(model)
    image = pil_image.convert("RGB").resize((width, height), Image.LANCZOS)
    array = np.asarray(image, dtype=np.float32)

    if channels == 1:
        array = np.mean(array, axis=2, keepdims=True)
    elif channels != 3:
        raise ValueError(f"Unsupported model channel count: {channels}")

    return np.expand_dims(array, axis=0)


def compute_gradcam(
    model,
    img_array: np.ndarray,
    class_index: int,
    layer_name: str | None = None,
) -> np.ndarray:
    """Compute and return a normalised Grad-CAM heatmap."""
    if layer_name is None:
        layer_name = _find_last_conv_layer(model)

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[model.get_layer(layer_name).output, model.output],
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array, training=False)
        loss = predictions[:, class_index]

    grads = tape.gradient(loss, conv_outputs)
    if grads is None:
        raise ValueError("Gradients were unavailable for the selected layer.")

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.nn.relu(heatmap).numpy()

    maximum = float(heatmap.max())
    if maximum > 0:
        heatmap = heatmap / maximum

    return heatmap.astype(np.float32)


def overlay_heatmap(
    original_image: Image.Image,
    heatmap: np.ndarray,
    alpha: float = 0.45,
    colormap: int = cv2.COLORMAP_JET,
) -> Image.Image:
    """Blend a heatmap over the original image at its original size."""
    original = original_image.convert("RGB")
    width, height = original.size
    original_array = np.asarray(original)

    heatmap_resized = cv2.resize(heatmap, (width, height))
    heatmap_uint8 = np.uint8(255 * np.clip(heatmap_resized, 0, 1))
    colored = cv2.applyColorMap(heatmap_uint8, colormap)
    colored = cv2.cvtColor(colored, cv2.COLOR_BGR2RGB)

    overlay = cv2.addWeighted(
        original_array,
        1 - alpha,
        colored,
        alpha,
        0,
    )
    return Image.fromarray(overlay)


def generate_gradcam(
    model,
    pil_image: Image.Image,
    class_index: int,
) -> tuple[Image.Image, Image.Image]:
    """Return the original image and its Grad-CAM overlay."""
    img_array = _preprocess_for_model(pil_image, model)
    heatmap = compute_gradcam(model, img_array, class_index)
    original = pil_image.convert("RGB")
    overlaid = overlay_heatmap(original, heatmap)
    return original, overlaid


def pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert a PIL image to bytes for Streamlit download."""
    buffer = io.BytesIO()
    img.save(buffer, format=fmt)
    return buffer.getvalue()
