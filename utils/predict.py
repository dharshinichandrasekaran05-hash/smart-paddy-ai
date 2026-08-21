"""
utils/predict.py — Smart Paddy AI prediction engine.

This version supports older H5 files and runs inference using a direct
model call instead of model.predict(), avoiding Keras predict-function
tracing issues on Streamlit Cloud.
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
IMG_SIZE = (224, 224)

_model = None
_class_names = None
_class_indices = None


class CompatibleDepthwiseConv2D(DepthwiseConv2D):
    """Load H5 files containing an older groups=1 layer argument."""

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


def get_model():
    """Load the model and class names once per Streamlit process."""
    global _model, _class_names, _class_indices

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

        _class_indices = _load_class_indices()
        _class_names = [
            name
            for name, index in sorted(
                _class_indices.items(),
                key=lambda item: int(item[1]),
            )
        ]

        print("===== CLASS MAPPING LOADED =====")
        for index, name in enumerate(_class_names):
            print(f"[{index}] {name}")

    return _model, _class_names


def preprocess(image: Image.Image) -> np.ndarray:
    """Convert an uploaded image into the model's expected input tensor."""
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    image = image.convert("RGB")
    image = image.resize(IMG_SIZE, Image.LANCZOS)
    array = np.asarray(image, dtype=np.float32)
    return np.expand_dims(array, axis=0)


def predict_image(image: Image.Image):
    """Return predicted class, confidence, and class probabilities."""
    model, class_names = get_model()
    image_tensor = preprocess(image)

    # Direct eager inference avoids Keras' generated tf__predict_function.
    output = model(image_tensor, training=False)
    if hasattr(output, "numpy"):
        predictions = output.numpy()
    else:
        predictions = np.asarray(output)

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
