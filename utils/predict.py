"""
utils/predict.py — Smart Paddy AI: Prediction Engine

Loads the existing H5 model and performs Paddy disease prediction.
Includes compatibility handling for older H5 files that store
DepthwiseConv2D with an unsupported groups=1 argument.
"""

import os
import json

import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D


# ─────────────────────── PATHS ──────────────────────────────────
# Paths are relative to the repository root, where app.py is located.
MODEL_PATH = "model/paddy_model.h5"
CLASS_IDX_PATH = "model/class_indices.json"


# ─────────────────────── CONFIG ─────────────────────────────────
IMG_SIZE = (224, 224)


# ─────────────────────── GLOBALS ────────────────────────────────
_model = None
_class_names = None
_class_indices = None


# ─────────────── H5/KERAS COMPATIBILITY LAYER ───────────────────
class CompatibleDepthwiseConv2D(DepthwiseConv2D):
    """
    Compatibility wrapper for H5 models saved with a groups=1 field.

    Some model files contain groups=1 in the serialized DepthwiseConv2D
    configuration, while the installed Keras version does not accept that
    keyword for this layer. Removing groups=1 is safe because a depthwise
    convolution is already a single-group operation.
    """

    @classmethod
    def from_config(cls, config):
        config = dict(config)
        config.pop("groups", None)
        return super().from_config(config)


# ─────────────────────── LOADERS ────────────────────────────────
def _load_class_indices() -> dict:
    """Load the class-index mapping saved during model training."""
    if not os.path.exists(CLASS_IDX_PATH):
        raise FileNotFoundError(
            f"class_indices.json not found at {CLASS_IDX_PATH}. "
            "Make sure the model folder is committed to the repository."
        )

    with open(CLASS_IDX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_model():
    """Lazy-load the Keras model and class mapping."""
    global _model, _class_names, _class_indices

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Make sure paddy_model.h5 is committed inside the model folder."
            )

        # compile=False is sufficient for prediction-only use. The custom
        # object removes groups=1 from older H5 DepthwiseConv2D configurations.
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

        print("\n===== CLASS MAPPING LOADED (index -> class) =====")
        for index, name in enumerate(_class_names):
            print(f"  [{index}] {name}")
        print("=================================================\n")

    return _model, _class_names


# ─────────────────────── PREPROCESSING ──────────────────────────
def preprocess(image: Image.Image) -> np.ndarray:
    """
    Preprocess a PIL image for EfficientNetB0.

    The image is resized to 224x224. No manual division by 255 is applied,
    because EfficientNetB0 includes its own input preprocessing layer in the
    trained model.
    """
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    image = image.convert("RGB")
    image = image.resize(IMG_SIZE, Image.LANCZOS)

    img = np.array(image, dtype=np.float32)
    img = np.expand_dims(img, axis=0)

    return img


# ─────────────────────── PREDICTION ─────────────────────────────
def predict_image(image: Image.Image):
    """
    Run inference on a PIL image.

    Returns:
        predicted_class: Predicted disease/class name.
        confidence: Confidence as a value from 0 to 1.
        all_probs: Dictionary containing each class and its percentage.
    """
    model, class_names = get_model()

    img = preprocess(image)
    preds = model.predict(img, verbose=0)[0]

    class_index = int(np.argmax(preds))
    confidence = float(np.max(preds))

    if class_index >= len(class_names):
        raise RuntimeError(
            "The model output has more classes than class_indices.json. "
            f"Model outputs: {len(preds)}, class names: {len(class_names)}."
        )

    predicted_class = class_names[class_index]

    all_probs = {
        class_name: round(float(preds[index]) * 100, 1)
        for index, class_name in enumerate(class_names)
        if index < len(preds)
    }

    print("\n--- Prediction ---")
    for class_name, percentage in sorted(
        all_probs.items(),
        key=lambda item: -item[1],
    ):
        bar = "█" * int(percentage / 5)
        print(f"  {class_name:35s}: {percentage:5.1f}%  {bar}")
    print(
        f"  -> Final: {predicted_class} "
        f"({confidence * 100:.1f}%)\n"
    )

    return predicted_class, confidence, all_probs
