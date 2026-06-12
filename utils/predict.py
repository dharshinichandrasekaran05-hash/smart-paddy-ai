"""
utils/predict.py — Smart Paddy AI: Prediction Engine
Place at: smart_paddy_ai/utils/predict.py

Fix applied:
  - IMG_SIZE changed to (128, 128) to match fast train.py
  - All other logic preserved
"""

import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

# ─────────────────────── PATHS ────────────────────────────────
MODEL_PATH     = "model/paddy_model.h5"
CLASS_IDX_PATH = "model/class_indices.json"

# ─────────────────────── CONFIG ───────────────────────────────
IMG_SIZE = (128, 128)   # ✅ Must match train.py IMG_SIZE exactly

# ─────────────────────── GLOBALS ──────────────────────────────
_model       = None
_class_names = None
_class_indices = None


# ─────────────────────── LOADERS ──────────────────────────────
def _load_class_indices() -> dict:
    """Load class-index mapping from JSON saved during training."""
    if not os.path.exists(CLASS_IDX_PATH):
        raise FileNotFoundError(
            f"class_indices.json not found at {CLASS_IDX_PATH}. "
            "Run train.py first so class mapping is generated."
        )
    with open(CLASS_IDX_PATH, "r") as f:
        return json.load(f)


def get_model():
    """Lazy-load the Keras model and class mapping. Prints mapping on first load."""
    global _model, _class_names, _class_indices

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Run train.py to train the model first."
            )
        _model = load_model(MODEL_PATH)

        _class_indices = _load_class_indices()
        _class_names = [
            k for k, _ in sorted(_class_indices.items(), key=lambda x: x[1])
        ]

        print("\n===== CLASS MAPPING LOADED (index -> class) =====")
        for i, name in enumerate(_class_names):
            print(f"  [{i}] {name}")
        print("=================================================\n")

    return _model, _class_names


# ─────────────────────── PREPROCESSING ────────────────────────
def preprocess(image: Image.Image) -> np.ndarray:
    """
    Preprocess a PIL image for EfficientNetB0.
    Image is resized to IMG_SIZE (128x128) to match training pipeline.
    ✅ FIX: NO rescale — EfficientNetB0 has built-in normalization.
    train.py uses NO rescale=1/255 (removed), so predict must match.
    """
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE, Image.LANCZOS)   # ✅ (128, 128)

    img = np.array(image, dtype=np.float32)
    # ✅ NO division by 255 — EfficientNetB0 preprocesses internally
    # Dividing by 255 here caused double normalization → bad predictions
    img = np.expand_dims(img, axis=0)               # (1, 128, 128, 3)

    return img


# ─────────────────────── PREDICTION ───────────────────────────
def predict_image(image: Image.Image):
    """
    Run inference on a PIL image.

    Returns
    -------
    predicted_class : str
    confidence      : float  (0-1)
    all_probs       : dict   {class_name: probability_percentage}

    Example
    -------
    predicted_class = "blast"
    confidence      = 0.83
    all_probs       = {"blast": 83.1, "brown_spot": 12.0, "healthy": 3.2, ...}
    """
    model, class_names = get_model()

    img   = preprocess(image)
    preds = model.predict(img, verbose=0)[0]   # shape: (num_classes,)

    class_index     = int(np.argmax(preds))
    confidence      = float(np.max(preds))
    predicted_class = class_names[class_index]

    all_probs = {
        cls: round(float(preds[i]) * 100, 1)
        for i, cls in enumerate(class_names)
    }

    print(f"\n--- Prediction ---")
    for cls, pct in sorted(all_probs.items(), key=lambda x: -x[1]):
        bar = "█" * int(pct / 5)
        print(f"  {cls:35s}: {pct:5.1f}%  {bar}")
    print(f"  -> Final: {predicted_class} ({confidence*100:.1f}%)\n")

    return predicted_class, confidence, all_probs