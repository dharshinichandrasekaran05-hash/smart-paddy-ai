"""
utils/explainability.py — Smart Paddy AI: AI Explainability Report Engine
Place at: smart_paddy_ai/utils/explainability.py

Builds a structured, publication-style explainability report from the
EXISTING Grad-CAM heatmap (utils/gradcam.py -> compute_gradcam) and the
model's confidence score. Every value below is derived mathematically
from the heatmap array — nothing is randomly generated.

──────────────────────────────────────────────────────────────────
LANGUAGE SUPPORT (fix)
──────────────────────────────────────────────────────────────────
Previously this module always built its prose in English, no matter
which language the farmer had selected in the sidebar — even though
utils/i18n.py already ships dedicated helpers for exactly this report
(confidence_interpretation_text, why_predicted_text,
explainability_summary_text, agricultural_interpretation_text,
translate_enum, ui_text). This file now accepts a `lang` parameter and
routes every piece of generated text through those i18n helpers, the
same way utils/severity.py, utils/pdf_report.py and utils/advisory.py
already do. All 11 languages are hand-written, local dictionary only —
no runtime translation API calls anywhere in this module.

Public entry point
-------------------
generate_explainability_report(disease, confidence, heatmap, severity_pct=None, lang="english")
    -> dict with all report fields, already localized to `lang`,
       ready to render in Streamlit.
"""

from __future__ import annotations
import numpy as np

from utils.i18n import (
    resolve_lang,
    translate_enum,
    ui_text,
    confidence_interpretation_text,
    why_predicted_text,
    explainability_summary_text,
    agricultural_interpretation_text,
)
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
    Decide a human-readable (English, internal-key) infection-location
    label from region shares. "Multiple Regions" is used when no single
    zone clearly dominates.

    NOTE: this returns the stable ENGLISH key (e.g. "Leaf Edge") — it is
    the lookup key for utils.i18n.translate_enum(), not the text shown to
    the farmer. Localization happens at the call site in
    generate_explainability_report(), never here.
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
    """
    Returns the stable ENGLISH key (matches utils.i18n's lesion-coverage
    translation block exactly) — localized later via translate_enum().
    """
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

    `focus_label` here is the stable ENGLISH key — localized later via
    translate_enum() at the call site.
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


# ─────────────────────── NO-HEATMAP FALLBACK TEXT ───────────────
# These three sentences only appear when Grad-CAM couldn't run at all.
# Hand-written for all 11 languages — local dictionary only, no API calls.
_NO_HEATMAP_WHY = {
    "english": "Grad-CAM heatmap could not be generated for this image, so a spatial explanation is unavailable. The prediction is based on the model's learned features alone.",
    "tamil": "இந்த படத்திற்கு Grad-CAM வெப்பப்படத்தை உருவாக்க முடியவில்லை, எனவே இடஞ்சார் விளக்கம் கிடைக்கவில்லை. கணிப்பு மாதிரி கற்றுக்கொண்ட அம்சங்களை மட்டுமே அடிப்படையாகக் கொண்டது.",
    "telugu": "ఈ చిత్రానికి Grad-CAM హీట్‌మ్యాప్ రూపొందించలేకపోయాము, కాబట్టి ప్రాదేశిక వివరణ అందుబాటులో లేదు. అంచనా మోడల్ నేర్చుకున్న లక్షణాలపై మాత్రమే ఆధారపడి ఉంది.",
    "kannada": "ಈ ಚಿತ್ರಕ್ಕೆ Grad-CAM ಹೀಟ್‌ಮ್ಯಾಪ್ ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ, ಆದ್ದರಿಂದ ಪ್ರಾದೇಶಿಕ ವಿವರಣೆ ಲಭ್ಯವಿಲ್ಲ. ಮುನ್ಸೂಚನೆ ಮಾದರಿ ಕಲಿತ ವೈಶಿಷ್ಟ್ಯಗಳ ಮೇಲೆ ಮಾತ್ರ ಆಧಾರಿತವಾಗಿದೆ.",
    "malayalam": "ഈ ചിത്രത്തിന് Grad-CAM ഹീറ്റ്മാപ്പ് സൃഷ്ടിക്കാൻ കഴിഞ്ഞില്ല, അതിനാൽ സ്ഥലപരമായ വിശദീകരണം ലഭ്യമല്ല. പ്രവചനം മോഡൽ പഠിച്ച സവിശേഷതകളെ മാത്രം അടിസ്ഥാനമാക്കിയുള്ളതാണ്.",
    "hindi": "इस छवि के लिए Grad-CAM हीटमैप तैयार नहीं किया जा सका, इसलिए स्थानिक व्याख्या उपलब्ध नहीं है। पूर्वानुमान केवल मॉडल की सीखी हुई विशेषताओं पर आधारित है।",
    "bengali": "এই ছবির জন্য Grad-CAM হিটম্যাপ তৈরি করা যায়নি, তাই স্থানিক ব্যাখ্যা পাওয়া যাচ্ছে না। পূর্বাভাসটি শুধুমাত্র মডেলের শেখা বৈশিষ্ট্যের উপর ভিত্তি করে তৈরি।",
    "marathi": "या प्रतिमेसाठी Grad-CAM हीटमॅप तयार करता आले नाही, त्यामुळे स्थानिक स्पष्टीकरण उपलब्ध नाही. अंदाज केवळ मॉडेलने शिकलेल्या वैशिष्ट्यांवर आधारित आहे.",
    "gujarati": "આ છબી માટે Grad-CAM હીટમેપ બનાવી શકાયું નથી, તેથી સ્થાનિક સમજૂતી ઉપલબ્ધ નથી. આગાહી ફક્ત મોડેલે શીખેલી લાક્ષણિકતાઓ પર આધારિત છે.",
    "punjabi": "ਇਸ ਤਸਵੀਰ ਲਈ Grad-CAM ਹੀਟਮੈਪ ਨਹੀਂ ਬਣਾਇਆ ਜਾ ਸਕਿਆ, ਇਸ ਲਈ ਸਥਾਨਿਕ ਵਿਆਖਿਆ ਉਪਲਬਧ ਨਹੀਂ ਹੈ। ਭਵਿੱਖਬਾਣੀ ਸਿਰਫ਼ ਮਾਡਲ ਦੀਆਂ ਸਿੱਖੀਆਂ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ 'ਤੇ ਆਧਾਰਿਤ ਹੈ।",
    "odia": "ଏହି ପ୍ରତିଛବି ପାଇଁ Grad-CAM ହିଟମ୍ୟାପ ପ୍ରସ୍ତୁତ କରାଯାଇ ପାରିଲା ନାହିଁ, ତେଣୁ ସ୍ଥାନିକ ବ୍ୟାଖ୍ୟା ଉପଲବ୍ଧ ନାହିଁ। ପୂର୍ବାନୁମାନ କେବଳ ମଡେଲର ଶିଖିଥିବା ବିଶେଷତା ଉପରେ ଆଧାରିତ।",
}
_NO_HEATMAP_SUMMARY = {
    "english": "Explainability visualisation unavailable for this prediction.",
    "tamil": "இந்த கணிப்புக்கு விளக்கக்காட்சி கிடைக்கவில்லை.",
    "telugu": "ఈ అంచనాకు వివరణాత్మక దృశ్యం అందుబాటులో లేదు.",
    "kannada": "ಈ ಮುನ್ಸೂಚನೆಗೆ ವಿವರಣಾ ದೃಶ್ಯೀಕರಣ ಲಭ್ಯವಿಲ್ಲ.",
    "malayalam": "ഈ പ്രവചനത്തിന് വിശദീകരണ ദൃശ്യാവിഷ്കാരം ലഭ്യമല്ല.",
    "hindi": "इस पूर्वानुमान के लिए व्याख्यात्मक दृश्य उपलब्ध नहीं है।",
    "bengali": "এই পূর্বাভাসের জন্য ব্যাখ্যামূলক ভিজ্যুয়ালাইজেশন উপলব্ধ নেই।",
    "marathi": "या अंदाजासाठी स्पष्टीकरणात्मक दृश्य उपलब्ध नाही.",
    "gujarati": "આ આગાહી માટે સમજૂતીત્મક વિઝ્યુલાઇઝેશન ઉપલબ્ધ નથી.",
    "punjabi": "ਇਸ ਭਵਿੱਖਬਾਣੀ ਲਈ ਵਿਆਖਿਆਤਮਕ ਦ੍ਰਿਸ਼ਟੀਕੋਣ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।",
    "odia": "ଏହି ପୂର୍ବାନୁମାନ ପାଇଁ ବ୍ୟାଖ୍ୟାତ୍ମକ ଭିଜୁଆଲାଇଜେସନ ଉପଲବ୍ଧ ନାହିଁ।",
}
_NO_HEATMAP_AG_INTERP = {
    "english": "Rely on the treatment and prevention advisory below, and confirm visually in the field.",
    "tamil": "கீழே உள்ள சிகிச்சை மற்றும் தடுப்பு ஆலோசனையை நம்பி, வயலில் நேரில் உறுதிப்படுத்தவும்.",
    "telugu": "దిగువ ఉన్న చికిత్స మరియు నివారణ సలహాను ఆధారంగా తీసుకుని, పొలంలో ప్రత్యక్షంగా నిర్ధారించుకోండి.",
    "kannada": "ಕೆಳಗಿನ ಚಿಕಿತ್ಸೆ ಮತ್ತು ತಡೆಗಟ್ಟುವಿಕೆ ಸಲಹೆಯನ್ನು ಅವಲಂಬಿಸಿ, ಹೊಲದಲ್ಲಿ ದೃಷ್ಟಿಗೋಚರವಾಗಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
    "malayalam": "താഴെയുള്ള ചികിത്സ, പ്രതിരോധ ഉപദേശം ആശ്രയിച്ച്, വയലിൽ നേരിട്ട് ഉറപ്പാക്കുക.",
    "hindi": "नीचे दी गई उपचार और रोकथाम सलाह पर भरोसा करें, और खेत में स्वयं देखकर पुष्टि करें।",
    "bengali": "নিচে দেওয়া চিকিৎসা ও প্রতিরোধ পরামর্শের উপর নির্ভর করুন এবং মাঠে চাক্ষুষ যাচাই করুন।",
    "marathi": "खालील उपचार व प्रतिबंध सल्ल्यावर अवलंबून राहा आणि शेतात प्रत्यक्ष खात्री करा.",
    "gujarati": "નીચે આપેલી સારવાર અને નિવારણ સલાહ પર આધાર રાખો, અને ખેતરમાં જાતે ખાતરી કરો.",
    "punjabi": "ਹੇਠਾਂ ਦਿੱਤੀ ਇਲਾਜ ਅਤੇ ਰੋਕਥਾਮ ਸਲਾਹ 'ਤੇ ਭਰੋਸਾ ਕਰੋ, ਅਤੇ ਖੇਤ ਵਿੱਚ ਖੁਦ ਜਾ ਕੇ ਪੁਸ਼ਟੀ ਕਰੋ।",
    "odia": "ତଳେ ଦିଆଯାଇଥିବା ଚିକିତ୍ସା ଏବଂ ପ୍ରତିରୋଧ ପରାମର୍ଶ ଉପରେ ନିର୍ଭର କରନ୍ତୁ, ଏବଂ କ୍ଷେତରେ ପ୍ରତ୍ୟକ୍ଷ ଭାବେ ନିଶ୍ଚିତ କରନ୍ତୁ।",
}


def _localized_no_heatmap_text(text_block: dict, lang: str) -> str:
    return text_block.get(lang, text_block["english"])


# ─────────────────────── PUBLIC API ─────────────────────────────
def generate_explainability_report(
    disease: str,
    confidence: float,
    heatmap: np.ndarray | None,
    severity_pct: float | None = None,
    lang: str = "english",
) -> dict:
    """
    Build the full Feature-1 explainability report, localized to `lang`.

    Parameters
    ----------
    disease      : predicted class name (e.g. "blast")
    confidence   : model confidence, 0-1
    heatmap      : Grad-CAM heatmap array (H, W), values 0-1, or None if
                   Grad-CAM was unavailable for this image.
    severity_pct : optional severity percentage already computed by
                   utils.severity.estimate_severity — included for
                   cross-reference in the summary text.
    lang         : one of utils.i18n.LANGUAGE_ORDER — every string in the
                   returned dict (labels + prose) is generated in this
                   language, mirroring how utils.severity.py and
                   utils.pdf_report.py already behave. Changing the
                   farmer's selected language and re-calling this function
                   changes the ENTIRE report, not just parts of it.

    Returns
    -------
    dict with keys:
        disease_area_pct, healthy_area_pct, infection_location,
        lesion_coverage_label, focus, confidence_interpretation,
        why_predicted, explainability_summary, agricultural_interpretation,
        available (bool — False if no heatmap was available)
    """
    lang = resolve_lang(lang)

    if heatmap is None:
        return {
            "available": False,
            "disease_area_pct": None,
            "healthy_area_pct": None,
            "infection_location": translate_enum("Unavailable", lang),
            "lesion_coverage_label": ui_text("gradcam_unavailable", lang),
            "focus": {"focus_label": translate_enum("Unavailable", lang)},
            "confidence_interpretation": confidence_interpretation_text(
                confidence, "Unavailable", lang
            ),
            "why_predicted": _localized_no_heatmap_text(_NO_HEATMAP_WHY, lang),
            "explainability_summary": _localized_no_heatmap_text(_NO_HEATMAP_SUMMARY, lang),
            "agricultural_interpretation": _localized_no_heatmap_text(_NO_HEATMAP_AG_INTERP, lang),
        }

    shares = _region_shares(heatmap)
    location_key = _infection_location(shares)
    disease_pct, healthy_pct = _disease_healthy_area(heatmap)
    coverage_key = _lesion_coverage_label(disease_pct)
    focus = _heatmap_focus(heatmap)
    focus_key = focus["focus_label"]

    conf_interp = confidence_interpretation_text(confidence, focus_key, lang)
    why = why_predicted_text(disease, location_key, coverage_key, focus_key, lang)
    summary = explainability_summary_text(
        disease, disease_pct, healthy_pct, location_key, coverage_key, conf_interp, lang
    )
    ag_interp = agricultural_interpretation_text(disease, location_key, disease_pct, lang)

    return {
        "available": True,
        "disease_area_pct": disease_pct,
        "healthy_area_pct": healthy_pct,
        "infection_location": translate_enum(location_key, lang),
        "lesion_coverage_label": translate_enum(coverage_key, lang),
        "focus": {**focus, "focus_label": translate_enum(focus_key, lang)},
        "confidence_interpretation": conf_interp,
        "why_predicted": why,
        "explainability_summary": summary,
        "agricultural_interpretation": ag_interp,
    }
