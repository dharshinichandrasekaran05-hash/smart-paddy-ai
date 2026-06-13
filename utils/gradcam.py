"""
utils/gradcam.py — Smart Paddy AI: Grad-CAM Explainability
"""
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import numpy as np
import cv2
import tensorflow as tf
import tf_keras
from PIL import Image
import io


def _find_last_conv_layer(model) -> str:
    for layer in reversed(model.layers):
        if isinstance(layer, tf_keras.layers.Conv2D):
            return layer.name
        if hasattr(layer, "layers"):
            for sub in reversed(layer.layers):
                if isinstance(sub, tf_keras.layers.Conv2D):
                    return sub.name
    raise ValueError("No Conv2D layer found in model.")


def compute_gradcam(model, img_array, class_index, layer_name=None):
    if layer_name is None:
        layer_name = _find_last_conv_layer(model)

    grad_model = tf_keras.models.Model(
        inputs=model.inputs,
        outputs=[model.get_layer(layer_name).output, model.output],
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array, training=False)
        loss = predictions[:, class_index]

    grads        = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap      = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap      = tf.squeeze(heatmap)
    heatmap      = tf.nn.relu(heatmap).numpy()

    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()

    return heatmap.astype(np.float32)


def overlay_heatmap(original_image, heatmap, alpha=0.45, colormap=cv2.COLORMAP_JET):
    orig_w, orig_h  = original_image.size
    orig_rgb        = np.array(original_image.convert("RGB"))
    heatmap_resized = cv2.resize(heatmap, (orig_w, orig_h))
    heatmap_uint8   = np.uint8(255 * heatmap_resized)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, colormap)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    overlay         = cv2.addWeighted(orig_rgb, 1 - alpha, heatmap_colored, alpha, 0)
    return Image.fromarray(overlay)


def generate_gradcam(model, pil_image, class_index):
    from utils.predict import preprocess
    img_array = preprocess(pil_image)
    heatmap   = compute_gradcam(model, img_array, class_index)
    resized   = pil_image.resize((224, 224), Image.LANCZOS)
    overlaid  = overlay_heatmap(resized, heatmap)
    return resized, overlaid


def pil_to_bytes(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()
