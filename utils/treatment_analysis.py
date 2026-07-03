"""
utils/treatment_analysis.py — Smart Paddy AI: Treatment Effectiveness Engine
Place at: smart_paddy_ai/utils/treatment_analysis.py

Extends the existing advisory system (utils/advisory.py) with a structured,
comparable view of each treatment option: success rate, recovery time,
cost, eco-friendliness, suitable disease stage, and priority.

This module does NOT replace utils/advisory.py — it complements it.
Preventive measures are pulled directly from advisory.get_advisory() so
the two stay in sync and nothing is duplicated.
"""

from __future__ import annotations
from utils.advisory import get_advisory

# ─────────────────────── ALIASES (mirrors advisory.py) ─────────
_ALIASES = {
    "bacterial_panicle_blight": "bacterial panicle blight",
    "bacterial_leaf_blight":    "bacterial leaf blight",
    "bacterial_leaf_streak":    "bacterial leaf streak",
    "brown_spot":               "brown spot",
    "dead_heart":               "dead heart",
    "downy_mildew":             "downy mildew",
    "blast":                    "blast",
    "tungro":                   "tungro",
    "hispa":                    "hispa",
    "normal":                   "normal",
    "healthy":                  "healthy",
}

# ─────────────────────── TREATMENT KNOWLEDGE BASE ───────────────
# Each entry mirrors the chemical/biological options already named in
# utils/advisory.py's "treatment" lists, annotated with effectiveness data.
_TREATMENTS: dict[str, list[dict]] = {
    "blast": [
        {"name": "Tricyclazole 75 WP (0.6 g/L)", "success_rate": 85, "recovery_days": "10–14",
         "cost": "Medium", "eco": "Moderate", "stage": "Early to active infection"},
        {"name": "Isoprothiolane 40 EC (1.5 mL/L)", "success_rate": 78, "recovery_days": "10–14",
         "cost": "Medium", "eco": "Moderate", "stage": "Early infection"},
        {"name": "Blast-resistant varieties (ADT 43, CO 51)", "success_rate": 90, "recovery_days": "Preventive",
         "cost": "Low", "eco": "High", "stage": "Pre-planting"},
    ],
    "brown spot": [
        {"name": "Mancozeb 75 WP (2.5 g/L)", "success_rate": 80, "recovery_days": "7–10",
         "cost": "Low", "eco": "Moderate", "stage": "Early to active infection"},
        {"name": "Zinc Sulphate foliar spray (0.5%)", "success_rate": 70, "recovery_days": "10–15",
         "cost": "Low", "eco": "High", "stage": "Nutrient-deficiency stage"},
        {"name": "Balanced NPK + FYM", "success_rate": 75, "recovery_days": "Preventive",
         "cost": "Low", "eco": "High", "stage": "Pre-planting / ongoing"},
    ],
    "tungro": [
        {"name": "Remove & destroy infected plants", "success_rate": 60, "recovery_days": "Immediate (field-level)",
         "cost": "Low", "eco": "High", "stage": "Active infection"},
        {"name": "Imidacloprid 17.8 SL (0.3 mL/L) — vector control", "success_rate": 72, "recovery_days": "7–10",
         "cost": "Medium", "eco": "Low", "stage": "Vector (leafhopper) presence"},
        {"name": "Neem-based pesticide", "success_rate": 55, "recovery_days": "10–14",
         "cost": "Low", "eco": "High", "stage": "Vector deterrence"},
    ],
    "bacterial panicle blight": [
        {"name": "Copper Oxychloride 50 WP (3 g/L)", "success_rate": 70, "recovery_days": "10–14",
         "cost": "Medium", "eco": "Moderate", "stage": "Panicle initiation"},
        {"name": "Streptomycin Sulphate (0.5 g/L)", "success_rate": 65, "recovery_days": "7–10",
         "cost": "Medium", "eco": "Low", "stage": "Active infection"},
        {"name": "Hot-water seed treatment (52°C, 10 min)", "success_rate": 80, "recovery_days": "Preventive",
         "cost": "Low", "eco": "High", "stage": "Pre-sowing"},
    ],
    "bacterial leaf blight": [
        {"name": "Copper Hydroxide 77 WP (2 g/L)", "success_rate": 75, "recovery_days": "10–14",
         "cost": "Medium", "eco": "Moderate", "stage": "Early to active infection"},
        {"name": "Streptomycin + Tetracycline (0.5 g/L)", "success_rate": 70, "recovery_days": "7–10",
         "cost": "Medium", "eco": "Low", "stage": "Active infection"},
        {"name": "Resistant varieties (IR64, Swarna Sub1)", "success_rate": 88, "recovery_days": "Preventive",
         "cost": "Low", "eco": "High", "stage": "Pre-planting"},
    ],
    "bacterial leaf streak": [
        {"name": "Copper Oxychloride 50 WP (3 g/L)", "success_rate": 68, "recovery_days": "10–14",
         "cost": "Medium", "eco": "Moderate", "stage": "Early infection"},
        {"name": "Bronopol-based bactericide", "success_rate": 62, "recovery_days": "10 (repeat cycle)",
         "cost": "Medium", "eco": "Moderate", "stage": "Wet-weather active infection"},
        {"name": "Certified disease-free seed", "success_rate": 82, "recovery_days": "Preventive",
         "cost": "Low", "eco": "High", "stage": "Pre-sowing"},
    ],
    "dead heart": [
        {"name": "Cartap Hydrochloride 4G (18 kg/ha)", "success_rate": 80, "recovery_days": "7–10",
         "cost": "Medium", "eco": "Low", "stage": "Larval boring stage"},
        {"name": "Trichogramma japonicum (biological)", "success_rate": 65, "recovery_days": "14–21",
         "cost": "Low", "eco": "High", "stage": "Egg-laying stage (preventive)"},
        {"name": "Clip & destroy egg masses", "success_rate": 60, "recovery_days": "Preventive",
         "cost": "Low", "eco": "High", "stage": "Nursery stage"},
    ],
    "hispa": [
        {"name": "Malathion 50 EC (2 mL/L)", "success_rate": 75, "recovery_days": "5–7",
         "cost": "Low", "eco": "Low", "stage": "Active infestation"},
        {"name": "Neem Seed Kernel Extract 5%", "success_rate": 60, "recovery_days": "10–14",
         "cost": "Low", "eco": "High", "stage": "Early infestation"},
        {"name": "Hand-picking adults", "success_rate": 50, "recovery_days": "Ongoing (manual)",
         "cost": "Low", "eco": "High", "stage": "Early infestation"},
    ],
    "downy mildew": [
        {"name": "Metalaxyl + Mancozeb (Ridomil Gold, 2.5 g/L)", "success_rate": 78, "recovery_days": "10–14",
         "cost": "Medium", "eco": "Moderate", "stage": "Early to active infection"},
        {"name": "Fosetyl-Al 80 WP (3 g/L)", "success_rate": 72, "recovery_days": "10–14",
         "cost": "Medium", "eco": "Moderate", "stage": "Active infection"},
        {"name": "Field drainage improvement", "success_rate": 65, "recovery_days": "Preventive",
         "cost": "Low", "eco": "High", "stage": "Waterlogging risk stage"},
    ],
    "normal": [
        {"name": "No treatment required", "success_rate": 100, "recovery_days": "N/A",
         "cost": "None", "eco": "High", "stage": "N/A"},
    ],
    "healthy": [
        {"name": "No treatment required", "success_rate": 100, "recovery_days": "N/A",
         "cost": "None", "eco": "High", "stage": "N/A"},
    ],
}


def _priority_from_context(success_rate: int, severity_pct: float | None) -> str:
    """
    Derive a recommendation priority from the treatment's success rate and
    (if available) the current severity percentage from utils.severity.
    Purely rule-based — no randomness.
    """
    if severity_pct is not None and severity_pct >= 60:
        return "Urgent" if success_rate >= 70 else "High"
    if severity_pct is not None and severity_pct >= 30:
        return "High" if success_rate >= 70 else "Medium"
    if success_rate >= 80:
        return "High"
    if success_rate >= 60:
        return "Medium"
    return "Low"


def get_treatment_effectiveness(
    disease: str,
    severity_pct: float | None = None,
    lang: str = "english",
) -> dict:
    """
    Return structured treatment-effectiveness data for a predicted disease.

    Returns
    -------
    dict:
        disease           : resolved disease key
        treatments        : list of dicts, each with
                             name, success_rate, recovery_days, cost,
                             eco, stage, priority
        preventive_measures: list[str]  (pulled from advisory.py, kept in sync)
    """
    key = _ALIASES.get(disease.lower().strip(), disease.lower().strip())
    treatments = _TREATMENTS.get(key)

    if treatments is None:
        # graceful fallback consistent with advisory.py's fallback behaviour
        treatments = [{
            "name": "Consult local agriculture extension officer",
            "success_rate": 50, "recovery_days": "Varies",
            "cost": "Low", "eco": "High", "stage": "N/A",
        }]

    enriched = []
    for t in treatments:
        enriched.append({
            **t,
            "priority": _priority_from_context(t["success_rate"], severity_pct),
        })

    # Sort so the highest-priority, most effective option surfaces first
    priority_rank = {"Urgent": 0, "High": 1, "Medium": 2, "Low": 3}
    enriched.sort(key=lambda t: (priority_rank.get(t["priority"], 9), -t["success_rate"]))

    advisory = get_advisory(key, lang)

    return {
        "disease": key,
        "treatments": enriched,
        "preventive_measures": advisory.get("prevention", []),
    }
