"""
utils/severity.py — Smart Paddy AI: Disease Severity Estimation
Place at: smart_paddy_ai/utils/severity.py

Estimates severity as a percentage based on:
  - Model confidence for diseased classes
  - Pixel-level infected area from Grad-CAM heatmap
"""

from __future__ import annotations
import numpy as np

# Used only to build the localized `ai_summary` sentence below. Imported
# lazily-safe (utils.i18n has no circular dependency back on this module).
from utils.i18n import health_ai_summary_text


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


# ═══════════════════════════════════════════════════════════════
# NEW — Feature 3: Enhanced Crop Health Intelligence Dashboard
# ═══════════════════════════════════════════════════════════════
# This function REUSES estimate_severity() and crop_health_index() above —
# it does not recompute severity or health from scratch. It only derives
# the additional qualitative indicators the dashboard needs.
def advanced_health_dashboard(
    predicted_class: str,
    confidence: float,
    severity_result: dict,
    health_result: dict,
    lang: str = "english",
    disease_display: str | None = None,
) -> dict:
    """
    Build the extra fields needed for the "Enhanced Crop Health Intelligence
    Dashboard" without altering existing severity/health calculations.

    Parameters
    ----------
    predicted_class : str
    confidence       : float (0-1)
    severity_result  : dict returned by estimate_severity()
    health_result    : dict returned by crop_health_index()
    lang             : one of utils.i18n.LANGUAGE_ORDER — controls the
                        language of `ai_summary` only. The other enum
                        fields below (risk_indicator, recovery_potential,
                        leaf_quality) are intentionally returned as their
                        stable ENGLISH keys, exactly like before — app.py
                        already localizes those itself via
                        utils.i18n.translate_enum() at the call site, so
                        translating them here too would double-translate.
    disease_display  : optional already-localized disease display name
                        (e.g. from utils.i18n.disease_display_name) to use
                        inside the ai_summary sentence instead of the raw
                        `predicted_class` key. Falls back to a title-cased
                        version of `predicted_class` if omitted.

    Returns
    -------
    dict with keys:
        risk_indicator     : "Low" | "Medium" | "High"
        recovery_potential : label + color
        confidence_meter    : rounded percentage for gauge display
        leaf_quality        : label + color
        ai_summary          : short natural-language paragraph, localized
                               to `lang`
    """
    is_healthy = predicted_class.lower() in ("healthy", "normal")
    severity_pct = severity_result["percentage"]
    health_score = health_result["score"]

    # ── Disease Risk Indicator ──────────────────────────────────
    if is_healthy:
        risk_indicator, risk_color = "Low", "#28a745"
    elif severity_pct >= 60:
        risk_indicator, risk_color = "High", "#dc3545"
    elif severity_pct >= 30:
        risk_indicator, risk_color = "Medium", "#ffc107"
    else:
        risk_indicator, risk_color = "Low", "#28a745"

    # ── Recovery Potential ───────────────────────────────────────
    # Higher health score + lower severity => better recovery outlook.
    if is_healthy:
        recovery_label, recovery_color = "Not Applicable", "#95a5a6"
    else:
        recovery_score = (health_score * 0.6) + ((100 - severity_pct) * 0.4)
        if recovery_score >= 70:
            recovery_label, recovery_color = "High", "#27ae60"
        elif recovery_score >= 45:
            recovery_label, recovery_color = "Moderate", "#f39c12"
        else:
            recovery_label, recovery_color = "Low", "#e74c3c"

    # ── AI Confidence Meter (just a formatted pass-through) ───────
    confidence_meter = round(confidence * 100, 1)

    # ── Leaf Quality Assessment ────────────────────────────────
    # Combines health score with severity to give a plain-language
    # quality label for the leaf tissue itself.
    if is_healthy:
        leaf_quality, lq_color = "Excellent", "#27ae60"
    elif health_score >= 75:
        leaf_quality, lq_color = "Good", "#2ecc71"
    elif health_score >= 50:
        leaf_quality, lq_color = "Fair", "#f39c12"
    else:
        leaf_quality, lq_color = "Poor", "#e74c3c"

    # ── AI-generated health summary (localized to `lang`) ───────
    disease_name = disease_display or predicted_class.replace("_", " ").title()
    ai_summary = health_ai_summary_text(
        is_healthy=is_healthy,
        confidence_meter=confidence_meter,
        disease=disease_name,
        severity_label=severity_result["label"],
        severity_pct=severity_pct,
        health_score=health_score,
        health_category=health_result["category"],
        recovery_label=recovery_label,
        lang=lang,
    )

    return {
        "risk_indicator": risk_indicator,
        "risk_color": risk_color,
        "recovery_potential": recovery_label,
        "recovery_color": recovery_color,
        "confidence_meter": confidence_meter,
        "leaf_quality": leaf_quality,
        "leaf_quality_color": lq_color,
        "ai_summary": ai_summary,
    }
