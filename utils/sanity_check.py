"""
sanity_check.py — Smart Paddy AI: Post-prediction sanity checker
Save this file at: smart_paddy_ai/utils/sanity_check.py

Catches obvious misclassifications using basic image color analysis.
No retraining needed — works on top of existing model predictions.
"""

import numpy as np
from PIL import Image


def analyze_image(image: Image.Image) -> dict:
    """
    Analyzes basic color features of the leaf image.
    Returns a dict of visual ratios.
    """
    img = image.resize((224, 224))
    arr = np.array(img).astype(float)

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    total = 224 * 224

    # Brown spots — high R, medium G, low B (classic brown_spot pattern)
    brown_mask  = (r > 120) & (r < 210) & (g > 60) & (g < 150) & (b < 100) & (r > g) & (g > b)
    brown_ratio = brown_mask.sum() / total

    # Yellow areas — tungro / downy_mildew causes yellowing
    yellow_mask  = (r > 150) & (g > 140) & (b < 100) & (r > b) & (g > b)
    yellow_ratio = yellow_mask.sum() / total

    # Healthy green areas
    green_mask  = (g > r) & (g > b) & (g > 80)
    green_ratio = green_mask.sum() / total

    # Dark / dead areas — dead_heart / blight
    dark_mask  = (r < 60) & (g < 60) & (b < 60)
    dark_ratio = dark_mask.sum() / total

    # Pale / white lesions — blast
    pale_mask  = (r > 180) & (g > 180) & (b > 150)
    pale_ratio = pale_mask.sum() / total

    return {
        "brown_ratio":  round(float(brown_ratio), 3),
        "yellow_ratio": round(float(yellow_ratio), 3),
        "green_ratio":  round(float(green_ratio), 3),
        "dark_ratio":   round(float(dark_ratio), 3),
        "pale_ratio":   round(float(pale_ratio), 3),
    }


def sanity_check(label: str, confidence: float, image: Image.Image) -> tuple:
    """
    Checks if the model prediction makes visual sense.
    Overrides obviously wrong predictions using color rules.

    Returns: (corrected_label, corrected_confidence, was_overridden: bool)
    """
    features = analyze_image(image)

    brown  = features["brown_ratio"]
    yellow = features["yellow_ratio"]
    green  = features["green_ratio"]
    dark   = features["dark_ratio"]
    pale   = features["pale_ratio"]

    original_label = label

    # ── Rule 1: Says Normal but has clear brown spots ──────────
    if label == "normal" and brown > 0.08:
        if yellow > 0.10:
            label = "tungro"
        else:
            label = "brown_spot"

    # ── Rule 2: Says Normal but significant yellowing ──────────
    elif label == "normal" and yellow > 0.15:
        label = "tungro"

    # ── Rule 3: Says Normal but pale/white lesions present ─────
    elif label == "normal" and pale > 0.12 and green < 0.4:
        label = "blast"

    # ── Rule 4: Says Normal but lots of dark/dead areas ────────
    elif label == "normal" and dark > 0.12:
        label = "dead_heart"

    # ── Rule 5: Low confidence + brown patches ─────────────────
    elif confidence < 0.45 and brown > 0.10:
        label = "brown_spot"

    # ── Rule 6: Low confidence + yellowing ─────────────────────
    elif confidence < 0.45 and yellow > 0.12:
        label = "tungro"

    # ── Rule 7: Says brown_spot but image is mostly green ──────
    elif label == "brown_spot" and green > 0.65 and brown < 0.04:
        label = "normal"

    was_overridden = label != original_label
    new_confidence = 0.68 if was_overridden else confidence

    return label, new_confidence, was_overridden