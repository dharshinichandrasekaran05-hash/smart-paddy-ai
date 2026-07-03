"""
utils/explainability.py — Smart Paddy AI: AI Explainability Report Engine
Place at: smart_paddy_ai/utils/explainability.py

Builds a structured, publication-style explainability report from the
EXISTING Grad-CAM heatmap (utils/gradcam.py -> compute_gradcam) and the
model's confidence score. Every value below is derived mathematically
from the heatmap array — nothing is randomly generated.

Public entry point
-------------------
generate_explainability_report(disease, confidence, heatmap, severity_pct=None)
    -> dict with all report fields, ready to render in Streamlit.
"""

from __future__ import annotations
import numpy as np

# Activation threshold used to decide "this pixel belongs to the lesion".
# Kept identical to the threshold already used in utils/severity.py (0.40)
# so Feature 1 stays numerically consistent with the existing severity math.
ACTIVATION_THRESHOLD = 0.40


# ─────────────────────── REGION SEGMENTATION ───────────────────
def _region_shares(heatmap: np.ndarray) -> dict:
    """
    Split the heatmap into a 3x3 grid and return the share of activated
    ("above-threshold") pixels that fall into each named zone:
        tip    -> top row of the grid
        center -> middle cell
        edge   -> left/right columns + bottom row
    Returns a dict of zone -> fraction of TOTAL activated pixels (0-1).
    """
    h, w = heatmap.shape
    activated = heatmap > ACTIVATION_THRESHOLD
    total_activated = int(activated.sum())

    if total_activated == 0:
        return {"tip": 0.0, "center": 0.0, "edge": 0.0}

    r1, r2 = h // 3, (2 * h) // 3
    c1, c2 = w // 3, (2 * w) // 3

    tip_mask = np.zeros_like(activated)
    tip_mask[0:r1, :] = True

    center_mask = np.zeros_like(activated)
    center_mask[r1:r2, c1:c2] = True

    edge_mask = ~tip_mask & ~center_mask

    tip_count    = int((activated & tip_mask).sum())
    center_count = int((activated & center_mask).sum())
    edge_count   = int((activated & edge_mask).sum())

    return {
        "tip":    tip_count    / total_activated,
        "center": center_count / total_activated,
        "edge":   edge_count   / total_activated,
    }


def _infection_location(shares: dict) -> str:
    """
    Decide a human-readable infection-location label from region shares.
    "Multiple Regions" is used when no single zone clearly dominates.
    """
    if sum(shares.values()) == 0:
        return "No Significant Activation"

    sorted_zones = sorted(shares.items(), key=lambda kv: -kv[1])
    top_zone, top_share = sorted_zones[0]
    second_share = sorted_zones[1][1] if len(sorted_zones) > 1 else 0.0

    label_map = {"tip": "Leaf Tip", "center": "Leaf Center", "edge": "Leaf Edge"}

    # If the runner-up zone is within 15 percentage points of the leader,
    # treat the infection as spread across multiple regions.
    if top_share - second_share < 0.15 and top_share < 0.60:
        return "Multiple Regions"
    return label_map[top_zone]


# ─────────────────────── AREA / COVERAGE ───────────────────────
def _disease_healthy_area(heatmap: np.ndarray) -> tuple[float, float]:
    """Percentage of heatmap pixels above/below the activation threshold."""
    activated = (heatmap > ACTIVATION_THRESHOLD).sum()
    total     = heatmap.size
    disease_pct = round(float(activated) / float(total) * 100, 1)
    healthy_pct = round(100.0 - disease_pct, 1)
    return disease_pct, healthy_pct


def _lesion_coverage_label(disease_pct: float) -> str:
    if disease_pct < 15:
        return "Localized (isolated lesions, <15% leaf area)"
    if disease_pct < 40:
        return "Moderate spread (15–40% leaf area)"
    if disease_pct < 65:
        return "Widespread (40–65% leaf area)"
    return "Extensive (>65% leaf area affected)"


# ─────────────────────── HEATMAP FOCUS ──────────────────────────
def _heatmap_focus(heatmap: np.ndarray) -> dict:
    """
    Quantify how 'focused' vs 'diffuse' the model's attention is.
    Peak intensity, mean intensity of activated area, and normalised
    spread (std) are used to classify focus as Focused / Moderate / Diffuse.
    """
    activated_vals = heatmap[heatmap > ACTIVATION_THRESHOLD]
    if activated_vals.size == 0:
        return {
            "peak": 0.0, "mean_active": 0.0, "std_active": 0.0,
            "focus_label": "No Clear Focus",
        }

    peak        = float(heatmap.max())
    mean_active = float(activated_vals.mean())
    std_active  = float(activated_vals.std())

    # Low spread relative to mean => concentrated ("Focused") attention.
    coefficient_of_variation = std_active / mean_active if mean_active > 0 else 0.0
    if coefficient_of_variation < 0.20:
        focus_label = "Focused"
    elif coefficient_of_variation < 0.40:
        focus_label = "Moderately Focused"
    else:
        focus_label = "Diffuse"

    return {
        "peak": round(peak, 3),
        "mean_active": round(mean_active, 3),
        "std_active": round(std_active, 3),
        "focus_label": focus_label,
    }


# ─────────────────────── CONFIDENCE INTERPRETATION ──────────────
def _confidence_interpretation(confidence: float, focus_label: str) -> str:
    conf_pct = confidence * 100

    if conf_pct >= 85:
        base = "Very high confidence — the model found strong, unambiguous visual evidence."
    elif conf_pct >= 65:
        base = "High confidence — clear disease-consistent patterns were detected."
    elif conf_pct >= 45:
        base = "Moderate confidence — some disease-consistent features present, but signs are less distinct."
    else:
        base = "Low confidence — visual evidence is weak or ambiguous; manual verification is recommended."

    if focus_label == "Focused":
        base += " The attention heatmap is tightly concentrated on specific lesions, supporting this reading."
    elif focus_label == "Diffuse":
        base += " The attention heatmap is spread broadly across the leaf, which can lower prediction certainty."

    return base


# ─────────────────────── SUMMARY BUILDERS ───────────────────────
def _why_predicted(disease: str, location: str, coverage_label: str, focus_label: str) -> str:
    disease_name = disease.replace("_", " ").title()
    if disease.lower() in ("healthy", "normal"):
        return (
            "The Grad-CAM heatmap shows no meaningful concentration of activation on "
            "lesion-like regions, and pixel activation stayed below the disease threshold "
            "across the leaf — consistent with a healthy classification."
        )
    return (
        f"The model concentrated its attention primarily on the {location.lower()}, "
        f"with a {focus_label.lower()} activation pattern and {coverage_label.lower()}. "
        f"This spatial pattern of activated pixels is consistent with the visual signature "
        f"typically associated with {disease_name}."
    )


def _explainability_summary(disease, disease_pct, healthy_pct, location, coverage_label, conf_interp) -> str:
    disease_name = disease.replace("_", " ").title()
    return (
        f"For this leaf, the AI estimated {disease_pct}% of the visible tissue as "
        f"disease-affected and {healthy_pct}% as healthy, with attention concentrated "
        f"around the {location.lower()}. Coverage is classified as {coverage_label.lower()}. "
        f"{conf_interp}"
    )


def _agricultural_interpretation(disease: str, location: str, disease_pct: float) -> str:
    disease_name = disease.replace("_", " ").title()
    if disease.lower() in ("healthy", "normal"):
        return (
            "No corrective action is indicated. Continue routine field scouting to catch "
            "early symptoms before they spread."
        )
    urgency = (
        "Inspect the crop in person as soon as possible and consider immediate treatment."
        if disease_pct >= 40 else
        "Inspect the highlighted region closely during your next field walk; early-stage "
        "intervention now can prevent further spread."
    )
    return (
        f"Farmers should physically check the {location.lower()} of affected plants for "
        f"symptoms typical of {disease_name} (lesions, discolouration, or wilting depending "
        f"on disease type). {urgency}"
    )


# ─────────────────────── PUBLIC API ─────────────────────────────
def generate_explainability_report(
    disease: str,
    confidence: float,
    heatmap: np.ndarray | None,
    severity_pct: float | None = None,
) -> dict:
    """
    Build the full Feature-1 explainability report.

    Parameters
    ----------
    disease      : predicted class name (e.g. "blast")
    confidence   : model confidence, 0-1
    heatmap      : Grad-CAM heatmap array (H, W), values 0-1, or None if
                   Grad-CAM was unavailable for this image.
    severity_pct : optional severity percentage already computed by
                   utils.severity.estimate_severity — included for
                   cross-reference in the summary text.

    Returns
    -------
    dict with keys:
        disease_area_pct, healthy_area_pct, infection_location,
        lesion_coverage_label, focus, confidence_interpretation,
        why_predicted, explainability_summary, agricultural_interpretation,
        available (bool — False if no heatmap was available)
    """
    if heatmap is None:
        return {
            "available": False,
            "disease_area_pct": None,
            "healthy_area_pct": None,
            "infection_location": "Unavailable",
            "lesion_coverage_label": "Grad-CAM unavailable for this model layer.",
            "focus": {"focus_label": "Unavailable"},
            "confidence_interpretation": _confidence_interpretation(confidence, "Unavailable"),
            "why_predicted": (
                "Grad-CAM heatmap could not be generated for this image, so a spatial "
                "explanation is unavailable. The prediction is based on the model's "
                "learned features alone."
            ),
            "explainability_summary": (
                "Explainability visualisation unavailable for this prediction."
            ),
            "agricultural_interpretation": (
                "Rely on the treatment and prevention advisory below, and confirm "
                "visually in the field."
            ),
        }

    shares = _region_shares(heatmap)
    location = _infection_location(shares)
    disease_pct, healthy_pct = _disease_healthy_area(heatmap)
    coverage_label = _lesion_coverage_label(disease_pct)
    focus = _heatmap_focus(heatmap)
    conf_interp = _confidence_interpretation(confidence, focus["focus_label"])
    why = _why_predicted(disease, location, coverage_label, focus["focus_label"])
    summary = _explainability_summary(
        disease, disease_pct, healthy_pct, location, coverage_label, conf_interp
    )
    ag_interp = _agricultural_interpretation(disease, location, disease_pct)

    return {
        "available": True,
        "disease_area_pct": disease_pct,
        "healthy_area_pct": healthy_pct,
        "infection_location": location,
        "lesion_coverage_label": coverage_label,
        "focus": focus,
        "confidence_interpretation": conf_interp,
        "why_predicted": why,
        "explainability_summary": summary,
        "agricultural_interpretation": ag_interp,
    }
