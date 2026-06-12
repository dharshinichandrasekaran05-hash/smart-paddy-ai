"""
utils/severity.py — Smart Paddy AI: Disease Severity Estimation
Place at: smart_paddy_ai/utils/severity.py

Estimates severity as a percentage based on:
  - Model confidence for diseased classes
  - Pixel-level infected area from Grad-CAM heatmap
"""

import numpy as np


# ─────────────────────── THRESHOLDS ───────────────────────────
SEVERITY_LEVELS = [
    (0,  30,  "Mild",     "#28a745"),   # green
    (31, 70,  "Moderate", "#ffc107"),   # amber
    (71, 100, "Severe",   "#dc3545"),   # red
]


def get_severity_label(severity_pct: float) -> tuple[str, str]:
    """
    Map a 0–100 percentage to a (label, hex_color) severity category.
    """
    for lo, hi, label, color in SEVERITY_LEVELS:
        if lo <= severity_pct <= hi:
            return label, color
    return "Severe", "#dc3545"


def estimate_severity(
    predicted_class: str,
    confidence: float,
    heatmap: np.ndarray | None = None,
) -> dict:
    """
    Estimate disease severity.

    Parameters
    ----------
    predicted_class : str   — e.g. "Blast"
    confidence      : float — model confidence 0–1
    heatmap         : optional Grad-CAM heatmap (H×W float32 0–1)

    Returns
    -------
    dict with keys: percentage, label, color, method
    """
    if predicted_class.lower() in ("healthy", "normal"):   # ✅ FIX: include "normal"
        return {
            "percentage": 0,
            "label":      "None",
            "color":      "#28a745",
            "method":     "healthy",
        }

    if heatmap is not None:
        # Percentage of pixels above activation threshold (0.4)
        activated   = (heatmap > 0.40).sum()
        total       = heatmap.size
        pixel_ratio = float(activated) / float(total)

        # Weighted combination: 60% heatmap area, 40% confidence
        raw_pct     = (pixel_ratio * 0.60 + (confidence - 0.5) * 0.40) * 2
        raw_pct     = max(0.0, min(1.0, raw_pct))
        severity_pct = round(raw_pct * 100, 1)
        method = "gradcam+confidence"
    else:
        # Fallback: confidence-based only
        # Map confidence [0.3 → 1.0] to severity [0 → 100]
        severity_pct = round(min(100.0, max(0.0, (confidence - 0.3) / 0.7 * 100)), 1)
        method = "confidence"

    label, color = get_severity_label(severity_pct)

    return {
        "percentage": severity_pct,
        "label":      label,
        "color":      color,
        "method":     method,
    }


def crop_health_index(
    predicted_class: str,
    confidence: float,
    severity_pct: float,
) -> dict:
    """
    Calculate a 0–100 Crop Health Index (CHI).

    Healthy plants score high; diseased + high-severity score low.

    Returns
    -------
    dict with keys: score, category, color
    """
    if predicted_class.lower() in ("healthy", "normal"):   # ✅ FIX: include "normal"
        # Small deduction for low-confidence healthy predictions
        base_score = 95 - round((1 - confidence) * 20)
    else:
        # Start from full health, subtract severity impact
        severity_weight = severity_pct / 100.0
        confidence_weight = confidence
        penalty = severity_weight * confidence_weight * 70
        base_score = max(0, round(90 - penalty))

    score = max(0, min(100, base_score))

    if score >= 90:
        category, color = "Excellent", "#27ae60"
    elif score >= 75:
        category, color = "Good",      "#2ecc71"
    elif score >= 50:
        category, color = "Moderate",  "#f39c12"
    else:
        category, color = "Poor",      "#e74c3c"

    return {"score": score, "category": category, "color": color}