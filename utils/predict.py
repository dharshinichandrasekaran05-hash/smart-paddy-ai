"""
utils/predict.py — Smart Paddy AI prediction engine.

Loads the existing H5 model, removes the legacy DepthwiseConv2D groups field
when needed, and automatically resizes images to the model's actual input
height and width.
"""

import os
import json

import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D


MODEL_PATH = "model/paddy_model.h5"
CLASS_IDX_PATH = "model/class_indices.json"

_model = None
_class_names = None
_class_indices = None
_input_size = None


class CompatibleDepthwiseConv2D(DepthwiseConv2D):
    """Compatibility wrapper for older H5 DepthwiseConv2D configs."""

    @classmethod
    def from_config(cls, config):
        config = dict(config)
        config.pop("groups", None)
        return super().from_config(config)


def _load_class_indices() -> dict:
    if not os.path.exists(CLASS_IDX_PATH):
        raise FileNotFoundError(
            f"class_indices.json not found at {CLASS_IDX_PATH}."
        )

    with open(CLASS_IDX_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def _find_input_size(model):
    """Return (width, height, channels) from the loaded model input shape."""
    shape = model.input_shape

    if isinstance(shape, list):
        shape = shape[0]
    if isinstance(shape, dict):
        shape = next(iter(shape.values()))

    if shape is None or len(shape) != 4:
        raise ValueError(
            f"Unsupported model input shape: {shape}. Expected (None, height, width, channels)."
        )

    _, height, width, channels = shape
    if height is None or width is None:
        raise ValueError(f"Model has dynamic spatial input shape: {shape}")

    return int(width), int(height), int(channels or 3)


def get_model():
    """Load the model, input size, and class mapping once."""
    global _model, _class_names, _class_indices, _input_size

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}."
            )

        _model = load_model(
            MODEL_PATH,
            compile=False,
            custom_objects={
                "DepthwiseConv2D": CompatibleDepthwiseConv2D,
            },
        )

        _input_size = _find_input_size(_model)
        _class_indices = _load_class_indices()
        _class_names = [
            name
            for name, index in sorted(
                _class_indices.items(),
                key=lambda item: int(item[1]),
            )
        ]

        print(f"Model input size: {_input_size}")
        print("===== CLASS MAPPING LOADED =====")
        for index, name in enumerate(_class_names):
            print(f"[{index}] {name}")

    return _model, _class_names


def preprocess(image: Image.Image, input_size=None) -> np.ndarray:
    """Resize and convert an uploaded image to the model input tensor."""
    if input_size is None:
        input_size = (224, 224, 3)

    width, height, channels = input_size

    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    image = image.convert("RGB")
    image = image.resize((width, height), Image.LANCZOS)
    array = np.asarray(image, dtype=np.float32)

    if channels == 1:
        array = np.mean(array, axis=2, keepdims=True)
    elif channels != 3:
        raise ValueError(
            f"Unsupported model channel count: {channels}. Expected 1 or 3."
        )

    return np.expand_dims(array, axis=0)


def predict_image(image: Image.Image):
    """Return predicted class, confidence, and class probabilities."""
    model, class_names = get_model()
    image_tensor = preprocess(image, _input_size)

    # Direct eager inference avoids generated tf__predict_function issues.
    output = model(image_tensor, training=False)
    predictions = output.numpy() if hasattr(output, "numpy") else np.asarray(output)
    predictions = np.asarray(predictions)[0]

    class_index = int(np.argmax(predictions))
    confidence = float(predictions[class_index])

    if class_index >= len(class_names):
        raise RuntimeError(
            "Model output and class_indices.json do not match: "
            f"model returned {len(predictions)} classes but only "
            f"{len(class_names)} class names were found."
        )

    predicted_class = class_names[class_index]
    all_probs = {
        name: round(float(predictions[index]) * 100, 1)
        for index, name in enumerate(class_names)
        if index < len(predictions)
    }

    print("\n--- Prediction ---")
    for name, percentage in sorted(
        all_probs.items(), key=lambda item: -item[1]
    ):
        bar = "█" * int(percentage / 5)
        print(f"  {name:35s}: {percentage:5.1f}%  {bar}")
    print(f"  -> Final: {predicted_class} ({confidence * 100:.1f}%)\n")

    return predicted_class, confidence, all_probs
