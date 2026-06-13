"""
utils/predict.py — Smart Paddy AI: Prediction Engine
"""
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import json
import numpy as np
from PIL import Image
import tensorflow as tf
import tf_keras
from tf_keras.models import load_model

# ─────────────────────── PATHS ────────────────────────────────
MODEL_PATH     = "model/paddy_model.h5"
CLASS_IDX_PATH = "model/class_indices.json"

# ─────────────────────── CONFIG ───────────────────────────────
IMG_SIZE = (128, 128)

# ─────────────────────── GLOBALS ──────────────────────────────
_model         = None
_class_names   = None
_class_indices = None

# ─────────────────────── LOADERS ──────────────────────────────
def _load_class_indices() -> dict:
    if not os.path.exists(CLASS_IDX_PATH):
        raise FileNotFoundError(
            f"class_indices.json not found at {CLASS_IDX_PATH}. "
            "Run train.py first so class mapping is generated."
        )
    with open(CLASS_IDX_PATH, "r") as f:
        return json.load(f)

def get_model():
    global _model, _class_names, _class_indices

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Run train.py to train the model first."
            )
        _model = load_model(MODEL_PATH, compile=False)

        _class_indices = _load_class_indices()
        _class_names = [
            k for k, _ in sorted(_class_indices.items(), key=lambda x: x[1])
        ]

        print("\n===== CLASS MAPPING LOADED =====")
        for i, name in enumerate(_class_names):
            print(f"  [{i}] {name}")
        print("================================\n")

    return _model, _class_names

# ─────────────────────── PREPROCESSING ────────────────────────
def preprocess(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE, Image.LANCZOS)
    img = np.array(image, dtype=np.float32)
    img = np.expand_dims(img, axis=0)
    return img

# ─────────────────────── PREDICTION ───────────────────────────
def predict_image(image: Image.Image):
    model, class_names = get_model()
    img   = preprocess(image)
    preds = model.predict(img, verbose=0)[0]

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
