"""
utils/i18n.py — Smart Paddy AI: Central Multilingual (i18n) Hub
Place at: smart_paddy_ai/utils/i18n.py

Single source of truth for every language-dependent string used outside
the disease advisory content itself (which lives in utils/advisory.py).

Supported languages (dropdown order, English is default):
    Tamil, Telugu, Kannada, Malayalam, Hindi, Bengali, Marathi,
    Gujarati, Punjabi, Odia, English
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════
# LANGUAGE REGISTRY
# ═══════════════════════════════════════════════════════════════
# Internal keys are stable strings used everywhere in the codebase
# (session state, function args, dict lookups). Do not rename these —
# UI order and native names are handled separately below.
LANGUAGE_ORDER = [
    "tamil", "telugu", "kannada", "malayalam", "hindi",
    "bengali", "marathi", "gujarati", "punjabi", "odia", "english",
]

DEFAULT_LANGUAGE = "english"

NATIVE_NAMES = {
    "tamil":     "தமிழ்",
    "telugu":    "తెలుగు",
    "kannada":   "ಕನ್ನಡ",
    "malayalam": "മലയാളം",
    "hindi":     "हिन्दी",
    "bengali":   "বাংলা",
    "marathi":   "मराठी",
    "gujarati":  "ગુજરાતી",
    "punjabi":   "ਪੰਜਾਬੀ",
    "odia":      "ଓଡ଼ିଆ",
    "english":   "English",
}

# gTTS language codes (per requirement)
TTS_LANG_CODES = {
    "tamil":     "ta",
    "telugu":    "te",
    "kannada":   "kn",
    "malayalam": "ml",
    "hindi":     "hi",
    "bengali":   "bn",
    "marathi":   "mr",
    "gujarati":  "gu",
    "punjabi":   "pa",
    "odia":      "or",
    "english":   "en",
}


def language_select_options() -> list[str]:
    """Ordered list of language keys for the dropdown, English last (default)."""
    return LANGUAGE_ORDER


def native_name(lang: str) -> str:
    return NATIVE_NAMES.get(lang, lang.title())


def tts_code(lang: str) -> str:
    return TTS_LANG_CODES.get(lang, "en")


def resolve_lang(lang: str) -> str:
    """Normalise/validate a language key, falling back to English."""
    lang = (lang or "").lower().strip()
    return lang if lang in NATIVE_NAMES else DEFAULT_LANGUAGE


# ═══════════════════════════════════════════════════════════════
# LOCAL-ONLY TRANSLATION LOOKUP (NO API CALLS)
# ═══════════════════════════════════════════════════════════════
# Many of the small per-string dicts below only have hand-written copy
# for a subset of the 11 languages (English + whichever language was
# authored first for that string). If `lang` isn't hand-written for a
# given string, _pick()/_pick_or() fall back to the English entry — they
# NEVER call an external translation API (Gemini is reserved exclusively
# for the chatbot; see utils/ai_expert.py). This keeps every language
# switch instant and fully offline, at the cost of showing English for
# any string that hasn't been hand-translated yet.


def _pick(block: dict, lang: str) -> str:
    """Look up `lang` in `block`; fall back to the English entry if missing."""
    if lang in block:
        return block[lang]
    return block.get("english", "")


def _pick_or(block: dict, lang: str, default: str) -> str:
    """Like _pick(), but falls back to `default` when there's no English entry either."""
    if lang in block:
        return block[lang]
    return block.get("english", default)


# ═══════════════════════════════════════════════════════════════
# DISEASE DISPLAY NAMES (translated, used for headers/results)
# ═══════════════════════════════════════════════════════════════
DISEASE_NAMES = {
    "blast": {
        "english": "Blast", "tamil": "பிளாஸ்ட்", "telugu": "బ్లాస్ట్", "kannada": "ಬ್ಲಾಸ್ಟ್",
        "malayalam": "ബ്ലാസ്റ്റ്", "hindi": "ब्लास्ट (झुलसा)", "bengali": "ব্লাস্ট রোগ",
        "marathi": "ब्लास्ट (करपा)", "gujarati": "બ્લાસ્ટ રોગ", "punjabi": "ਬਲਾਸਟ ਰੋਗ", "odia": "ବ୍ଲାଷ୍ଟ ରୋଗ",
    },
    "brown_spot": {
        "english": "Brown Spot", "tamil": "பழுப்பு புள்ளி நோய்", "telugu": "గోధుమ మచ్చ తెగులు",
        "kannada": "ಕಂದು ಚುಕ್ಕೆ ರೋಗ", "malayalam": "തവിട്ട് പുള്ളി രോഗം", "hindi": "भूरा धब्बा रोग",
        "bengali": "বাদামী দাগ রোগ", "marathi": "तपकिरी ठिपका रोग", "gujarati": "બ્રાઉન સ્પોટ રોગ",
        "punjabi": "ਭੂਰਾ ਦਾਗ਼ ਰੋਗ", "odia": "ବାଦାମୀ ଦାଗ ରୋଗ",
    },
    "tungro": {
        "english": "Tungro", "tamil": "டங்க்ரோ நோய்", "telugu": "టుంగ్రో వ్యాధి", "kannada": "ಟುಂಗ್ರೊ ರೋಗ",
        "malayalam": "ടുങ്ട്രോ രോഗം", "hindi": "टुंग्रो रोग", "bengali": "টুংগ্রো রোগ",
        "marathi": "टुंग्रो रोग", "gujarati": "ટુંગ્રો રોગ", "punjabi": "ਟੁੰਗਰੋ ਰੋਗ", "odia": "ଟୁଙ୍ଗ୍ରୋ ରୋଗ",
    },
    "bacterial_panicle_blight": {
        "english": "Bacterial Panicle Blight", "tamil": "பாக்டீரியல் பேனிக்கல் பிளைட்",
        "telugu": "బాక్టీరియల్ పానికిల్ బ్లైట్", "kannada": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಪ್ಯಾನಿಕಲ್ ಬ್ಲೈಟ್",
        "malayalam": "ബാക്ടീരിയൽ പാനിക്കിൾ ബ്ലൈറ്റ്", "hindi": "बैक्टीरियल पैनिकल ब्लाइट",
        "bengali": "ব্যাকটেরিয়াল প্যানিকল ব্লাইট", "marathi": "बॅक्टेरियल पॅनिकल ब्लाइट",
        "gujarati": "બેક્ટેરિયલ પેનિકલ બ્લાઇટ", "punjabi": "ਬੈਕਟੀਰੀਅਲ ਪੈਨਿਕਲ ਬਲਾਈਟ",
        "odia": "ବ୍ୟାକ୍ଟେରିଆଲ ପାନିକଲ ବ୍ଲାଇଟ",
    },
    "bacterial_leaf_blight": {
        "english": "Bacterial Leaf Blight", "tamil": "பாக்டீரியல் இலை அழுகல்",
        "telugu": "బాక్టీరియల్ ఆకు ఎండు తెగులు", "kannada": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಎಲೆ ಅಂಗಮಾರಿ",
        "malayalam": "ബാക്ടീരിയൽ ഇല കരിച്ചിൽ", "hindi": "बैक्टीरियल पत्ती झुलसा",
        "bengali": "ব্যাকটেরিয়াল পাতা ব্লাইট", "marathi": "बॅक्टेरियल पान करपा",
        "gujarati": "બેક્ટેરિયલ પર્ણ સુકારો", "punjabi": "ਬੈਕਟੀਰੀਅਲ ਪੱਤਾ ਝੁਲਸ",
        "odia": "ବ୍ୟାକ୍ଟେରିଆଲ ପତ୍ର ମଡ଼ା ରୋଗ",
    },
    "bacterial_leaf_streak": {
        "english": "Bacterial Leaf Streak", "tamil": "பாக்டீரியல் இலை கோடு நோய்",
        "telugu": "బాక్టీరియల్ ఆకు చారల తెగులు", "kannada": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಎಲೆ ಪಟ್ಟಿ ರೋಗ",
        "malayalam": "ബാക്ടീരിയൽ ഇല വരപ്പ് രോഗം", "hindi": "बैक्टीरियल पत्ती धारी रोग",
        "bengali": "ব্যাকটেরিয়াল পাতা রেখা রোগ", "marathi": "बॅक्टेरियल पान पट्टी रोग",
        "gujarati": "બેક્ટેરિયલ પર્ણ પટ્ટી રોગ", "punjabi": "ਬੈਕਟੀਰੀਅਲ ਪੱਤਾ ਧਾਰੀ ਰੋਗ",
        "odia": "ବ୍ୟାକ୍ଟେରିଆଲ ପତ୍ର ଧାରି ରୋଗ",
    },
    "dead_heart": {
        "english": "Dead Heart", "tamil": "டெட் ஹார்ட் (தண்டு துளைப்பான்)", "telugu": "డెడ్ హార్ట్ (కాండం తొలుచు పురుగు)",
        "kannada": "ಡೆಡ್ ಹಾರ್ಟ್ (ಕಾಂಡ ಕೊರಕ)", "malayalam": "ഡെഡ് ഹാർട്ട് (തണ്ട് തുരപ്പൻ)",
        "hindi": "डेड हार्ट (तना छेदक)", "bengali": "ডেড হার্ট (কাণ্ড ছিদ্রকারী পোকা)",
        "marathi": "डेड हार्ट (खोड किडा)", "gujarati": "ડેડ હાર્ટ (દાંડી કોરી ખાનાર જીવાત)",
        "punjabi": "ਡੈੱਡ ਹਾਰਟ (ਤਣਾ ਛੇਦਕ)", "odia": "ଡେଡ ହାର୍ଟ (କାଣ୍ଡ ପୋକ)",
    },
    "hispa": {
        "english": "Hispa", "tamil": "ஹிஸ்பா", "telugu": "హిస్పా పురుగు", "kannada": "ಹಿಸ್ಪಾ ಕೀಟ",
        "malayalam": "ഹിസ്പ", "hindi": "हिस्पा कीट", "bengali": "হিসপা পোকা", "marathi": "हिस्पा किड",
        "gujarati": "હિસ્પા જીવાત", "punjabi": "ਹਿਸਪਾ ਕੀੜਾ", "odia": "ହିସ୍ପା ପୋକ",
    },
    "downy_mildew": {
        "english": "Downy Mildew", "tamil": "டவுனி மில்டியூ", "telugu": "డౌనీ మిల్డ్యూ",
        "kannada": "ಡೌನಿ ಮಿಲ್ಡ್ಯೂ", "malayalam": "ഡൌണി മിൽഡ്യൂ", "hindi": "डाउनी मिल्ड्यू",
        "bengali": "ডাউনি মিলডিউ", "marathi": "डाउनी मिल्ड्यू", "gujarati": "ડાઉની માઇલ્ડ્યુ",
        "punjabi": "ਡਾਊਨੀ ਮਿਲਡਿਊ", "odia": "ଡାଉନି ମିଲଡିଉ",
    },
    "normal": {
        "english": "Healthy", "tamil": "ஆரோக்கியமானது", "telugu": "ఆరోగ్యంగా ఉంది",
        "kannada": "ಆರೋಗ್ಯಕರ", "malayalam": "ആരോഗ്യമുള്ളത്", "hindi": "स्वस्थ",
        "bengali": "সুস্থ", "marathi": "निरोगी", "gujarati": "તંદુરસ્ત", "punjabi": "ਤੰਦਰੁਸਤ", "odia": "ସୁସ୍ଥ",
    },
    "healthy": {
        "english": "Healthy", "tamil": "ஆரோக்கியமானது", "telugu": "ఆరోగ్యంగా ఉంది",
        "kannada": "ಆರೋಗ್ಯಕರ", "malayalam": "ആരോഗ്യമുള്ളത്", "hindi": "स्वस्थ",
        "bengali": "সুস্থ", "marathi": "निरोगी", "gujarati": "તંદુરસ્ત", "punjabi": "ਤੰਦਰੁਸਤ", "odia": "ସୁସ୍ଥ",
    },
}


def disease_display_name(disease_key: str, lang: str) -> str:
    """Translated disease name; falls back to a Title-Case English guess."""
    lang = resolve_lang(lang)
    key = disease_key.lower().strip()
    block = DISEASE_NAMES.get(key)
    if block is None:
        return disease_key.replace("_", " ").title()
    return _pick(block, lang)


# ═══════════════════════════════════════════════════════════════
# UI LABELS
# ═══════════════════════════════════════════════════════════════
# Every key below MUST exist for every language in LANGUAGE_ORDER + "english".
_UI_RAW = {
    # Research Metrics page — comparison table column headers
    # (app.py: existing-vs-proposed metrics table). Hand-written for
    # every language below; any language not yet added here falls back
    # to English via _pick() — local dictionary only, no API calls.
    "col_metric": {"english": "Metric", "tamil": "அளவீடு", "telugu": "మెట్రిక్", "kannada": "ಮೆಟ್ರಿಕ್",
                   "malayalam": "മെട്രിക്", "hindi": "मेट्रिक", "bengali": "মেট্রিক", "marathi": "मेट्रिक",
                   "gujarati": "મેટ્રિક", "punjabi": "ਮੈਟ੍ਰਿਕ", "odia": "ମେଟ୍ରିକ"},
    "col_existing_system_pct": {"english": "Existing System (%)", "tamil": "தற்போதைய முறை (%)",
                   "telugu": "ప్రస్తుత విధానం (%)", "kannada": "ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ವ್ಯವಸ್ಥೆ (%)",
                   "malayalam": "നിലവിലെ സംവിധാനം (%)", "hindi": "मौजूदा प्रणाली (%)",
                   "bengali": "বিদ্যমান ব্যবস্থা (%)", "marathi": "सध्याची प्रणाली (%)",
                   "gujarati": "હાલની સિસ્ટમ (%)", "punjabi": "ਮੌਜੂਦਾ ਸਿਸਟਮ (%)", "odia": "ବର୍ତ୍ତମାନ ପ୍ରଣାଳୀ (%)"},
    "col_proposed_system_pct": {"english": "Smart Paddy AI (%)", "tamil": "ஸ்மார்ட் பேடி AI (%)",
                   "telugu": "స్మార్ట్ పాడీ AI (%)", "kannada": "ಸ್ಮಾರ್ಟ್ ಪ್ಯಾಡಿ AI (%)",
                   "malayalam": "സ്മാർട്ട് പാഡി AI (%)", "hindi": "स्मार्ट पैडी AI (%)",
                   "bengali": "স্মার্ট প্যাডি AI (%)", "marathi": "स्मार्ट पॅडी AI (%)",
                   "gujarati": "સ્માર્ટ પેડી AI (%)", "punjabi": "ਸਮਾਰਟ ਪੈਡੀ AI (%)", "odia": "ସ୍ମାର୍ଟ ପେଡି AI (%)"},
    "col_improvement_pct": {"english": "Improvement (%)", "tamil": "முன்னேற்றம் (%)",
                   "telugu": "మెరుగుదల (%)", "kannada": "ಸುಧಾರಣೆ (%)", "malayalam": "മെച്ചപ്പെടുത്തൽ (%)",
                   "hindi": "सुधार (%)", "bengali": "উন্নতি (%)", "marathi": "सुधारणा (%)",
                   "gujarati": "સુધારો (%)", "punjabi": "ਸੁਧਾਰ (%)", "odia": "ଉନ୍ନତି (%)"},

    # ── Diagnosis page: upload placeholder / download button ──────
    "supports_formats_caption": {
        "english": "Supports JPG and PNG formats — upload a clear photo of a paddy leaf to begin.",
    },
    "pdf_click_save_btn": {"english": "📥 Download PDF Report"},

    # ── Diagnosis page: Enhanced Crop Health Intelligence Dashboard ─
    "enhanced_crop_health_header": {"english": "🩺 Enhanced Crop Health Intelligence"},
    "disease_risk_label": {"english": "Disease Risk"},
    "ai_confidence_meter_label": {"english": "AI Confidence Meter"},
    "severity_health_overview_header": {"english": "Severity & Health Overview"},
    "severity_pct_axis_label": {"english": "Severity (%)"},
    "health_index_axis_label": {"english": "Crop Health Index"},

    # ── Diagnosis page: treatment effectiveness table ──────────────
    "treatment_effectiveness_header": {"english": "Treatment Effectiveness"},
    "treatment_col_option": {"english": "Treatment Option"},
    "treatment_col_priority": {"english": "Priority"},
    "treatment_col_success_rate": {"english": "Success Rate"},
    "treatment_col_recovery_time": {"english": "Recovery Time (days)"},
    "treatment_col_cost": {"english": "Cost"},
    "treatment_col_eco_friendly": {"english": "Eco-Friendly"},
    "treatment_col_best_stage": {"english": "Best Applied At Stage"},

    # ── Model Performance page: header / capability comparison ─────
    "model_performance_title": {"english": "Model Performance"},
    "model_performance_subtitle": {
        "english": "Research-oriented metrics comparing Smart Paddy AI against a conventional baseline system.",
    },
    "model_performance_caption": {
        "english": "For academic and research reference only — figures below combine measured evaluation results with conceptual design-rationale comparisons.",
    },
    "capability_comparison_subtitle": {
        "english": "A conceptual, design-rationale comparison of architectural capabilities — not measured accuracy results.",
    },
    "capability_score_axis": {"english": "Capability Score (1–5)"},
    "capability_chart_caption": {
        "english": "Scores reflect known architectural properties (depth, compound scaling, parameter efficiency, transfer learning) used to justify the choice of EfficientNetB0, not experimental results from a held-out test set.",
    },
    "verdict_box_html": {
        "english": "<b>Verdict:</b> EfficientNetB0 offers the strongest balance of feature-extraction depth, parameter efficiency, transfer-learning capability, training speed, and generalization ability — making it the most suitable backbone for Smart Paddy AI's disease-classification task.",
    },

    # ── Model Performance page: existing vs proposed metrics table ─
    "existing_vs_proposed_subtitle": {
        "english": "How Smart Paddy AI's measured evaluation metrics compare against a conventional existing system.",
    },
    "conclusion_box_template": {
        "english": (
            "<b>Conclusion:</b> Smart Paddy AI achieves an average improvement of "
            "<b>{gain:.1f} percentage points</b> over the existing system "
            "(proposed avg: {proposed:.1f}% vs existing avg: {existing:.1f}%)."
        ),
    },

    # ── Analytics page: summary stat cards ──────────────────────────
    "total_scans_label": {"english": "Total Scans"},
    "most_common_disease_label": {"english": "Most Common Disease"},
    "avg_confidence_label": {"english": "Average Confidence"},
    "avg_health_index_label": {"english": "Average Health Index"},

    # ── Analytics page: charts & tables ──────────────────────────────
    "disease_distribution_header": {"english": "Disease Distribution"},
    "scan_count_by_disease_header": {"english": "Scan Count by Disease"},
    "col_disease": {"english": "Disease"},
    "col_count": {"english": "Count"},
    "monthly_scan_trends_header": {"english": "Monthly Scan Trends"},
    "month_axis_label": {"english": "Month"},
    "scans_axis_label": {"english": "Number of Scans"},
    "severity_distribution_header": {"english": "Severity Distribution"},
    "recent_predictions_header": {"english": "Recent Predictions"},
    "col_timestamp": {"english": "Timestamp"},
    "col_confidence": {"english": "Confidence"},
    "col_severity": {"english": "Severity"},
    "col_health_index": {"english": "Health Index"},

    "title": {
        "english": "Smart Paddy AI", "tamil": "ஸ்மார்ட் பேடி AI", "telugu": "స్మార్ట్ పాడీ AI",
        "kannada": "ಸ್ಮಾರ್ಟ್ ಪ್ಯಾಡಿ AI", "malayalam": "സ്മാർട്ട് പാഡി AI", "hindi": "स्मार्ट पैडी AI",
        "bengali": "স্মার্ট প্যাডি AI", "marathi": "स्मार्ट पॅडी AI", "gujarati": "સ્માર્ટ પેડી AI",
        "punjabi": "ਸਮਾਰਟ ਪੈਡੀ AI", "odia": "ସ୍ମାର୍ଟ ପେଡି AI",
    },
    "subtitle": {
        "english": "Rice Disease Detection & Agricultural Decision Support",
        "tamil": "நெல் நோய் கண்டறிதல் மற்றும் விவசாய ஆலோசனை",
        "telugu": "వరి వ్యాధి గుర్తింపు మరియు వ్యవసాయ నిర్ణయ మద్దతు",
        "kannada": "ಭತ್ತದ ರೋಗ ಪತ್ತೆ ಮತ್ತು ಕೃಷಿ ನಿರ್ಧಾರ ಬೆಂಬಲ",
        "malayalam": "നെല്ല് രോഗ കണ്ടെത്തലും കാർഷിക തീരുമാന പിന്തുണയും",
        "hindi": "धान रोग पहचान एवं कृषि निर्णय सहायता",
        "bengali": "ধান রোগ সনাক্তকরণ ও কৃষি সিদ্ধান্ত সহায়তা",
        "marathi": "भात रोग ओळख आणि कृषी निर्णय सहाय्य",
        "gujarati": "ડાંગર રોગ ઓળખ અને કૃષિ નિર્ણય સહાય",
        "punjabi": "ਝੋਨੇ ਦੀ ਬਿਮਾਰੀ ਪਛਾਣ ਅਤੇ ਖੇਤੀ ਫੈਸਲਾ ਸਹਾਇਤਾ",
        "odia": "ଧାନ ରୋଗ ଚିହ୍ନଟ ଏବଂ କୃଷି ନିଷ୍ପତ୍ତି ସହାୟତା",
    },
    "upload": {
        "english": "Upload Paddy Leaf Image", "tamil": "நெல் இலை படம் பதிவேற்றவும்",
        "telugu": "వరి ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి", "kannada": "ಭತ್ತದ ಎಲೆ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "malayalam": "നെല്ല് ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക", "hindi": "धान की पत्ती की तस्वीर अपलोड करें",
        "bengali": "ধানের পাতার ছবি আপলোড করুন", "marathi": "भाताच्या पानाचा फोटो अपलोड करा",
        "gujarati": "ડાંગરના પાનનો ફોટો અપલોડ કરો", "punjabi": "ਝੋਨੇ ਦੇ ਪੱਤੇ ਦੀ ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ",
        "odia": "ଧାନ ପତ୍ରର ଛବି ଅପଲୋଡ କରନ୍ତୁ",
    },
    "detected": {
        "english": "Detected Disease", "tamil": "கண்டறியப்பட்ட நோய்", "telugu": "గుర్తించిన వ్యాధి",
        "kannada": "ಪತ್ತೆಯಾದ ರೋಗ", "malayalam": "കണ്ടെത്തിയ രോഗം", "hindi": "पहचानी गई बीमारी",
        "bengali": "শনাক্ত রোগ", "marathi": "ओळखलेला रोग", "gujarati": "શોધાયેલ રોગ",
        "punjabi": "ਪਛਾਣੀ ਗਈ ਬਿਮਾਰੀ", "odia": "ଚିହ୍ନଟ ହୋଇଥିବା ରୋଗ",
    },
    "confidence": {
        "english": "Model Confidence", "tamil": "மாதிரி நம்பகத்தன்மை", "telugu": "మోడల్ నమ్మకత్వం",
        "kannada": "ಮಾಡೆಲ್ ವಿಶ್ವಾಸಾರ್ಹತೆ", "malayalam": "മോഡൽ വിശ്വാസ്യത", "hindi": "मॉडल विश्वास स्तर",
        "bengali": "মডেল আত্মবিশ্বাস", "marathi": "मॉडेल विश्वासार्हता", "gujarati": "મોડેલ વિશ્વસનીયતા",
        "punjabi": "ਮਾਡਲ ਭਰੋਸੇਯੋਗਤਾ", "odia": "ମଡେଲ ବିଶ୍ୱାସନୀୟତା",
    },
    "severity": {
        "english": "Severity", "tamil": "தீவிரம்", "telugu": "తీవ్రత", "kannada": "ತೀವ್ರತೆ",
        "malayalam": "തീവ്രത", "hindi": "गंभीरता", "bengali": "তীব্রতা", "marathi": "तीव्रता",
        "gujarati": "તીવ્રતા", "punjabi": "ਗੰਭੀਰਤਾ", "odia": "ତୀବ୍ରତା",
    },
    "health": {
        "english": "Crop Health Index", "tamil": "பயிர் ஆரோக்கிய குறியீடு", "telugu": "పంట ఆరోగ్య సూచిక",
        "kannada": "ಬೆಳೆ ಆರೋಗ್ಯ ಸೂಚ್ಯಂಕ", "malayalam": "വിള ആരോഗ്യ സൂചിക", "hindi": "फसल स्वास्थ्य सूचकांक",
        "bengali": "ফসল স্বাস্থ্য সূচক", "marathi": "पीक आरोग्य निर्देशांक", "gujarati": "પાક આરોગ્ય સૂચકાંક",
        "punjabi": "ਫਸਲ ਸਿਹਤ ਸੂਚਕਾਂਕ", "odia": "ଫସଲ ସ୍ୱାସ୍ଥ୍ୟ ସୂଚକାଙ୍କ",
    },
    "risk": {
        "english": "Risk Level", "tamil": "அபாய நிலை", "telugu": "ప్రమాద స్థాయి", "kannada": "ಅಪಾಯ ಮಟ್ಟ",
        "malayalam": "അപകട നില", "hindi": "जोखिम स्तर", "bengali": "ঝুঁকির মাত্রা", "marathi": "धोक्याची पातळी",
        "gujarati": "જોખમ સ્તર", "punjabi": "ਜੋਖਮ ਪੱਧਰ", "odia": "ବିପଦ ସ୍ତର",
    },
    "advisory": {
        "english": "Agricultural Advisory", "tamil": "விவசாய ஆலோசனை", "telugu": "వ్యవసాయ సలహా",
        "kannada": "ಕೃಷಿ ಸಲಹೆ", "malayalam": "കാർഷിക ഉപദേശം", "hindi": "कृषि सलाह",
        "bengali": "কৃষি পরামর্শ", "marathi": "कृषी सल्ला", "gujarati": "કૃષિ સલાહ",
        "punjabi": "ਖੇਤੀ ਸਲਾਹ", "odia": "କୃଷି ପରାମର୍ଶ",
    },
    "treatment": {
        "english": "Treatment", "tamil": "சிகிச்சை", "telugu": "చికిత్స", "kannada": "ಚಿಕಿತ್ಸೆ",
        "malayalam": "ചികിത്സ", "hindi": "उपचार", "bengali": "চিকিৎসা", "marathi": "उपचार",
        "gujarati": "સારવાર", "punjabi": "ਇਲਾਜ", "odia": "ଚିକିତ୍ସା",
    },
    "prevention": {
        "english": "Prevention", "tamil": "தடுப்பு", "telugu": "నివారణ", "kannada": "ತಡೆಗಟ್ಟುವಿಕೆ",
        "malayalam": "പ്രതിരോധം", "hindi": "रोकथाम", "bengali": "প্রতিরোধ", "marathi": "प्रतिबंध",
        "gujarati": "નિવારણ", "punjabi": "ਰੋਕਥਾਮ", "odia": "ପ୍ରତିରୋଧ",
    },
    "fertilizer": {
        "english": "Fertilizer", "tamil": "உரம்", "telugu": "ఎరువు", "kannada": "ಗೊಬ್ಬರ",
        "malayalam": "വളം", "hindi": "उर्वरक", "bengali": "সার", "marathi": "खत",
        "gujarati": "ખાતર", "punjabi": "ਖਾਦ", "odia": "ସାର",
    },
    "irrigation": {
        "english": "Irrigation", "tamil": "நீர்ப்பாசனம்", "telugu": "నీటిపారుదల", "kannada": "ನೀರಾವರಿ",
        "malayalam": "ജലസേചനം", "hindi": "सिंचाई", "bengali": "সেচ", "marathi": "सिंचन",
        "gujarati": "સિંચાઈ", "punjabi": "ਸਿੰਚਾਈ", "odia": "ଜଳସେଚନ",
    },
    "chatbot": {
        "english": "Farming Assistant", "tamil": "விவசாய உதவியாளர்", "telugu": "వ్యవసాయ సహాయకుడు",
        "kannada": "ಕೃಷಿ ಸಹಾಯಕ", "malayalam": "കാർഷിക സഹായി", "hindi": "कृषि सहायक",
        "bengali": "কৃষি সহায়ক", "marathi": "शेती सहाय्यक", "gujarati": "ખેતી સહાયક",
        "punjabi": "ਖੇਤੀ ਸਹਾਇਕ", "odia": "କୃଷି ସହାୟକ",
    },
    "analytics": {
        "english": "Analytics Dashboard", "tamil": "ஆய்வு டாஷ்போர்டு", "telugu": "విశ్లేషణ డాష్‌బోర్డ్",
        "kannada": "ವಿಶ್ಲೇಷಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್", "malayalam": "അനലിറ്റിക്സ് ഡാഷ്‌ബോർഡ്",
        "hindi": "विश्लेषण डैशबोर्ड", "bengali": "অ্যানালিটিক্স ড্যাশবোর্ড", "marathi": "विश्लेषण डॅशबोर्ड",
        "gujarati": "એનાલિટિક્સ ડેશબોર્ડ", "punjabi": "ਵਿਸ਼ਲੇਸ਼ਣ ਡੈਸ਼ਬੋਰਡ", "odia": "ବିଶ୍ଳେଷଣ ଡ୍ୟାସବୋର୍ଡ",
    },
    "research": {
        "english": "Research Metrics", "tamil": "ஆராய்ச்சி அளவீடுகள்", "telugu": "పరిశోధన కొలమానాలు",
        "kannada": "ಸಂಶೋಧನಾ ಮಾಪನಗಳು", "malayalam": "ഗവേഷണ അളവുകൾ", "hindi": "शोध मेट्रिक्स",
        "bengali": "গবেষণা মেট্রিক্স", "marathi": "संशोधन मेट्रिक्स", "gujarati": "સંશોધન મેટ્રિક્સ",
        "punjabi": "ਖੋਜ ਮੈਟ੍ਰਿਕਸ", "odia": "ଗବେଷଣା ମେଟ୍ରିକ୍ସ",
    },
    "listen": {
        "english": "Listen to Advisory", "tamil": "ஆலோசனையை கேளுங்கள்", "telugu": "సలహాను వినండి",
        "kannada": "ಸಲಹೆಯನ್ನು ಆಲಿಸಿ", "malayalam": "ഉപദേശം കേൾക്കുക", "hindi": "सलाह सुनें",
        "bengali": "পরামর্শ শুনুন", "marathi": "सल्ला ऐका", "gujarati": "સલાહ સાંભળો",
        "punjabi": "ਸਲਾਹ ਸੁਣੋ", "odia": "ପରାମର୍ଶ ଶୁଣନ୍ତୁ",
    },
    "download_pdf": {
        "english": "Download PDF Report", "tamil": "PDF அறிக்கை பதிவிறக்கம்", "telugu": "PDF నివేదికను డౌన్‌లోడ్ చేయండి",
        "kannada": "PDF ವರದಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ", "malayalam": "PDF റിപ്പോർട്ട് ഡൗൺലോഡ് ചെയ്യുക",
        "hindi": "PDF रिपोर्ट डाउनलोड करें", "bengali": "PDF রিপোর্ট ডাউনলোড করুন", "marathi": "PDF अहवाल डाउनलोड करा",
        "gujarati": "PDF રિપોર્ટ ડાઉનલોડ કરો", "punjabi": "PDF ਰਿਪੋਰਟ ਡਾਊਨਲੋਡ ਕਰੋ", "odia": "PDF ରିପୋର୍ଟ ଡାଉନଲୋଡ କରନ୍ତୁ",
    },
    "all_conf": {
        "english": "All Class Probabilities", "tamil": "அனைத்து வகை நிகழ்தகவுகள்", "telugu": "అన్ని తరగతుల సంభావ్యతలు",
        "kannada": "ಎಲ್ಲಾ ವರ್ಗಗಳ ಸಂಭವನೀಯತೆ", "malayalam": "എല്ലാ ക്ലാസ് സാധ്യതകളും", "hindi": "सभी वर्गों की संभावना",
        "bengali": "সমস্ত শ্রেণির সম্ভাবনা", "marathi": "सर्व वर्गांची संभाव्यता", "gujarati": "તમામ વર્ગોની સંભાવના",
        "punjabi": "ਸਾਰੀਆਂ ਸ਼੍ਰੇਣੀਆਂ ਦੀ ਸੰਭਾਵਨਾ", "odia": "ସମସ୍ତ ଶ୍ରେଣୀର ସମ୍ଭାବନା",
    },
    "gradcam": {
        "english": "Grad-CAM Explainability", "tamil": "தொற்று பகுதி வரைபடம்", "telugu": "గ్రాడ్-కామ్ వివరణ",
        "kannada": "ಗ್ರ್ಯಾಡ್-ಕ್ಯಾಮ್ ವಿವರಣೆ", "malayalam": "ഗ്രാഡ്-ക്യാം വിശദീകരണം", "hindi": "ग्रैड-कैम व्याख्या",
        "bengali": "গ্র্যাড-ক্যাম ব্যাখ্যা", "marathi": "ग्रॅड-कॅम स्पष्टीकरण", "gujarati": "ગ્રેડ-કેમ સમજૂતી",
        "punjabi": "ਗ੍ਰੈਡ-ਕੈਮ ਵਿਆਖਿਆ", "odia": "ଗ୍ରାଡ-କ୍ୟାମ ବ୍ୟାଖ୍ୟା",
    },
    "orig": {
        "english": "Original Image", "tamil": "அசல் படம்", "telugu": "అసలు చిత్రం", "kannada": "ಮೂಲ ಚಿತ್ರ",
        "malayalam": "യഥാർത്ഥ ചിത്രം", "hindi": "मूल तस्वीर", "bengali": "মূল ছবি", "marathi": "मूळ प्रतिमा",
        "gujarati": "મૂળ છબી", "punjabi": "ਮੂਲ ਤਸਵੀਰ", "odia": "ମୂଳ ଛବି",
    },
    "heatmap": {
        "english": "Infected Region Heatmap", "tamil": "தொற்று பகுதி வரைபடம்", "telugu": "వ్యాధి ప్రాంత హీట్‌మ్యాప్",
        "kannada": "ಸೋಂಕಿತ ಪ್ರದೇಶ ಹೀಟ್‌ಮ್ಯಾಪ್", "malayalam": "രോഗബാധിത ഭാഗ ഹീറ്റ്മാപ്പ്",
        "hindi": "संक्रमित क्षेत्र हीटमैप", "bengali": "আক্রান্ত অঞ্চল হিটম্যাপ", "marathi": "संक्रमित भाग हीटमॅप",
        "gujarati": "ચેપગ્રસ્ત વિસ્તાર હીટમેપ", "punjabi": "ਲਾਗ ਵਾਲਾ ਖੇਤਰ ਹੀਟਮੈਪ", "odia": "ସଂକ୍ରମିତ ଅଞ୍ଚଳ ହିଟମ୍ୟାପ",
    },
    "download_cam": {
        "english": "Download Heatmap", "tamil": "வரைபடம் பதிவிறக்கம்", "telugu": "హీట్‌మ్యాప్ డౌన్‌లోడ్",
        "kannada": "ಹೀಟ್‌ಮ್ಯಾಪ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ", "malayalam": "ഹീറ്റ്മാപ്പ് ഡൗൺലോഡ് ചെയ്യുക",
        "hindi": "हीटमैप डाउनलोड करें", "bengali": "হিটম্যাপ ডাউনলোড করুন", "marathi": "हीटमॅप डाउनलोड करा",
        "gujarati": "હીટમેપ ડાઉનલોડ કરો", "punjabi": "ਹੀਟਮੈਪ ਡਾਊਨਲੋਡ ਕਰੋ", "odia": "ହିଟମ୍ୟାପ ଡାଉନଲୋଡ କରନ୍ତୁ",
    },
    "ask": {
        "english": "Ask the AI assistant...", "tamil": "AI உதவியாளரிடம் கேளுங்கள்...", "telugu": "AI సహాయకుడిని అడగండి...",
        "kannada": "AI ಸಹಾಯಕರನ್ನು ಕೇಳಿ...", "malayalam": "AI സഹായിയോട് ചോദിക്കൂ...", "hindi": "AI सहायक से पूछें...",
        "bengali": "AI সহায়ককে জিজ্ঞাসা করুন...", "marathi": "AI सहाय्यकाला विचारा...",
        "gujarati": "AI સહાયકને પૂછો...", "punjabi": "AI ਸਹਾਇਕ ਨੂੰ ਪੁੱਛੋ...", "odia": "AI ସହାୟକଙ୍କୁ ପଚାରନ୍ତୁ...",
    },
    "send": {
        "english": "Send", "tamil": "அனுப்பு", "telugu": "పంపండి", "kannada": "ಕಳುಹಿಸಿ", "malayalam": "അയക്കുക",
        "hindi": "भेजें", "bengali": "পাঠান", "marathi": "पाठवा", "gujarati": "મોકલો", "punjabi": "ਭੇਜੋ", "odia": "ପଠାନ୍ତୁ",
    },
    "clear": {
        "english": "Clear", "tamil": "அழி", "telugu": "క్లియర్", "kannada": "ಅಳಿಸಿ", "malayalam": "മായ്ക്കുക",
        "hindi": "साफ़ करें", "bengali": "মুছুন", "marathi": "साफ करा", "gujarati": "સાફ કરો", "punjabi": "ਸਾਫ਼ ਕਰੋ", "odia": "ସଫା କରନ୍ତୁ",
    },
    "view_english": {
        "english": "View in English", "tamil": "ஆங்கிலத்தில் காண்க", "telugu": "ఆంగ్లంలో చూడండి",
        "kannada": "ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ವೀಕ್ಷಿಸಿ", "malayalam": "ഇംഗ്ലീഷിൽ കാണുക", "hindi": "अंग्रेज़ी में देखें",
        "bengali": "ইংরেজিতে দেখুন", "marathi": "इंग्रजीत पहा", "gujarati": "અંગ્રેજીમાં જુઓ",
        "punjabi": "ਅੰਗਰੇਜ਼ੀ ਵਿੱਚ ਵੇਖੋ", "odia": "ଇଂରାଜୀରେ ଦେଖନ୍ତୁ",
    },
    "no_upload_title": {
        "english": "Upload a paddy leaf image to begin diagnosis",
        "tamil": "நோய் கண்டறிதலைத் தொடங்க நெல் இலை படத்தை பதிவேற்றவும்",
        "telugu": "నిర్ధారణ ప్రారంభించడానికి వరి ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "kannada": "ರೋಗ ಪತ್ತೆ ಆರಂಭಿಸಲು ಭತ್ತದ ಎಲೆ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "malayalam": "രോഗനിർണയം ആരംഭിക്കാൻ നെല്ല് ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "hindi": "निदान शुरू करने हेतु धान की पत्ती की तस्वीर अपलोड करें",
        "bengali": "নির্ণয় শুরু করতে ধানের পাতার ছবি আপলোড করুন",
        "marathi": "निदान सुरू करण्यासाठी भाताच्या पानाचा फोटो अपलोड करा",
        "gujarati": "નિદાન શરૂ કરવા ડાંગરના પાનનો ફોટો અપલોડ કરો",
        "punjabi": "ਜਾਂਚ ਸ਼ੁਰੂ ਕਰਨ ਲਈ ਝੋਨੇ ਦੇ ਪੱਤੇ ਦੀ ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ",
        "odia": "ନିଦାନ ଆରମ୍ଭ କରିବାକୁ ଧାନ ପତ୍ରର ଛବି ଅପଲୋଡ କରନ୍ତୁ",
    },

    # ── Analytics / Dashboard section headers (added) ──────────
    "total_scans": {
        "english": "Total Scans", "tamil": "மொத்த ஸ்கேன்கள்", "telugu": "మొత్తం స్కాన్‌లు",
        "kannada": "ಒಟ್ಟು ಸ್ಕ್ಯಾನ್‌ಗಳು", "malayalam": "ആകെ സ്കാനുകൾ", "hindi": "कुल स्कैन",
        "bengali": "মোট স্ক্যান", "marathi": "एकूण स्कॅन", "gujarati": "કુલ સ્કેન",
        "punjabi": "ਕੁੱਲ ਸਕੈਨ", "odia": "ମୋଟ ସ୍କାନ",
    },
    "most_common_disease": {
        "english": "Most Common Disease", "tamil": "அதிகம் காணப்படும் நோய்", "telugu": "అత్యంత సాధారణ వ్యాధి",
        "kannada": "ಅತ್ಯಂತ ಸಾಮಾನ್ಯ ರೋಗ", "malayalam": "ഏറ്റവും സാധാരണമായ രോഗം", "hindi": "सबसे आम बीमारी",
        "bengali": "সর্বাধিক সাধারণ রোগ", "marathi": "सर्वाधिक सामान्य रोग", "gujarati": "સૌથી સામાન્ય રોગ",
        "punjabi": "ਸਭ ਤੋਂ ਆਮ ਬਿਮਾਰੀ", "odia": "ସର୍ବାଧିକ ସାଧାରଣ ରୋଗ",
    },
    "avg_confidence": {
        "english": "Avg Confidence", "tamil": "சராசரி நம்பகத்தன்மை", "telugu": "సగటు నమ్మకత్వం",
        "kannada": "ಸರಾಸರಿ ವಿಶ್ವಾಸ", "malayalam": "ശരാശരി ആത്മവിശ്വാസം", "hindi": "औसत विश्वास स्तर",
        "bengali": "গড় আত্মবিশ্বাস", "marathi": "सरासरी विश्वासार्हता", "gujarati": "સરેરાશ વિશ્વસનીયતા",
        "punjabi": "ਔਸਤ ਭਰੋਸੇਯੋਗਤਾ", "odia": "ହାରାହାରି ବିଶ୍ୱାସନୀୟତା",
    },
    "avg_health_index": {
        "english": "Avg Health Index", "tamil": "சராசரி ஆரோக்கிய குறியீடு", "telugu": "సగటు ఆరోగ్య సూచిక",
        "kannada": "ಸರಾಸರಿ ಆರೋಗ್ಯ ಸೂಚ್ಯಂಕ", "malayalam": "ശരാശരി ആരോഗ്യ സൂചിക", "hindi": "औसत स्वास्थ्य सूचकांक",
        "bengali": "গড় স্বাস্থ্য সূচক", "marathi": "सरासरी आरोग्य निर्देशांक", "gujarati": "સરેરાશ આરોગ્ય સૂચકાંક",
        "punjabi": "ਔਸਤ ਸਿਹਤ ਸੂਚਕਾਂਕ", "odia": "ହାରାହାରି ସ୍ୱାସ୍ଥ୍ୟ ସୂଚକାଙ୍କ",
    },
    "disease_distribution": {
        "english": "Disease Distribution", "tamil": "நோய் பரவல்", "telugu": "వ్యాధి పంపిణీ",
        "kannada": "ರೋಗ ವಿತರಣೆ", "malayalam": "രോഗ വിതരണം", "hindi": "रोग वितरण",
        "bengali": "রোগ বণ্টন", "marathi": "रोग वितरण", "gujarati": "રોગ વિતરણ",
        "punjabi": "ਬਿਮਾਰੀ ਵੰਡ", "odia": "ରୋଗ ବଣ୍ଟନ",
    },
    "scan_count_by_disease": {
        "english": "Scan Count by Disease", "tamil": "நோய் வாரியாக ஸ்கேன் எண்ணிக்கை",
        "telugu": "వ్యాధి వారీగా స్కాన్ సంఖ్య", "kannada": "ರೋಗವಾರು ಸ್ಕ್ಯಾನ್ ಸಂಖ್ಯೆ",
        "malayalam": "രോഗം അനുസരിച്ച് സ്കാൻ എണ്ണം", "hindi": "रोग के अनुसार स्कैन संख्या",
        "bengali": "রোগ অনুযায়ী স্ক্যান সংখ্যা", "marathi": "रोगानुसार स्कॅन संख्या",
        "gujarati": "રોગ મુજબ સ્કેન સંખ્યા", "punjabi": "ਬਿਮਾਰੀ ਅਨੁਸਾਰ ਸਕੈਨ ਗਿਣਤੀ", "odia": "ରୋଗ ଅନୁସାରେ ସ୍କାନ ସଂଖ୍ୟା",
    },
    "monthly_scan_trends": {
        "english": "Monthly Scan Trends", "tamil": "மாதாந்திர ஸ்கேன் போக்கு", "telugu": "నెలవారీ స్కాన్ ధోరణులు",
        "kannada": "ಮಾಸಿಕ ಸ್ಕ್ಯಾನ್ ಪ್ರವೃತ್ತಿ", "malayalam": "പ്രതിമാസ സ്കാൻ ട്രെൻഡുകൾ", "hindi": "मासिक स्कैन रुझान",
        "bengali": "মাসিক স্ক্যান প্রবণতা", "marathi": "मासिक स्कॅन ट्रेंड", "gujarati": "માસિક સ્કેન વલણ",
        "punjabi": "ਮਾਸਿਕ ਸਕੈਨ ਰੁਝਾਨ", "odia": "ମାସିକ ସ୍କାନ ଧାରା",
    },
    "severity_distribution": {
        "english": "Severity Distribution", "tamil": "தீவிரத்தன்மை பரவல்", "telugu": "తీవ్రత పంపిణీ",
        "kannada": "ತೀವ್ರತೆ ವಿತರಣೆ", "malayalam": "തീവ്രത വിതരണം", "hindi": "गंभीरता वितरण",
        "bengali": "তীব্রতা বণ্টন", "marathi": "तीव्रता वितरण", "gujarati": "તીવ્રતા વિતરણ",
        "punjabi": "ਗੰਭੀਰਤਾ ਵੰਡ", "odia": "ତୀବ୍ରତା ବଣ୍ଟନ",
    },
    "recent_predictions": {
        "english": "Recent Predictions", "tamil": "சமீபத்திய கணிப்புகள்", "telugu": "ఇటీవలి అంచనాలు",
        "kannada": "ಇತ್ತೀಚಿನ ಮುನ್ಸೂಚನೆಗಳು", "malayalam": "സമീപകാല പ്രവചനങ്ങൾ", "hindi": "हाल की भविष्यवाणियाँ",
        "bengali": "সাম্প্রতিক পূর্বাভাস", "marathi": "अलीकडील अंदाज", "gujarati": "તાજેતરની આગાહીઓ",
        "punjabi": "ਤਾਜ਼ਾ ਭਵਿੱਖਬਾਣੀਆਂ", "odia": "ସାମ୍ପ୍ରତିକ ପୂର୍ବାନୁମାନ",
    },
    "severity_health_overview": {
        "english": "Severity & Health Overview", "tamil": "தீவிரம் & ஆரோக்கிய கண்ணோட்டம்",
        "telugu": "తీవ్రత & ఆరోగ్య అవలోకనం", "kannada": "ತೀವ್ರತೆ ಮತ್ತು ಆರೋಗ್ಯ ಅವಲೋಕನ",
        "malayalam": "തീവ്രതയും ആരോഗ്യവും അവലോകനം", "hindi": "गंभीरता और स्वास्थ्य अवलोकन",
        "bengali": "তীব্রতা ও স্বাস্থ্য পর্যালোচনা", "marathi": "तीव्रता आणि आरोग्य आढावा",
        "gujarati": "તીવ્રતા અને આરોગ્ય ઝાંખી", "punjabi": "ਗੰਭੀਰਤਾ ਅਤੇ ਸਿਹਤ ਸੰਖੇਪ", "odia": "ତୀବ୍ରତା ଏବଂ ସ୍ୱାସ୍ଥ୍ୟ ସମୀକ୍ଷା",
    },
    "enhanced_health_intelligence": {
        "english": "Enhanced Crop Health Intelligence", "tamil": "மேம்படுத்தப்பட்ட பயிர் ஆரோக்கிய நுண்ணறிவு",
        "telugu": "మెరుగైన పంట ఆరోగ్య మేధస్సు", "kannada": "ವರ್ಧಿತ ಬೆಳೆ ಆರೋಗ್ಯ ಬುದ್ಧಿಮತ್ತೆ",
        "malayalam": "മെച്ചപ്പെടുത്തിയ വിള ആരോഗ്യ ബുദ്ധി", "hindi": "उन्नत फसल स्वास्थ्य बुद्धिमत्ता",
        "bengali": "উন্নত ফসল স্বাস্থ্য বুদ্ধিমত্তা", "marathi": "प्रगत पीक आरोग्य बुद्धिमत्ता",
        "gujarati": "અદ્યતન પાક આરોગ્ય બુદ્ધિ", "punjabi": "ਉੱਨਤ ਫਸਲ ਸਿਹਤ ਬੁੱਧੀ", "odia": "ଉନ୍ନତ ଫସଲ ସ୍ୱାସ୍ଥ୍ୟ ବୁଦ୍ଧିମତା",
    },
    "disease_risk": {
        "english": "Disease Risk", "tamil": "நோய் அபாயம்", "telugu": "వ్యాధి ప్రమాదం",
        "kannada": "ರೋಗ ಅಪಾಯ", "malayalam": "രോഗ അപകടസാധ്യത", "hindi": "रोग जोखिम",
        "bengali": "রোগের ঝুঁকি", "marathi": "रोग धोका", "gujarati": "રોગ જોખમ",
        "punjabi": "ਬਿਮਾਰੀ ਜੋਖਮ", "odia": "ରୋଗ ବିପଦ",
    },
    "recovery_potential_label": {
        "english": "Recovery Potential", "tamil": "மீட்பு திறன்", "telugu": "కోలుకునే అవకాశం",
        "kannada": "ಚೇತರಿಕೆ ಸಾಮರ್ಥ್ಯ", "malayalam": "വീണ്ടെടുക്കൽ സാധ്യത", "hindi": "सुधार क्षमता",
        "bengali": "পুনরুদ্ধার সম্ভাবনা", "marathi": "पुनर्प्राप्ती क्षमता", "gujarati": "રિકવરી સંભાવના",
        "punjabi": "ਰਿਕਵਰੀ ਸਮਰੱਥਾ", "odia": "ପୁନରୁଦ୍ଧାର ସମ୍ଭାବନା",
    },
    "ai_confidence_meter": {
        "english": "AI Confidence Meter", "tamil": "AI நம்பகத்தன்மை அளவீடு", "telugu": "AI నమ్మకత్వ మీటర్",
        "kannada": "AI ವಿಶ್ವಾಸ ಮೀಟರ್", "malayalam": "AI ആത്മവിശ്വാസ മീറ്റർ", "hindi": "AI विश्वास मीटर",
        "bengali": "AI আত্মবিশ্বাস মিটার", "marathi": "AI विश्वासार्हता मीटर", "gujarati": "AI વિશ્વસનીયતા મીટર",
        "punjabi": "AI ਭਰੋਸੇਯੋਗਤਾ ਮੀਟਰ", "odia": "AI ବିଶ୍ୱାସନୀୟତା ମିଟର",
    },
    "leaf_quality_label": {
        "english": "Leaf Quality", "tamil": "இலை தரம்", "telugu": "ఆకు నాణ్యత",
        "kannada": "ಎಲೆ ಗುಣಮಟ್ಟ", "malayalam": "ഇല ഗുണനിലവാരം", "hindi": "पत्ती गुणवत्ता",
        "bengali": "পাতার মান", "marathi": "पानाची गुणवत्ता", "gujarati": "પાનની ગુણવત્તા",
        "punjabi": "ਪੱਤੇ ਦੀ ਗੁਣਵੱਤਾ", "odia": "ପତ୍ର ଗୁଣବତ୍ତା",
    },
    "ai_explainability_report": {
        "english": "AI Explainability Report", "tamil": "AI விளக்க அறிக்கை", "telugu": "AI వివరణ నివేదిక",
        "kannada": "AI ವಿವರಣಾ ವರದಿ", "malayalam": "AI വിശദീകരണ റിപ്പോർട്ട്", "hindi": "AI व्याख्या रिपोर्ट",
        "bengali": "AI ব্যাখ্যা রিপোর্ট", "marathi": "AI स्पष्टीकरण अहवाल", "gujarati": "AI સમજૂતી અહેવાલ",
        "punjabi": "AI ਵਿਆਖਿਆ ਰਿਪੋਰਟ", "odia": "AI ବ୍ୟାଖ୍ୟା ରିପୋର୍ଟ",
    },
    "disease_affected_area": {
        "english": "Disease-Affected Area", "tamil": "நோய் பாதிக்கப்பட்ட பகுதி", "telugu": "వ్యాధి ప్రభావిత ప్రాంతం",
        "kannada": "ರೋಗ ಬಾಧಿತ ಪ್ರದೇಶ", "malayalam": "രോഗബാധിത ഭാഗം", "hindi": "रोग-प्रभावित क्षेत्र",
        "bengali": "রোগাক্রান্ত এলাকা", "marathi": "रोगग्रस्त भाग", "gujarati": "રોગ-અસરગ્રસ્ત વિસ્તાર",
        "punjabi": "ਬਿਮਾਰੀ-ਪ੍ਰਭਾਵਿਤ ਖੇਤਰ", "odia": "ରୋଗ ପ୍ରଭାବିତ ଅଞ୍ଚଳ",
    },
    "infection_location_label": {
        "english": "Infection Location", "tamil": "தொற்று இருப்பிடம்", "telugu": "సంక్రమణ ప్రాంతం",
        "kannada": "ಸೋಂಕಿನ ಸ್ಥಳ", "malayalam": "ബാധിച്ച സ്ഥാനം", "hindi": "संक्रमण स्थान",
        "bengali": "সংক্রমণের অবস্থান", "marathi": "संसर्ग स्थान", "gujarati": "ચેપનું સ્થાન",
        "punjabi": "ਲਾਗ ਦਾ ਸਥਾਨ", "odia": "ସଂକ୍ରମଣ ସ୍ଥାନ",
    },
    "attention_focus": {
        "english": "Attention Focus", "tamil": "கவன மையம்", "telugu": "దృష్టి కేంద్రీకరణ",
        "kannada": "ಗಮನ ಕೇಂದ್ರೀಕರಣ", "malayalam": "ശ്രദ്ധാ കേന്ദ്രീകരണം", "hindi": "ध्यान केंद्रण",
        "bengali": "মনোযোগ কেন্দ্রবিন্দু", "marathi": "लक्ष केंद्रीकरण", "gujarati": "ધ્યાન કેન્દ્રીકરણ",
        "punjabi": "ਧਿਆਨ ਕੇਂਦਰ", "odia": "ଧ୍ୟାନ କେନ୍ଦ୍ରୀକରଣ",
    },
    "treatment_effectiveness_analysis": {
        "english": "Treatment Effectiveness Analysis", "tamil": "சிகிச்சை செயல்திறன் பகுப்பாய்வு",
        "telugu": "చికిత్స సమర్థత విశ్లేషణ", "kannada": "ಚಿಕಿತ್ಸೆ ಪರಿಣಾಮಕಾರಿತ್ವ ವಿಶ್ಲೇಷಣೆ",
        "malayalam": "ചികിത്സാ ഫലപ്രാപ്തി വിശകലനം", "hindi": "उपचार प्रभावशीलता विश्लेषण",
        "bengali": "চিকিৎসা কার্যকারিতা বিশ্লেষণ", "marathi": "उपचार परिणामकारकता विश्लेषण",
        "gujarati": "સારવાર અસરકારકતા વિશ્લેષણ", "punjabi": "ਇਲਾਜ ਪ੍ਰਭਾਵਸ਼ੀਲਤਾ ਵਿਸ਼ਲੇਸ਼ਣ", "odia": "ଚିକିତ୍ସା କାର୍ଯ୍ୟକାରିତା ବିଶ୍ଳେଷଣ",
    },
    "option": {
        "english": "Option", "tamil": "விருப்பம்", "telugu": "ఎంపిక", "kannada": "ಆಯ್ಕೆ",
        "malayalam": "ഓപ്ഷൻ", "hindi": "विकल्प", "bengali": "বিকল্প", "marathi": "पर्याय",
        "gujarati": "વિકલ્પ", "punjabi": "ਵਿਕਲਪ", "odia": "ବିକଳ୍ପ",
    },
    "priority": {
        "english": "Priority", "tamil": "முன்னுரிமை", "telugu": "ప్రాధాన్యత", "kannada": "ಆದ್ಯತೆ",
        "malayalam": "മുൻഗണന", "hindi": "प्राथमिकता", "bengali": "অগ্রাধিকার", "marathi": "प्राधान्य",
        "gujarati": "પ્રાધાન્ય", "punjabi": "ਤਰਜੀਹ", "odia": "ପ୍ରାଥମିକତା",
    },
    "success_rate": {
        "english": "Success Rate", "tamil": "வெற்றி விகிதம்", "telugu": "విజయ రేటు", "kannada": "ಯಶಸ್ಸಿನ ದರ",
        "malayalam": "വിജയ നിരക്ക്", "hindi": "सफलता दर", "bengali": "সাফল্যের হার", "marathi": "यशाचा दर",
        "gujarati": "સફળતા દર", "punjabi": "ਸਫਲਤਾ ਦਰ", "odia": "ସଫଳତା ହାର",
    },
    "recovery_time": {
        "english": "Recovery Time", "tamil": "மீட்பு காலம்", "telugu": "కోలుకునే సమయం", "kannada": "ಚೇತರಿಕೆ ಸಮಯ",
        "malayalam": "വീണ്ടെടുക്കൽ സമയം", "hindi": "रिकवरी समय", "bengali": "পুনরুদ্ধার সময়", "marathi": "पुनर्प्राप्ती वेळ",
        "gujarati": "રિકવરી સમય", "punjabi": "ਰਿਕਵਰੀ ਸਮਾਂ", "odia": "ପୁନରୁଦ୍ଧାର ସମୟ",
    },
    "cost": {
        "english": "Cost", "tamil": "செலவு", "telugu": "ఖర్చు", "kannada": "ವೆಚ್ಚ", "malayalam": "ചെലവ്",
        "hindi": "लागत", "bengali": "খরচ", "marathi": "खर्च", "gujarati": "ખર્ચ", "punjabi": "ਲਾਗਤ", "odia": "ମୂଲ୍ୟ",
    },
    "eco_friendly": {
        "english": "Eco-Friendly", "tamil": "சுற்றுச்சூழல் நட்பு", "telugu": "పర్యావరణ అనుకూలం",
        "kannada": "ಪರಿಸರ ಸ್ನೇಹಿ", "malayalam": "പരിസ്ഥിതി സൗഹൃദം", "hindi": "पर्यावरण अनुकूल",
        "bengali": "পরিবেশ-বান্ধব", "marathi": "पर्यावरणपूरक", "gujarati": "પર્યાવરણને અનુકૂળ",
        "punjabi": "ਵਾਤਾਵਰਣ ਪੱਖੀ", "odia": "ପରିବେଶ ଅନୁକୂଳ",
    },
    "best_stage": {
        "english": "Best Stage", "tamil": "சிறந்த கட்டம்", "telugu": "ఉత్తమ దశ", "kannada": "ಉತ್ತಮ ಹಂತ",
        "malayalam": "മികച്ച ഘട്ടം", "hindi": "सर्वोत्तम चरण", "bengali": "সেরা পর্যায়", "marathi": "सर्वोत्तम टप्पा",
        "gujarati": "શ્રેષ્ઠ તબક્કો", "punjabi": "ਸਭ ਤੋਂ ਵਧੀਆ ਪੜਾਅ", "odia": "ସର୍ବୋତ୍ତମ ପର୍ଯ୍ୟାୟ",
    },
    "report_label": {
        "english": "Report", "tamil": "அறிக்கை", "telugu": "నివేదిక", "kannada": "ವರದಿ", "malayalam": "റിപ്പോർട്ട്",
        "hindi": "रिपोर्ट", "bengali": "রিপোর্ট", "marathi": "अहवाल", "gujarati": "અહેવાલ",
        "punjabi": "ਰਿਪੋਰਟ", "odia": "ରିପୋର୍ଟ",
    },
    "optional_details": {
        "english": "Optional Details", "tamil": "விருப்பமான விவரங்கள்", "telugu": "ఐచ్ఛిక వివరాలు",
        "kannada": "ಐಚ್ಛಿಕ ವಿವರಗಳು", "malayalam": "ഓപ്ഷണൽ വിശദാംശങ്ങൾ", "hindi": "वैकल्पिक विवरण",
        "bengali": "ঐচ্ছিক বিবরণ", "marathi": "पर्यायी तपशील", "gujarati": "વૈકલ્પિક વિગતો",
        "punjabi": "ਵਿਕਲਪਿਕ ਵੇਰਵੇ", "odia": "ଐଚ୍ଛିକ ବିବରଣୀ",
    },
    "farmer_name_label": {
        "english": "Farmer Name", "tamil": "விவசாயி பெயர்", "telugu": "రైతు పేరు", "kannada": "ರೈತನ ಹೆಸರು",
        "malayalam": "കർഷകന്റെ പേര്", "hindi": "किसान का नाम", "bengali": "কৃষকের নাম", "marathi": "शेतकऱ्याचे नाव",
        "gujarati": "ખેડૂતનું નામ", "punjabi": "ਕਿਸਾਨ ਦਾ ਨਾਮ", "odia": "କୃଷକଙ୍କ ନାମ",
    },
    "location_label": {
        "english": "Location", "tamil": "இடம்", "telugu": "ప్రాంతం", "kannada": "ಸ್ಥಳ", "malayalam": "സ്ഥലം",
        "hindi": "स्थान", "bengali": "অবস্থান", "marathi": "ठिकाण", "gujarati": "સ્થાન",
        "punjabi": "ਸਥਾਨ", "odia": "ସ୍ଥାନ",
    },
    "navigate_label": {
        "english": "Navigate", "tamil": "வழிசெலுத்து", "telugu": "నావిగేట్", "kannada": "ನ್ಯಾವಿಗೇಟ್",
        "malayalam": "നാവിഗേറ്റ്", "hindi": "नेविगेट करें", "bengali": "নেভিগেট করুন", "marathi": "नेव्हिगेट करा",
        "gujarati": "નેવિગેટ કરો", "punjabi": "ਨੈਵੀਗੇਟ ਕਰੋ", "odia": "ନାଭିଗେଟ୍ କରନ୍ତୁ",
    },
    "signed_in_as": {
        "english": "Signed in as", "tamil": "இப்படி உள்நுழைந்துள்ளீர்கள்", "telugu": "ఇలా సైన్ ఇన్ చేసారు",
        "kannada": "ಹೀಗೆ ಸೈನ್ ಇನ್ ಆಗಿದ್ದೀರಿ", "malayalam": "ഇങ്ങനെ സൈൻ ഇൻ ചെയ്തിരിക്കുന്നു", "hindi": "इस रूप में साइन इन है",
        "bengali": "এইভাবে সাইন ইন করা আছে", "marathi": "असे साइन इन केले आहे", "gujarati": "આ રીતે સાઇન ઇન છે",
        "punjabi": "ਇਸ ਤਰ੍ਹਾਂ ਸਾਈਨ ਇਨ ਹੈ", "odia": "ଏହିପରି ସାଇନ୍ ଇନ୍ ହୋଇଛନ୍ତି",
    },
    "browsing_as": {
        "english": "Browsing as", "tamil": "இப்படி உலாவுகிறீர்கள்", "telugu": "ఇలా బ్రౌజ్ చేస్తున్నారు",
        "kannada": "ಹೀಗೆ ಬ್ರೌಸ್ ಮಾಡುತ್ತಿದ್ದೀರಿ", "malayalam": "ഇങ്ങനെ ബ്രൗസ് ചെയ്യുന്നു", "hindi": "इस रूप में ब्राउज़ कर रहे हैं",
        "bengali": "এইভাবে ব্রাউজ করছেন", "marathi": "असे ब्राउझ करत आहात", "gujarati": "આ રીતે બ્રાઉઝ કરી રહ્યાં છો",
        "punjabi": "ਇਸ ਤਰ੍ਹਾਂ ਬ੍ਰਾਊਜ਼ ਕਰ ਰਹੇ ਹੋ", "odia": "ଏହିପରି ବ୍ରାଉଜ୍ କରୁଛନ୍ତି",
    },

    # ═══════════════════════════════════════════════════════════
    # NEW KEYS — added for full-coverage multilingual refactor.
    # Explicit English + Malayalam text (this pass's target languages).
    # Other nine languages fall back to English automatically via
    # get_ui_labels() until native strings are added for them — this
    # does not break anything, it only affects these new labels.
    # ═══════════════════════════════════════════════════════════
    "access_denied": {
        "english": "🚫 Access Denied. This page is for administrators only.",
        "malayalam": "🚫 പ്രവേശനം നിഷേധിച്ചു. ഈ പേജ് അഡ്മിനിസ്ട്രേറ്റർമാർക്ക് മാത്രമുള്ളതാണ്.",
    },
    "admin_login_heading": {"english": "Admin Login", "malayalam": "അഡ്മിൻ ലോഗിൻ"},
    "username_label": {"english": "Username", "malayalam": "ഉപയോക്തൃനാമം"},
    "password_label": {"english": "Password", "malayalam": "പാസ്‌വേഡ്"},
    "login_as_admin_btn": {"english": "Login as Admin", "malayalam": "അഡ്മിനായി ലോഗിൻ ചെയ്യുക"},
    "logout_btn": {"english": "Logout", "malayalam": "ലോഗ്ഔട്ട്"},
    "login_success": {"english": "Logged in ✅", "malayalam": "ലോഗിൻ വിജയകരം ✅"},
    "invalid_credentials": {"english": "Invalid credentials.", "malayalam": "തെറ്റായ ലോഗിൻ വിവരങ്ങൾ."},
    "farmer_name_ph": {"english": "e.g. Murugan", "malayalam": "ഉദാ: രാജൻ"},
    "location_ph": {"english": "e.g. Thanjavur", "malayalam": "ഉദാ: പാലക്കാട്"},
    "analysing_leaf": {"english": "Analysing leaf...", "malayalam": "ഇല വിശകലനം ചെയ്യുന്നു..."},
    "generating_heatmap": {
        "english": "Generating explainability heatmap...",
        "malayalam": "വിശദീകരണ ഹീറ്റ്മാപ്പ് നിർമ്മിക്കുന്നു...",
    },
    "gradcam_failed": {"english": "Grad-CAM failed on this platform", "malayalam": "Grad-CAM ഈ പ്ലാറ്റ്ഫോമിൽ പരാജയപ്പെട്ടു"},
    "heatmap_failed": {"english": "Heatmap generation failed", "malayalam": "ഹീറ്റ്മാപ്പ് നിർമ്മാണം പരാജയപ്പെട്ടു"},
    "gradcam_unavailable": {
        "english": "Grad-CAM unavailable for this model layer.",
        "malayalam": "ഈ മോഡൽ ലെയറിന് Grad-CAM ലഭ്യമല്ല.",
    },
    "lesion_coverage_caption": {"english": "Lesion coverage", "malayalam": "മുറിവ് വ്യാപ്തി"},
    "why_predicted_label": {"english": "Why the model predicted this", "malayalam": "മോഡൽ ഇത് എന്തുകൊണ്ട് പ്രവചിച്ചു"},
    "summary_label": {"english": "Summary", "malayalam": "സംഗ്രഹം"},
    "confidence_interpretation_label": {"english": "Confidence interpretation", "malayalam": "വിശ്വാസ്യത വ്യാഖ്യാനം"},
    "agricultural_interpretation_label": {"english": "Agricultural interpretation", "malayalam": "കാർഷിക വ്യാഖ്യാനം"},
    "building_pdf": {"english": "Building PDF report...", "malayalam": "PDF റിപ്പോർട്ട് തയ്യാറാക്കുന്നു..."},
    "report_section_title": {"english": "Report", "malayalam": "റിപ്പോർട്ട്"},
    "chatbot_intro_caption": {
        "english": "Ask about crop diseases, fertilizers, irrigation, pests, and more.",
        "malayalam": "വിള രോഗങ്ങൾ, വളങ്ങൾ, ജലസേചനം, കീടങ്ങൾ എന്നിവയെക്കുറിച്ച് ചോദിക്കൂ.",
    },
    "quick_questions_label": {"english": "Quick questions:", "malayalam": "പെട്ടെന്നുള്ള ചോദ്യങ്ങൾ:"},
    "upload_dashboard_info": {
        "english": "📤 Upload images on the Diagnosis page to populate the dashboard.",
        "malayalam": "📤 ഡാഷ്ബോർഡ് നിറയ്ക്കാൻ 'രോഗനിർണയം' പേജിൽ ചിത്രങ്ങൾ അപ്‌ലോഡ് ചെയ്യുക.",
    },
    "training_curves_header": {
        "english": "Training Curves (from last training run)",
        "malayalam": "പരിശീലന വക്രങ്ങൾ (അവസാന പരിശീലനത്തിൽ നിന്ന്)",
    },
    "confusion_matrix_header": {
        "english": "Confusion Matrix (from last training run)",
        "malayalam": "കൺഫ്യൂഷൻ മാട്രിക്സ് (അവസാന പരിശീലനത്തിൽ നിന്ന്)",
    },
    "upload_eval_data_header": {"english": "Upload Evaluation Data (Optional)", "malayalam": "മൂല്യനിർണ്ണയ ഡാറ്റ അപ്‌ലോഡ് ചെയ്യുക (ഐച്ഛികം)"},
    "csv_upload_caption": {
        "english": "Upload a CSV with columns `true_label` and `pred_label`.",
        "malayalam": "`true_label`, `pred_label` എന്നീ കോളങ്ങളുള്ള ഒരു CSV അപ്‌ലോഡ് ചെയ്യുക.",
    },
    "upload_eval_csv_label": {"english": "Upload evaluation CSV", "malayalam": "മൂല്യനിർണ്ണയ CSV അപ്‌ലോഡ് ചെയ്യുക"},
    "csv_column_error": {
        "english": "CSV must have columns: `true_label` and `pred_label`",
        "malayalam": "CSV-യിൽ `true_label`, `pred_label` എന്നീ കോളങ്ങൾ ഉണ്ടായിരിക്കണം",
    },
    "overall_accuracy_label": {"english": "Overall Accuracy", "malayalam": "മൊത്തം കൃത്യത"},
    "macro_average_label": {"english": "Macro Average", "malayalam": "മാക്രോ ശരാശരി"},
    "weighted_average_label": {"english": "Weighted Average", "malayalam": "വെയ്റ്റഡ് ശരാശരി"},
    "admin_dashboard_title": {"english": "👑 Admin Dashboard", "malayalam": "👑 അഡ്മിൻ ഡാഷ്ബോർഡ്"},
    "admin_dashboard_caption": {
        "english": "System-wide usage summary and disease statistics.",
        "malayalam": "സിസ്റ്റം-വ്യാപകമായ ഉപയോഗ സംഗ്രഹവും രോഗ സ്ഥിതിവിവരവും.",
    },
    "no_predictions_logged": {"english": "No predictions have been logged yet.", "malayalam": "ഇതുവരെ പ്രവചനങ്ങളൊന്നും രേഖപ്പെടുത്തിയിട്ടില്ല."},
    "predictions_by_disease_header": {"english": "Predictions by Disease", "malayalam": "രോഗം അനുസരിച്ചുള്ള പ്രവചനങ്ങൾ"},
    "scans_per_user_header": {"english": "Scans per User", "malayalam": "ഉപയോക്താവ് അനുസരിച്ചുള്ള സ്കാനുകൾ"},
    "recent_activity_header": {"english": "Recent Activity (last 10 scans)", "malayalam": "സമീപകാല പ്രവർത്തനം (അവസാന 10 സ്കാനുകൾ)"},
    "full_history_title": {"english": "📋 Full Prediction History", "malayalam": "📋 പൂർണ്ണ പ്രവചന ചരിത്രം"},
    "full_history_caption": {
        "english": "Complete log of every prediction across all users.",
        "malayalam": "എല്ലാ ഉപയോക്താക്കളുടെയും എല്ലാ പ്രവചനങ്ങളുടെയും പൂർണ്ണ രേഖ.",
    },
    "no_prediction_records": {"english": "No prediction records found.", "malayalam": "പ്രവചന രേഖകളൊന്നും കണ്ടെത്തിയില്ല."},
    "filter_by_user": {"english": "Filter by User", "malayalam": "ഉപയോക്താവ് അനുസരിച്ച് ഫിൽട്ടർ ചെയ്യുക"},
    "filter_by_disease": {"english": "Filter by Disease", "malayalam": "രോഗം അനുസരിച്ച് ഫിൽട്ടർ ചെയ്യുക"},
    "showing_records_of": {
        "english": "Showing **{shown}** of **{total}** records.",
        "malayalam": "**{total}**-ൽ **{shown}** രേഖകൾ കാണിക്കുന്നു.",
    },
    "full_prediction_history_count": {
        "english": "Full Prediction History ({total} records)",
        "malayalam": "പൂർണ്ണ പ്രവചന ചരിത്രം ({total} രേഖകൾ)",
    },
    "model_architecture_summary_header": {"english": "Model Architecture Summary", "malayalam": "മോഡൽ ആർക്കിടെക്ചർ സംഗ്രഹം"},
    "cnn_resnet_effnet_header": {
        "english": "CNN vs ResNet50 vs EfficientNetB0", "malayalam": "CNN vs ResNet50 vs EfficientNetB0",
    },
    "accuracy_precision_recall_f1_header": {
        "english": "Accuracy, Precision, Recall & F1 Comparison",
        "malayalam": "കൃത്യത, പ്രിസിഷൻ, റീകോൾ & F1 താരതമ്യം",
    },

    # ─── ADDED — multilingual fix pass: these admin-only pages (Research,
    # Admin Dashboard, Full History) had hardcoded English strings that
    # were never routed through get_ui_labels()/ui_text(), which is why
    # switching the language left them untranslated while the rest of
    # the app (Diagnosis / Chatbot / Model Performance / Analytics) was
    # already fully localized. Only "english" is hand-written below —
    # exactly like every other key in this file, _pick() auto-translates
    # every other one of the 11 languages on demand via Gemini (cached).
    "admin_total_predictions_label": {"english": "Total Predictions"},
    "admin_unique_users_label":      {"english": "Unique Users"},
    "admin_top_disease_label":       {"english": "Top Disease"},
    "download_full_log_btn":         {"english": "⬇️ Download Full Log as CSV"},
    "download_filtered_log_btn":     {"english": "⬇️ Download Filtered Log as CSV"},
    "all_users_option":              {"english": "All Users"},
    "all_diseases_option":           {"english": "All Diseases"},

    "research_metrics_caption": {
        "english": "Confusion matrix, classification report, and training curves "
                    "from the last training run.",
    },
    "eval_confusion_matrix_caption": {"english": "Confusion Matrix"},
    "eval_col_class":     {"english": "Class"},
    "eval_col_precision": {"english": "Precision"},
    "eval_col_recall":    {"english": "Recall"},
    "eval_col_f1":        {"english": "F1 Score"},
    "eval_col_support":   {"english": "Support"},

    "capability_comparison_full_title": {
        "english": "Capability Comparison Across the Three Deep Learning Models",
    },
    "capability_score_axis_lower": {"english": "Capability score (1–5)"},
    "capability_models_caption": {
        "english": "CNN (Baseline): a shallow architecture with limited depth and "
                    "feature-representation capacity, restricting how much "
                    "disease-relevant detail it can extract. ResNet50 (Benchmark): "
                    "a strong deep feature extractor via residual learning, capable "
                    "of learning rich hierarchical features, but computationally "
                    "heavier and more resource-intensive to deploy. EfficientNetB0 "
                    "(Proposed): the proposed model, offering a strong balance of "
                    "feature extraction, computational efficiency, scalability, and "
                    "deployment suitability through compound scaling and transfer "
                    "learning.",
    },
    "why_effnet_selected_title": {"english": "Why EfficientNetB0 Was Selected"},
    "why_effnet_selected_body": {
        "english": "EfficientNetB0 was selected as the proposed model because it "
                    "provides an effective balance between deep feature extraction "
                    "capability, computational efficiency, deployment suitability, "
                    "and scalability. Through compound scaling and transfer "
                    "learning, the model learns strong visual representations "
                    "while requiring fewer computational resources than heavier "
                    "architectures such as ResNet50.",
    },
    "research_metrics_avg_gain_caption": {
        "english": "Across all evaluation metrics, the Proposed Smart Paddy AI "
                    "system performs better than the existing system, with an "
                    "average improvement of {gain:.1f} percentage points "
                    "({proposed:.1f}% vs {existing:.1f}%).",
    },
    "research_final_conclusion_template": {
        "english": "✅ <b>Conclusion:</b> Based on the capability comparison, "
                    "<b>EfficientNetB0 is the most suitable model</b> among the "
                    "three architectures evaluated for the Smart Paddy AI system. "
                    "The proposed system also demonstrates improved Accuracy, "
                    "Precision, Recall, and F1-Score compared with the existing "
                    "system, with an average gain of {gain:.1f} percentage points "
                    "({proposed:.1f}% vs {existing:.1f}%). Together, model "
                    "capability and evaluation performance support EfficientNetB0 "
                    "as the proposed model for this project.",
    },
    "model_arch_param_col": {"english": "Parameter"},
    "model_arch_value_col": {"english": "Value"},

    # ─── ADDED — PaddyBuddy floating assistant character (new feature) ───
    "paddybuddy_name": {"english": "PaddyBuddy"},
    "paddybuddy_greeting": {
        "english": "Hi! I'm PaddyBuddy 🌾 How can I help you?",
        "tamil": "வணக்கம்! நான் PaddyBuddy 🌾 உங்களுக்கு எப்படி உதவலாம்?",
        "telugu": "నమస్కారం! నేను PaddyBuddy 🌾 మీకు ఎలా సహాయం చేయగలను?",
        "kannada": "ನಮಸ್ಕಾರ! ನಾನು PaddyBuddy 🌾 ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
        "malayalam": "നമസ്കാരം! ഞാൻ PaddyBuddy 🌾 നിങ്ങളെ എങ്ങനെ സഹായിക്കാം?",
        "hindi": "नमस्ते! मैं PaddyBuddy 🌾 आपकी कैसे मदद कर सकता हूँ?",
        "bengali": "নমস্কার! আমি PaddyBuddy 🌾 আপনাকে কীভাবে সাহায্য করতে পারি?",
        "marathi": "नमस्कार! मी PaddyBuddy 🌾 तुम्हाला कशी मदत करू शकतो?",
        "gujarati": "નમસ્તે! હું PaddyBuddy 🌾 તમારી કેવી રીતે મદદ કરી શકું?",
        "punjabi": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ PaddyBuddy 🌾 ਤੁਹਾਡੀ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?",
        "odia": "ନମସ୍କାର! ମୁଁ PaddyBuddy 🌾 ଆପଣଙ୍କୁ କିପରି ସାହାଯ୍ୟ କରିପାରିବି?",
    },
    "paddybuddy_on_upload": {"english": "Let me take a look at your paddy leaf!"},
    "paddybuddy_analysing": {"english": "Analysing the leaf..."},
    "paddybuddy_healthy": {"english": "Great! Your paddy leaf looks healthy!"},
    "paddybuddy_disease_found": {"english": "Don't worry. I'll explain what you can do."},
    "paddybuddy_chat_open": {"english": "Hi there! Ask me anything about your paddy crop."},
    "paddybuddy_panel_title": {"english": "PaddyBuddy Assistant"},
    "paddybuddy_close_btn": {"english": "Close"},
    "paddybuddy_result_context": {
        "english": "Your leaf was identified as {disease} with {severity} severity. "
                    "I can explain the symptoms, treatment and prevention steps.",
    },

    # ─── ADDED — multilingual fix pass: sidebar Gemini-status messages
    # were hardcoded English and never routed through get_ui_labels()/
    # ui_text(), so they stayed in English regardless of the selected
    # language. Only "english" is hand-written — _pick() auto-translates
    # every other language on demand via Gemini (cached), same as every
    # other key in this file.
    "gemini_not_configured_warning": {
        "english": "⚠️ GEMINI_API_KEY not found — translated advisory text and "
                    "the AI chatbot will show English/placeholder content only. "
                    "Add GEMINI_API_KEY in .streamlit/secrets.toml or as an "
                    "environment variable.",
    },
    "gemini_last_error_expander": {
        "english": "⚠️ Last Gemini error (translation may have fallen back to English)",
    },
}


def get_ui_labels(lang: str) -> dict:
    """Return the full UI-label dict for a given language (English fallback per key)."""
    lang = resolve_lang(lang)
    return {key: _pick(block, lang) for key, block in _UI_RAW.items()}


def ui_text(key: str, lang: str, **kwargs) -> str:
    """
    Fetch a single UI string by key and `.format(**kwargs)` it.
    Convenience wrapper so callers don't need get_ui_labels() just for
    one interpolated string (e.g. "Showing {shown} of {total} records").
    Unknown key -> returns the key itself so a typo is visible in the UI
    instead of silently swallowed.
    """
    lang = resolve_lang(lang)
    block = _UI_RAW.get(key)
    if block is None:
        return key
    template = _pick(block, lang)
    return template.format(**kwargs) if kwargs else template


# ═══════════════════════════════════════════════════════════════
# SEVERITY / EXPLAINABILITY SENTENCE TEMPLATES
# ═══════════════════════════════════════════════════════════════
# These build the natural-language sentences used in
# utils/severity.py (advanced_health_dashboard -> ai_summary) and
# utils/explainability.py (why_predicted / explainability_summary /
# confidence_interpretation / agricultural_interpretation), so those
# modules never hardcode English prose — they call these functions
# and pass in the already-computed numbers/labels.
# ═══════════════════════════════════════════════════════════════

def confidence_interpretation_text(confidence: float, focus_label: str, lang: str) -> str:
    lang = resolve_lang(lang)
    conf_pct = confidence * 100

    _BASE = {
        "very_high": {
            "english": "Very high confidence — the model found strong, unambiguous visual evidence.",
            "malayalam": "വളരെ ഉയർന്ന വിശ്വാസ്യത — മോഡലിന് ശക്തവും വ്യക്തവുമായ ദൃശ്യ തെളിവുകൾ ലഭിച്ചു.",
        },
        "high": {
            "english": "High confidence — clear disease-consistent patterns were detected.",
            "malayalam": "ഉയർന്ന വിശ്വാസ്യത — രോഗവുമായി യോജിക്കുന്ന വ്യക്തമായ പാറ്റേണുകൾ കണ്ടെത്തി.",
        },
        "moderate": {
            "english": "Moderate confidence — some disease-consistent features present, but signs are less distinct.",
            "malayalam": "മിതമായ വിശ്വാസ്യത — രോഗവുമായി യോജിക്കുന്ന ചില സവിശേഷതകൾ ഉണ്ട്, പക്ഷേ അടയാളങ്ങൾ അത്ര വ്യക്തമല്ല.",
        },
        "low": {
            "english": "Low confidence — visual evidence is weak or ambiguous; manual verification is recommended.",
            "malayalam": "കുറഞ്ഞ വിശ്വാസ്യത — ദൃശ്യ തെളിവുകൾ ദുർബലമോ അവ്യക്തമോ ആണ്; നേരിട്ട് പരിശോധിക്കാൻ ശുപാർശ ചെയ്യുന്നു.",
        },
    }
    _FOCUSED_ADD = {
        "english": " The attention heatmap is tightly concentrated on specific lesions, supporting this reading.",
        "malayalam": " ശ്രദ്ധാ ഹീറ്റ്മാപ്പ് പ്രത്യേക മുറിവുകളിൽ കേന്ദ്രീകരിച്ചിരിക്കുന്നു, ഇത് ഈ വിലയിരുത്തലിനെ പിന്തുണയ്ക്കുന്നു.",
    }
    _DIFFUSE_ADD = {
        "english": " The attention heatmap is spread broadly across the leaf, which can lower prediction certainty.",
        "malayalam": " ശ്രദ്ധാ ഹീറ്റ്മാപ്പ് ഇല മുഴുവനും വ്യാപിച്ചിരിക്കുന്നു, ഇത് പ്രവചന ഉറപ്പ് കുറയ്ക്കാം.",
    }

    if conf_pct >= 85:
        bucket = "very_high"
    elif conf_pct >= 65:
        bucket = "high"
    elif conf_pct >= 45:
        bucket = "moderate"
    else:
        bucket = "low"

    text = _pick(_BASE[bucket], lang)
    if focus_label == "Focused":
        text += _pick(_FOCUSED_ADD, lang)
    elif focus_label == "Diffuse":
        text += _pick(_DIFFUSE_ADD, lang)
    return text


def why_predicted_text(disease: str, location: str, coverage_label: str, focus_label: str, lang: str) -> str:
    lang = resolve_lang(lang)
    disease_name = disease.replace("_", " ").title()

    if disease.lower() in ("healthy", "normal"):
        _HEALTHY = {
            "english": (
                "The Grad-CAM heatmap shows no meaningful concentration of activation on "
                "lesion-like regions, and pixel activation stayed below the disease threshold "
                "across the leaf — consistent with a healthy classification."
            ),
            "malayalam": (
                "Grad-CAM ഹീറ്റ്മാപ്പിൽ മുറിവ് പോലുള്ള ഭാഗങ്ങളിൽ കാര്യമായ ആക്റ്റിവേഷൻ കേന്ദ്രീകരണം "
                "കാണുന്നില്ല, ഇലയിലുടനീളം പിക്സൽ ആക്റ്റിവേഷൻ രോഗ പരിധിക്ക് താഴെയാണ് — ഇത് ആരോഗ്യകരമായ "
                "വർഗ്ഗീകരണവുമായി യോജിക്കുന്നു."
            ),
        }
        return _pick(_HEALTHY, lang)

    loc = translate_enum(location, lang)
    cov = translate_enum(coverage_label, lang)
    foc = translate_enum(focus_label, lang)

    _TMPL = {
        "english": (
            "The model concentrated its attention primarily on the {location}, "
            "with a {focus} activation pattern and {coverage}. "
            "This spatial pattern of activated pixels is consistent with the visual signature "
            "typically associated with {disease_name}."
        ),
        "malayalam": (
            "മോഡൽ അതിന്റെ ശ്രദ്ധ പ്രധാനമായും {location}-ൽ കേന്ദ്രീകരിച്ചു, {focus} ആക്റ്റിവേഷൻ "
            "പാറ്റേണിനൊപ്പം {coverage}. ഈ സ്ഥലപരമായ ആക്റ്റിവേഷൻ പാറ്റേൺ സാധാരണയായി "
            "{disease_name}-മായി ബന്ധപ്പെട്ട ദൃശ്യ സവിശേഷതയുമായി യോജിക്കുന്നു."
        ),
    }
    template = _pick(_TMPL, lang)
    return template.format(
        location=loc.lower() if lang == "english" else loc,
        focus=foc.lower() if lang == "english" else foc,
        coverage=cov.lower() if lang == "english" else cov,
        disease_name=disease_name,
    )


def explainability_summary_text(
    disease: str, disease_pct: float, healthy_pct: float,
    location: str, coverage_label: str, confidence_interp: str, lang: str,
) -> str:
    lang = resolve_lang(lang)
    loc = translate_enum(location, lang)
    cov = translate_enum(coverage_label, lang)

    _TMPL = {
        "english": (
            "For this leaf, the AI estimated {disease_pct}% of the visible tissue as "
            "disease-affected and {healthy_pct}% as healthy, with attention concentrated "
            "around the {location}. Coverage is classified as {coverage}. {conf_interp}"
        ),
        "malayalam": (
            "ഈ ഇലയിൽ, ദൃശ്യമായ ടിഷ്യുവിന്റെ {disease_pct}% AI രോഗബാധിതമെന്നും "
            "{healthy_pct}% ആരോഗ്യകരമെന്നും കണക്കാക്കി, ശ്രദ്ധ {location}-ന് ചുറ്റും "
            "കേന്ദ്രീകരിച്ചു. വ്യാപ്തി {coverage} ആയി തരംതിരിച്ചിരിക്കുന്നു. {conf_interp}"
        ),
    }
    template = _pick(_TMPL, lang)
    return template.format(
        disease_pct=disease_pct, healthy_pct=healthy_pct,
        location=loc.lower() if lang == "english" else loc,
        coverage=cov.lower() if lang == "english" else cov,
        conf_interp=confidence_interp,
    )


def agricultural_interpretation_text(disease: str, location: str, disease_pct: float, lang: str) -> str:
    lang = resolve_lang(lang)
    disease_name = disease.replace("_", " ").title()

    if disease.lower() in ("healthy", "normal"):
        _HEALTHY = {
            "english": (
                "No corrective action is indicated. Continue routine field scouting to catch "
                "early symptoms before they spread."
            ),
            "malayalam": (
                "തിരുത്തൽ നടപടികളൊന്നും ആവശ്യമില്ല. രോഗലക്ഷണങ്ങൾ പടരുന്നതിന് മുമ്പ് കണ്ടെത്താൻ "
                "പതിവ് വയൽ പരിശോധന തുടരുക."
            ),
        }
        return _pick(_HEALTHY, lang)

    loc = translate_enum(location, lang)
    _URGENT = {
        "english": "Inspect the crop in person as soon as possible and consider immediate treatment.",
        "malayalam": "കഴിയുന്നത്ര വേഗം വിള നേരിട്ട് പരിശോധിക്കുകയും ഉടനടി ചികിത്സ പരിഗണിക്കുകയും ചെയ്യുക.",
    }
    _EARLY = {
        "english": (
            "Inspect the highlighted region closely during your next field walk; early-stage "
            "intervention now can prevent further spread."
        ),
        "malayalam": (
            "അടുത്ത വയൽ പരിശോധനയിൽ അടയാളപ്പെടുത്തിയ ഭാഗം സൂക്ഷ്മമായി പരിശോധിക്കുക; ഇപ്പോൾ "
            "നേരത്തെയുള്ള ഇടപെടൽ കൂടുതൽ വ്യാപനം തടയാൻ സഹായിക്കും."
        ),
    }
    urgency = (_URGENT if disease_pct >= 40 else _EARLY).get(
        lang, (_URGENT if disease_pct >= 40 else _EARLY)["english"]
    )

    _TMPL = {
        "english": (
            "Farmers should physically check the {location} of affected plants for "
            "symptoms typical of {disease_name} (lesions, discolouration, or wilting depending "
            "on disease type). {urgency}"
        ),
        "malayalam": (
            "{disease_name}-ന്റെ സാധാരണ ലക്ഷണങ്ങൾക്കായി (മുറിവുകൾ, നിറവ്യത്യാസം, അല്ലെങ്കിൽ "
            "വാട്ടം, രോഗത്തിന്റെ തരം അനുസരിച്ച്) ബാധിച്ച ചെടികളുടെ {location} കർഷകർ നേരിട്ട് "
            "പരിശോധിക്കണം. {urgency}"
        ),
    }
    template = _pick(_TMPL, lang)
    return template.format(
        location=loc.lower() if lang == "english" else loc,
        disease_name=disease_name,
        urgency=urgency,
    )


def health_ai_summary_text(
    is_healthy: bool, confidence_meter: float, disease: str,
    severity_label: str, severity_pct: float, health_score: float,
    health_category: str, recovery_label: str, lang: str,
) -> str:
    lang = resolve_lang(lang)
    disease_name = disease.replace("_", " ").title()

    if is_healthy:
        _TMPL = {
            "english": (
                "This plant shows no disease indicators. Confidence in this "
                "assessment is {confidence_meter}%. Continue routine monitoring."
            ),
            "malayalam": (
                "ഈ ചെടിയിൽ രോഗ ലക്ഷണങ്ങളൊന്നും കാണുന്നില്ല. ഈ വിലയിരുത്തലിന്റെ "
                "വിശ്വാസ്യത {confidence_meter}% ആണ്. പതിവ് നിരീക്ഷണം തുടരുക."
            ),
        }
        template = _pick(_TMPL, lang)
        return template.format(confidence_meter=confidence_meter)

    sev_label = translate_enum(severity_label, lang)
    cat_label = translate_enum(health_category, lang)
    rec_label = translate_enum(recovery_label, lang)

    _TMPL = {
        "english": (
            "{disease_name} detected with {confidence_meter}% confidence. "
            "Estimated severity is {severity_label} ({severity_pct}%), "
            "placing crop health at {health_score}/100 ({health_category}). "
            "Recovery potential is assessed as {recovery_label} with prompt treatment."
        ),
        "malayalam": (
            "{confidence_meter}% വിശ്വാസ്യതയോടെ {disease_name} കണ്ടെത്തി. "
            "കണക്കാക്കിയ തീവ്രത {severity_label} ({severity_pct}%) ആണ്, "
            "വിള ആരോഗ്യം {health_score}/100 ({health_category}) ആണ്. "
            "ഉടനടി ചികിത്സയോടെ രോഗമുക്തി സാധ്യത {recovery_label} ആയി വിലയിരുത്തുന്നു."
        ),
    }
    template = _pick(_TMPL, lang)
    return template.format(
        disease_name=disease_name,
        confidence_meter=confidence_meter,
        severity_label=sev_label.lower() if lang == "english" else sev_label,
        severity_pct=severity_pct,
        health_score=health_score,
        health_category=cat_label.lower() if lang == "english" else cat_label,
        recovery_label=rec_label.lower() if lang == "english" else rec_label,
    )


# ═══════════════════════════════════════════════════════════════
# TREATMENT NAME / STAGE TRANSLATIONS (utils/treatment_analysis.py)
# ═══════════════════════════════════════════════════════════════
# Chemical/fungicide/product names are left EXACTLY as in English per
# the project's requirement that scientific & chemical names are not
# translated. Only the plain-language action/stage wording is
# translated. Any name/stage not found here is shown as-is (English) —
# safe fallback, never crashes.
_TREATMENT_STAGE_RAW = {
    "Early to active infection": {
        "tamil": "ஆரம்பம் முதல் செயலில் உள்ள தொற்று வரை", "telugu": "ప్రారంభం నుండి క్రియాశీల సంక్రమణ వరకు", "kannada": "ಆರಂಭಿಕದಿಂದ ಸಕ್ರಿಯ ಸೋಂಕಿನವರೆಗೆ", "malayalam": "പ്രാരംഭം മുതൽ സജീവ അണുബാധ വരെ", "hindi": "प्रारंभिक से सक्रिय संक्रमण तक", "bengali": "প্রাথমিক থেকে সক্রিয় সংক্রমণ", "marathi": "प्रारंभिक ते सक्रिय संसर्ग", "gujarati": "પ્રારંભિકથી સક્રિય ચેપ સુધી", "punjabi": "ਸ਼ੁਰੂਆਤੀ ਤੋਂ ਸਰਗਰਮ ਲਾਗ ਤੱਕ", "odia": "ପ୍ରାରମ୍ଭିକରୁ ସକ୍ରିୟ ସଂକ୍ରମଣ ପର୍ଯ୍ୟନ୍ତ", "malayalam": "പ്രാരംഭം മുതൽ സജീവ അണുബാധ വരെ"},
    "Early infection": {
        "tamil": "ஆரம்ப தொற்று", "telugu": "ప్రారంభ సంక్రమణ", "kannada": "ಆರಂಭಿಕ ಸೋಂಕು", "malayalam": "പ്രാരംഭ അണുബാധ", "hindi": "प्रारंभिक संक्रमण", "bengali": "প্রাথমিক সংক্রমণ", "marathi": "प्रारंभिक संसर्ग", "gujarati": "પ્રારંભિક ચેપ", "punjabi": "ਸ਼ੁਰੂਆਤੀ ਲਾਗ", "odia": "ପ୍ରାରମ୍ଭିକ ସଂକ୍ରମଣ"},
    "Pre-planting": {
        "tamil": "நடவு செய்வதற்கு முன்", "telugu": "నాటడానికి ముందు", "kannada": "ನಾಟುವ ಮೊದಲು", "malayalam": "നടീലിന് മുമ്പ്", "hindi": "रोपाई से पहले", "bengali": "রোপণের আগে", "marathi": "लागवडीपूर्वी", "gujarati": "વાવણી પહેલાં", "punjabi": "ਬਿਜਾਈ ਤੋਂ ਪਹਿਲਾਂ", "odia": "ରୋପଣ ପୂର୍ବରୁ"},
    "Nutrient-deficiency stage": {
        "tamil": "ஊட்டச்சத்து குறைபாடு நிலை", "telugu": "పోషక లోప దశ", "kannada": "ಪೋಷಕಾಂಶ ಕೊರತೆ ಹಂತ", "malayalam": "പോഷക കുറവ് ഘട്ടം", "hindi": "पोषक तत्वों की कमी का चरण", "bengali": "পুষ্টির ঘাটতির পর্যায়", "marathi": "पोषक घटकांची कमतरता अवस्था", "gujarati": "પોષક તત્ત્વોની ઉણપનો તબક્કો", "punjabi": "ਪੋਸ਼ਕ ਤੱਤਾਂ ਦੀ ਘਾਟ ਦਾ ਪੜਾਅ", "odia": "ପୋଷକ ଅଭାବ ପର୍ଯ୍ୟାୟ"},
    "Pre-planting / ongoing": {
        "tamil": "நடவுக்கு முன் / தொடர்ந்து", "telugu": "నాటడానికి ముందు / కొనసాగింపు", "kannada": "ನಾಟುವ ಮೊದಲು / ಮುಂದುವರಿಕೆ", "malayalam": "നടീലിന് മുമ്പ് / തുടർച്ചയായി", "hindi": "रोपाई से पहले / जारी", "bengali": "রোপণের আগে / চলমান", "marathi": "लागवडीपूर्वी / सुरू", "gujarati": "વાવણી પહેલાં / ચાલુ", "punjabi": "ਬਿਜਾਈ ਤੋਂ ਪਹਿਲਾਂ / ਜਾਰੀ", "odia": "ରୋପଣ ପୂର୍ବରୁ / ଚାଲୁ"},
    "Active infection": {
        "tamil": "செயலில் உள்ள தொற்று", "telugu": "క్రియాశీల సంక్రమణ", "kannada": "ಸಕ್ರಿಯ ಸೋಂಕು", "malayalam": "സജീവ അണുബാധ", "hindi": "सक्रिय संक्रमण", "bengali": "সক্রিয় সংক্রমণ", "marathi": "सक्रिय संसर्ग", "gujarati": "સક્રિય ચેપ", "punjabi": "ਸਰਗਰਮ ਲਾਗ", "odia": "ସକ୍ରିୟ ସଂକ୍ରମଣ"},
    "Vector (leafhopper) presence": {
        "tamil": "பரப்பி (இலைத்தத்துப்பூச்சி) இருப்பு", "telugu": "వాహక (ఆకుదూకుడు) ఉనికి", "kannada": "ವಾಹಕ (ಎಲೆ ಜಿಗಿತ ಕೀಟ) ಇರುವಿಕೆ", "malayalam": "വാഹക (ഇലച്ചാടി) സാന്നിധ്യം", "hindi": "वाहक (लीफहॉपर) की उपस्थिति", "bengali": "বাহক (লিফহপার) উপস্থিতি", "marathi": "वाहक (तुडतुडा) उपस्थिती", "gujarati": "વાહક (લીફહોપર)ની હાજરી", "punjabi": "ਵਾਹਕ (ਲੀਫਹੌਪਰ) ਦੀ ਮੌਜੂਦਗੀ", "odia": "ବାହକ (ଲିଫହପର) ଉପସ୍ଥିତି"},
    "Vector deterrence": {
        "tamil": "பரப்பியைத் தடுப்பது", "telugu": "వాహక నియంత్రణ", "kannada": "ವಾಹಕ ನಿಯಂತ್ರಣ", "malayalam": "വാഹക നിയന്ത്രണം", "hindi": "वाहक नियंत्रण", "bengali": "বাহক নিয়ন্ত্রণ", "marathi": "वाहक नियंत्रण", "gujarati": "વાહક નિયંત્રણ", "punjabi": "ਵਾਹਕ ਨਿਯੰਤਰਣ", "odia": "ବାହକ ନିୟନ୍ତ୍ରଣ"},
    "Panicle initiation": {
        "tamil": "கதிர் தொடக்க நிலை", "telugu": "కంకి ప్రారంభ దశ", "kannada": "ತೆನೆ ಆರಂಭ ಹಂತ", "malayalam": "കതിർ ആരംഭ ഘട്ടം", "hindi": "बालियों के आरंभ का चरण", "bengali": "শীষ শুরু হওয়ার পর্যায়", "marathi": "कणसांची सुरुवात अवस्था", "gujarati": "ડૂંડા શરૂ થવાનો તબક્કો", "punjabi": "ਬਾਲੀ ਸ਼ੁਰੂਆਤ ਪੜਾਅ", "odia": "ଶୀଷ ଆରମ୍ଭ ପର୍ଯ୍ୟାୟ"},
    "Pre-sowing": {
        "tamil": "விதைப்பதற்கு முன்", "telugu": "విత్తే ముందు", "kannada": "ಬಿತ್ತುವ ಮೊದಲು", "malayalam": "വിതയ്ക്കുന്നതിന് മുമ്പ്", "hindi": "बुवाई से पहले", "bengali": "বপনের আগে", "marathi": "पेरणीपूर्वी", "gujarati": "વાવણી પહેલાં", "punjabi": "ਬਿਜਾਈ ਤੋਂ ਪਹਿਲਾਂ", "odia": "ବୁଣିବା ପୂର୍ବରୁ"},
    "Larval boring stage": {
        "tamil": "புழு துளைக்கும் நிலை", "telugu": "లార్వా తొలిచే దశ", "kannada": "ಲಾರ್ವಾ ಕೊರೆಯುವ ಹಂತ", "malayalam": "ലാർവ തുരപ്പൻ ഘട്ടം", "hindi": "लार्वा तना छेदने का चरण", "bengali": "লার্ভা ছিদ্র করার পর্যায়", "marathi": "अळी छिद्र करण्याची अवस्था", "gujarati": "લાર્વા છિદ્ર કરવાની અવસ્થા", "punjabi": "ਲਾਰਵਾ ਦੇ ਛੇਦ ਕਰਨ ਦਾ ਪੜਾਅ", "odia": "ଲାର୍ଭା ଛିଦ୍ର କରିବା ପର୍ଯ୍ୟାୟ"},
    "Egg-laying stage (preventive)": {
        "tamil": "முட்டையிடும் நிலை (தடுப்பு)", "telugu": "గుడ్లు పెట్టే దశ (నివారణ)", "kannada": "ಮೊಟ್ಟೆ ಇಡುವ ಹಂತ (ತಡೆಗಟ್ಟುವಿಕೆ)", "malayalam": "മുട്ടയിടൽ ഘട്ടം (പ്രതിരോധം)", "hindi": "अंडे देने का चरण (रोकथाम)", "bengali": "ডিম পাড়ার পর্যায় (প্রতিরোধ)", "marathi": "अंडी घालण्याची अवस्था (प्रतिबंध)", "gujarati": "ઈંડા મૂકવાનો તબક્કો (નિવારણ)", "punjabi": "ਅੰਡੇ ਦੇਣ ਦਾ ਪੜਾਅ (ਰੋਕਥਾਮ)", "odia": "ଅଣ୍ଡା ଦେବା ପର୍ଯ୍ୟାୟ (ପ୍ରତିରୋଧ)"},
    "Nursery stage": {
        "tamil": "நாற்றங்கால் நிலை", "telugu": "నర్సరీ దశ", "kannada": "ನರ್ಸರಿ ಹಂತ", "malayalam": "നഴ്സറി ഘട്ടം", "hindi": "नर्सरी चरण", "bengali": "নার্সারি পর্যায়", "marathi": "रोपवाटिका अवस्था", "gujarati": "નર્સરી તબક્કો", "punjabi": "ਨਰਸਰੀ ਪੜਾਅ", "odia": "ନର୍ସରୀ ପର୍ଯ୍ୟାୟ"},
    "Active infestation": {
        "tamil": "செயலில் உள்ள பூச்சித் தாக்குதல்", "telugu": "క్రియాశీల పురుగు దాడి", "kannada": "ಸಕ್ರಿಯ ಕೀಟ ಬಾಧೆ", "malayalam": "സജീവ ബാധ", "hindi": "सक्रिय कीट प्रकोप", "bengali": "সক্রিয় পোকার আক্রমণ", "marathi": "सक्रिय कीड प्रादुर्भाव", "gujarati": "સક્રિય જીવાત ઉપદ્રવ", "punjabi": "ਸਰਗਰਮ ਕੀਟ ਹਮਲਾ", "odia": "ସକ୍ରିୟ କୀଟ ଆକ୍ରମଣ"},
    "Early infestation": {
        "tamil": "ஆரம்ப பூச்சித் தாக்குதல்", "telugu": "ప్రారంభ పురుగు దాడి", "kannada": "ಆರಂಭಿಕ ಕೀಟ ಬಾಧೆ", "malayalam": "പ്രാരംഭ ബാധ", "hindi": "प्रारंभिक कीट प्रकोप", "bengali": "প্রাথমিক পোকার আক্রমণ", "marathi": "प्रारंभिक कीड प्रादुर्भाव", "gujarati": "પ્રારંભિક જીવાત ઉપદ્રવ", "punjabi": "ਸ਼ੁਰੂਆਤੀ ਕੀਟ ਹਮਲਾ", "odia": "ପ୍ରାରମ୍ଭିକ କୀଟ ଆକ୍ରମଣ"},
    "Waterlogging risk stage": {
        "tamil": "நீர் தேக்க அபாய நிலை", "telugu": "నీరు నిలిచే ప్రమాద దశ", "kannada": "ನೀರು ನಿಲ್ಲುವ ಅಪಾಯದ ಹಂತ", "malayalam": "വെള്ളക്കെട്ട് അപകട ഘട്ടം", "hindi": "जलभराव जोखिम चरण", "bengali": "জলাবদ্ধতার ঝুঁকির পর্যায়", "marathi": "पाणी साचण्याचा धोका", "gujarati": "પાણી ભરાવાનો જોખમ તબક્કો", "punjabi": "ਪਾਣੀ ਖੜ੍ਹਨ ਦਾ ਜੋਖਮ ਪੜਾਅ", "odia": "ଜଳ ଜମିବା ବିପଦ ପର୍ଯ୍ୟାୟ"},
    "Wet-weather active infection": {
        "tamil": "மழைக்கால செயலில் உள்ள தொற்று", "telugu": "తడి వాతావరణ క్రియాశీల సంక్రమణ", "kannada": "ತೇವ ಹವಾಮಾನ ಸಕ್ರಿಯ ಸೋಂಕು", "malayalam": "മഴക്കാല സജീവ അണുബാധ", "hindi": "नम मौसम में सक्रिय संक्रमण", "bengali": "ভেজা আবহাওয়ায় সক্রিয় সংক্রমণ", "marathi": "ओलसर हवामानातील सक्रिय संसर्ग", "gujarati": "ભીના હવામાનનો સક્રિય ચેપ", "punjabi": "ਨਮੀ ਵਾਲੇ ਮੌਸਮ ਦੀ ਸਰਗਰਮ ਲਾਗ", "odia": "ଆର୍ଦ୍ର ପାଗର ସକ୍ରିୟ ସଂକ୍ରମଣ"},
    "N/A": {
        "tamil": "பொருந்தாது", "telugu": "వర్తించదు", "kannada": "ಅನ್ವಯಿಸುವುದಿಲ್ಲ", "malayalam": "ബാധകമല്ല", "hindi": "लागू नहीं", "bengali": "প্রযোজ্য নয়", "marathi": "लागू नाही", "gujarati": "લાગુ પડતું નથી", "punjabi": "ਲਾਗੂ ਨਹੀਂ", "odia": "ଲାଗୁ ହୁଏ ନାହିଁ"},
}

_TREATMENT_NAME_RAW = {
    # Chemical/fungicide names kept as-is; only translating the
    # plain-language action names (non-chemical practices).
    "Remove & destroy infected plants":         {"malayalam": "രോഗം ബാധിച്ച ചെടികൾ നീക്കം ചെയ്ത് നശിപ്പിക്കുക"},
    "Neem-based pesticide":                     {"malayalam": "വേപ്പ് അധിഷ്ഠിത കീടനാശിനി"},
    "Hot-water seed treatment (52°C, 10 min)":  {"malayalam": "ചൂടുവെള്ള വിത്ത് ചികിത്സ (52°C, 10 മിനിറ്റ്)"},
    "Certified disease-free seed":              {"malayalam": "സാക്ഷ്യപ്പെടുത്തിയ രോഗരഹിത വിത്ത്"},
    "Trichogramma japonicum (biological)":      {"malayalam": "ട്രൈക്കോഗ്രാമ ജപ്പോണിക്കം (ജൈവ നിയന്ത്രണം)"},
    "Clip & destroy egg masses":                {"malayalam": "മുട്ടക്കൂട്ടങ്ങൾ മുറിച്ച് നശിപ്പിക്കുക"},
    "Hand-picking adults":                      {"malayalam": "പ്രാണികളെ കൈകൊണ്ട് പെറുക്കിമാറ്റുക"},
    "Field drainage improvement":               {"malayalam": "വയൽ നീർവാർച്ച മെച്ചപ്പെടുത്തൽ"},
    "No treatment required":                    {"malayalam": "ചികിത്സ ആവശ്യമില്ല"},
    "Zinc Sulphate foliar spray (0.5%)":        {"malayalam": "സിങ്ക് സൾഫേറ്റ് ഇല തളി (0.5%)"},
    "Balanced NPK + FYM":                       {"malayalam": "സമീകൃത NPK + കാലിവളം"},
    "Resistant varieties (ADT 43, CO 51)":      {"malayalam": "പ്രതിരോധശേഷിയുള്ള ഇനങ്ങൾ (ADT 43, CO 51)"},
    "Resistant varieties (IR64, Swarna Sub1)":  {"malayalam": "പ്രതിരോധശേഷിയുള്ള ഇനങ്ങൾ (IR64, Swarna Sub1)"},
}


def translate_treatment_name(name: str, lang: str) -> str:
    """Translate a treatment 'name' field. Chemical names pass through unchanged."""
    lang = resolve_lang(lang)
    block = _TREATMENT_NAME_RAW.get(name)
    if block is None:
        return name
    return _pick_or(block, lang, name)


def translate_treatment_stage(stage: str, lang: str) -> str:
    """Translate a treatment 'stage' field."""
    lang = resolve_lang(lang)
    block = _TREATMENT_STAGE_RAW.get(stage)
    if block is None:
        return stage
    return _pick_or(block, lang, stage)


# ═══════════════════════════════════════════════════════════════
# RISK BADGE + ACTION MESSAGES
# ═══════════════════════════════════════════════════════════════
_RISK_RAW = {
    "high":   {"english": "HIGH", "tamil": "அதிக அபாயம்", "telugu": "అధిక ప్రమాదం", "kannada": "ಹೆಚ್ಚಿನ ಅಪಾಯ",
               "malayalam": "ഉയർന്ന അപകടം", "hindi": "उच्च जोखिम", "bengali": "উচ্চ ঝুঁকি", "marathi": "उच्च धोका",
               "gujarati": "ઉચ્ચ જોખમ", "punjabi": "ਉੱਚ ਜੋਖਮ", "odia": "ଉଚ୍ଚ ବିପଦ"},
    "medium": {"english": "MEDIUM", "tamil": "நடுத்தர அபாயம்", "telugu": "మధ్యస్థ ప్రమాదం", "kannada": "ಮಧ್ಯಮ ಅಪಾಯ",
               "malayalam": "ഇടത്തരം അപകടം", "hindi": "मध्यम जोखिम", "bengali": "মাঝারি ঝুঁকি", "marathi": "मध्यम धोका",
               "gujarati": "મધ્યમ જોખમ", "punjabi": "ਦਰਮਿਆਨਾ ਜੋਖਮ", "odia": "ମଧ୍ୟମ ବିପଦ"},
    "low":    {"english": "LOW", "tamil": "குறைந்த அபாயம்", "telugu": "తక్కువ ప్రమాదం", "kannada": "ಕಡಿಮೆ ಅಪಾಯ",
               "malayalam": "കുറഞ്ഞ അപകടം", "hindi": "कम जोखिम", "bengali": "কম ঝুঁকি", "marathi": "कमी धोका",
               "gujarati": "ઓછું જોખમ", "punjabi": "ਘੱਟ ਜੋਖਮ", "odia": "କମ ବିପଦ"},
}

_ACTION_RAW = {
    "healthy": {
        "english": "Crop looks healthy — routine monitoring sufficient",
        "tamil": "பயிர் ஆரோக்கியமாக உள்ளது — வழக்கமான கண்காணிப்பு போதுமானது",
        "telugu": "పంట ఆరోగ్యంగా ఉంది — సాధారణ పర్యవేక్షణ సరిపోతుంది",
        "kannada": "ಬೆಳೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ — ನಿಯಮಿತ ಮೇಲ್ವಿಚಾರಣೆ ಸಾಕು",
        "malayalam": "വിള ആരോഗ്യകരമാണ് — പതിവ് നിരീക്ഷണം മതി",
        "hindi": "फसल स्वस्थ दिख रही है — नियमित निगरानी पर्याप्त है",
        "bengali": "ফসল সুস্থ দেখাচ্ছে — নিয়মিত পর্যবেক্ষণই যথেষ্ট",
        "marathi": "पीक निरोगी दिसत आहे — नियमित निरीक्षण पुरेसे आहे",
        "gujarati": "પાક તંદુરસ્ત દેખાય છે — નિયમિત દેખરેખ પૂરતી છે",
        "punjabi": "ਫਸਲ ਤੰਦਰੁਸਤ ਲੱਗ ਰਹੀ ਹੈ — ਨਿਯਮਤ ਨਿਗਰਾਨੀ ਕਾਫ਼ੀ ਹੈ",
        "odia": "ଫସଲ ସୁସ୍ଥ ଦେଖାଯାଉଛି — ନିୟମିତ ନିରୀକ୍ଷଣ ଯଥେଷ୍ଟ",
    },
    "high": {
        "english": "Immediate action required within 24 hrs",
        "tamil": "24 மணி நேரத்தில் உடனடி நடவடிக்கை தேவை",
        "telugu": "24 గంటల్లో తక్షణ చర్య అవసరం",
        "kannada": "24 ಗಂಟೆಗಳಲ್ಲಿ ತಕ್ಷಣದ ಕ್ರಮ ಅಗತ್ಯ",
        "malayalam": "24 മണിക്കൂറിനുള്ളിൽ ഉടനടി നടപടി ആവശ്യമാണ്",
        "hindi": "24 घंटों के भीतर तुरंत कार्रवाई आवश्यक है",
        "bengali": "২৪ ঘণ্টার মধ্যে তাৎক্ষণিক ব্যবস্থা প্রয়োজন",
        "marathi": "24 तासांच्या आत तातडीने कारवाई आवश्यक आहे",
        "gujarati": "24 કલાકમાં તાત્કાલિક પગલાં જરૂરી છે",
        "punjabi": "24 ਘੰਟਿਆਂ ਵਿੱਚ ਤੁਰੰਤ ਕਾਰਵਾਈ ਜ਼ਰੂਰੀ ਹੈ",
        "odia": "24 ଘଣ୍ଟା ମଧ୍ୟରେ ତୁରନ୍ତ ପଦକ୍ଷେପ ଆବଶ୍ୟକ",
    },
    "medium": {
        "english": "Monitor and treat within 3 days",
        "tamil": "3 நாட்களுக்குள் கண்காணித்து சிகிச்சை அளிக்கவும்",
        "telugu": "3 రోజుల్లో పరిశీలించి చికిత్స చేయండి",
        "kannada": "3 ದಿನಗಳಲ್ಲಿ ಗಮನಿಸಿ ಚಿಕಿತ್ಸೆ ನೀಡಿ",
        "malayalam": "3 ദിവസത്തിനുള്ളിൽ നിരീക്ഷിച്ച് ചികിത്സിക്കുക",
        "hindi": "3 दिनों के भीतर निगरानी कर उपचार करें",
        "bengali": "৩ দিনের মধ্যে পর্যবেক্ষণ করে চিকিৎসা করুন",
        "marathi": "3 दिवसांत निरीक्षण करून उपचार करा",
        "gujarati": "3 દિવસમાં દેખરેખ રાખી સારવાર કરો",
        "punjabi": "3 ਦਿਨਾਂ ਵਿੱਚ ਨਿਗਰਾਨੀ ਕਰਕੇ ਇਲਾਜ ਕਰੋ",
        "odia": "3 ଦିନ ମଧ୍ୟରେ ନିରୀକ୍ଷଣ କରି ଚିକିତ୍ସା କରନ୍ତୁ",
    },
    "low": {
        "english": "Routine monitoring sufficient",
        "tamil": "வழக்கமான கண்காணிப்பு போதுமானது",
        "telugu": "సాధారణ పర్యవేక్షణ సరిపోతుంది",
        "kannada": "ನಿಯಮಿತ ಮೇಲ್ವಿಚಾರಣೆ ಸಾಕು",
        "malayalam": "പതിവ് നിരീക്ഷണം മതി",
        "hindi": "नियमित निगरानी पर्याप्त है",
        "bengali": "নিয়মিত পর্যবেক্ষণই যথেষ্ট",
        "marathi": "नियमित निरीक्षण पुरेसे आहे",
        "gujarati": "નિયમિત દેખરેખ પૂરતી છે",
        "punjabi": "ਨਿਯਮਤ ਨਿਗਰਾਨੀ ਕਾਫ਼ੀ ਹੈ",
        "odia": "ନିୟମିତ ନିରୀକ୍ଷଣ ଯଥେଷ୍ଟ",
    },
}


def risk_label(level: str, lang: str) -> str:
    lang = resolve_lang(lang)
    return _pick(_RISK_RAW.get(level, _RISK_RAW["low"]), lang)


def action_text(level: str, lang: str) -> str:
    lang = resolve_lang(lang)
    return _pick(_ACTION_RAW.get(level, _ACTION_RAW["low"]), lang)


# ═══════════════════════════════════════════════════════════════
# CHATBOT UI STRINGS (greeting + quick-question buttons)
# ═══════════════════════════════════════════════════════════════
_GREETING_RAW = {
    "english": "Hello! I'm your Smart Paddy AI assistant. Ask me about rice diseases, fertilizers, irrigation, pests, or harvest tips!",
    "tamil": "வணக்கம்! நான் ஸ்மார்ட் பேடி AI உதவியாளர். நெல் நோய்கள், உரம், நீர்ப்பாசனம் பற்றி கேளுங்கள்!",
    "telugu": "నమస్కారం! నేను స్మార్ట్ పాడీ AI సహాయకుడిని. వరి వ్యాధులు, ఎరువులు, నీటిపారుదల, పురుగుల గురించి అడగండి!",
    "kannada": "ನಮಸ್ಕಾರ! ನಾನು ಸ್ಮಾರ್ಟ್ ಪ್ಯಾಡಿ AI ಸಹಾಯಕ. ಭತ್ತದ ರೋಗಗಳು, ಗೊಬ್ಬರ, ನೀರಾವರಿ, ಕೀಟಗಳ ಬಗ್ಗೆ ಕೇಳಿ!",
    "malayalam": "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ സ്മാർട്ട് പാഡി AI സഹായി. നെല്ല് രോഗങ്ങൾ, വളം, ജലസേചനം, കീടങ്ങൾ എന്നിവയെക്കുറിച്ച് ചോദിക്കൂ!",
    "hindi": "नमस्ते! मैं आपका स्मार्ट पैडी AI सहायक हूँ। धान के रोगों, उर्वरक, सिंचाई, कीट या फसल कटाई के बारे में पूछें!",
    "bengali": "নমস্কার! আমি আপনার স্মার্ট প্যাডি AI সহায়ক। ধানের রোগ, সার, সেচ, পোকামাকড় নিয়ে জিজ্ঞাসা করুন!",
    "marathi": "नमस्कार! मी तुमचा स्मार्ट पॅडी AI सहाय्यक आहे. भाताचे रोग, खत, सिंचन, किडी याबद्दल विचारा!",
    "gujarati": "નમસ્તે! હું તમારો સ્માર્ટ પેડી AI સહાયક છું. ડાંગરના રોગો, ખાતર, સિંચાઈ, જીવાત વિશે પૂછો!",
    "punjabi": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਸਮਾਰਟ ਪੈਡੀ AI ਸਹਾਇਕ ਹਾਂ। ਝੋਨੇ ਦੀਆਂ ਬਿਮਾਰੀਆਂ, ਖਾਦ, ਸਿੰਚਾਈ, ਕੀੜਿਆਂ ਬਾਰੇ ਪੁੱਛੋ!",
    "odia": "ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କର ସ୍ମାର୍ଟ ପେଡି AI ସହାୟକ। ଧାନ ରୋଗ, ସାର, ଜଳସେଚନ, ପୋକ ବିଷୟରେ ପଚାରନ୍ତୁ!",
}

_QUICK_Q_RAW = {
    "english": ["How can I treat this disease?", "How can I prevent blast disease?", "What fertilizer schedule should I follow?", "What should I do during rainy conditions?", "What are common paddy diseases?", "How does the AI detect disease?", "What does the confidence score mean?", "How can I improve crop health?"],
    "tamil": ["இந்த நோயை எப்படி குணப்படுத்துவது?", "பிளாஸ்ட் நோயை எப்படி தடுப்பது?", "எந்த உர அட்டவணையை பின்பற்ற வேண்டும்?", "மழைக்காலத்தில் என்ன செய்ய வேண்டும்?", "பொதுவான நெல் நோய்கள் யாவை?", "AI நோயை எவ்வாறு கண்டறிகிறது?", "நம்பிக்கை மதிப்பெண் என்றால் என்ன?", "பயிர் ஆரோக்கியத்தை எவ்வாறு மேம்படுத்துவது?"],
    "telugu": ["ఈ వ్యాధికి ఎలా చికిత్స చేయాలి?", "బ్లాస్ట్ వ్యాధిని ఎలా నివారించాలి?", "ఏ ఎరువుల షెడ్యూల్ పాటించాలి?", "వర్షాకాలంలో ఏమి చేయాలి?", "సాధారణ వరి వ్యాధులు ఏమిటి?", "AI వ్యాధిని ఎలా గుర్తిస్తుంది?", "నమ్మకం స్కోర్ అంటే ఏమిటి?", "పంట ఆరోగ్యాన్ని ఎలా మెరుగుపరచాలి?"],
    "kannada": ["ಈ ರೋಗಕ್ಕೆ ಹೇಗೆ ಚಿಕಿತ್ಸೆ ನೀಡಬೇಕು?", "ಬ್ಲಾಸ್ಟ್ ರೋಗವನ್ನು ಹೇಗೆ ತಡೆಯಬೇಕು?", "ಯಾವ ಗೊಬ್ಬರ ವೇಳಾಪಟ್ಟಿ ಅನುಸರಿಸಬೇಕು?", "ಮಳೆಯ ಸಮಯದಲ್ಲಿ ಏನು ಮಾಡಬೇಕು?", "ಸಾಮಾನ್ಯ ಭತ್ತದ ರೋಗಗಳು ಯಾವುವು?", "AI ರೋಗವನ್ನು ಹೇಗೆ ಪತ್ತೆಹಚ್ಚುತ್ತದೆ?", "ವಿಶ್ವಾಸದ ಅಂಕ ಎಂದರೇನು?", "ಬೆಳೆ ಆರೋಗ್ಯವನ್ನು ಹೇಗೆ ಸುಧಾರಿಸಬೇಕು?"],
    "malayalam": ["ഈ രോഗം എങ്ങനെ ചികിത്സിക്കാം?", "ബ്ലാസ്റ്റ് രോഗം എങ്ങനെ തടയാം?", "ഏത് വളപ്രയോഗ ഷെഡ്യൂൾ പാലിക്കണം?", "മഴക്കാലത്ത് എന്ത് ചെയ്യണം?", "സാധാരണ നെൽ രോഗങ്ങൾ ഏതൊക്കെയാണ്?", "AI രോഗം എങ്ങനെ കണ്ടെത്തുന്നു?", "വിശ്വാസ്യതാ സ്കോർ എന്താണ്?", "വിള ആരോഗ്യം എങ്ങനെ മെച്ചപ്പെടുത്താം?"],
    "hindi": ["इस रोग का उपचार कैसे करें?", "ब्लास्ट रोग से कैसे बचें?", "कौन सा उर्वरक कार्यक्रम अपनाएं?", "बारिश के समय क्या करना चाहिए?", "धान के सामान्य रोग कौन से हैं?", "AI रोग की पहचान कैसे करता है?", "विश्वसनीयता स्कोर का क्या अर्थ है?", "फसल का स्वास्थ्य कैसे सुधारें?"],
    "bengali": ["এই রোগের চিকিৎসা কীভাবে করব?", "ব্লাস্ট রোগ কীভাবে প্রতিরোধ করব?", "কোন সার প্রয়োগের সময়সূচি মানতে হবে?", "বৃষ্টির সময় কী করা উচিত?", "সাধারণ ধানের রোগগুলি কী কী?", "AI কীভাবে রোগ শনাক্ত করে?", "নির্ভরযোগ্যতার স্কোরের অর্থ কী?", "ফসলের স্বাস্থ্য কীভাবে উন্নত করব?"],
    "marathi": ["या रोगावर उपचार कसा करावा?", "ब्लास्ट रोग कसा टाळावा?", "कोणते खत वेळापत्रक पाळावे?", "पावसाळ्यात काय करावे?", "भाताचे सामान्य रोग कोणते?", "AI रोग कसा ओळखतो?", "विश्वासार्हता गुणांचा अर्थ काय?", "पिकाचे आरोग्य कसे सुधारावे?"],
    "gujarati": ["આ રોગની સારવાર કેવી રીતે કરવી?", "બ્લાસ્ટ રોગથી કેવી રીતે બચવું?", "કયું ખાતર સમયપત્રક અનુસરવું?", "વરસાદ દરમિયાન શું કરવું?", "સામાન્ય ડાંગરના રોગો કયા છે?", "AI રોગને કેવી રીતે ઓળખે છે?", "વિશ્વાસ સ્કોરનો અર્થ શું છે?", "પાકનું આરોગ્ય કેવી રીતે સુધારવું?"],
    "punjabi": ["ਇਸ ਬਿਮਾਰੀ ਦਾ ਇਲਾਜ ਕਿਵੇਂ ਕਰੀਏ?", "ਬਲਾਸਟ ਬਿਮਾਰੀ ਤੋਂ ਕਿਵੇਂ ਬਚੀਏ?", "ਕਿਹੜੀ ਖਾਦ ਸਮਾਂ-ਸਾਰਣੀ ਅਪਣਾਈਏ?", "ਮੀਂਹ ਦੌਰਾਨ ਕੀ ਕਰਨਾ ਚਾਹੀਦਾ ਹੈ?", "ਝੋਨੇ ਦੀਆਂ ਆਮ ਬਿਮਾਰੀਆਂ ਕਿਹੜੀਆਂ ਹਨ?", "AI ਬਿਮਾਰੀ ਦੀ ਪਛਾਣ ਕਿਵੇਂ ਕਰਦਾ ਹੈ?", "ਭਰੋਸੇ ਦੇ ਸਕੋਰ ਦਾ ਕੀ ਅਰਥ ਹੈ?", "ਫਸਲ ਦੀ ਸਿਹਤ ਕਿਵੇਂ ਸੁਧਾਰੀਏ?"],
    "odia": ["ଏହି ରୋଗର ଚିକିତ୍ସା କିପରି କରିବି?", "ବ୍ଲାଷ୍ଟ ରୋଗକୁ କିପରି ରୋକିବି?", "କେଉଁ ସାର ସମୟସୂଚୀ ଅନୁସରଣ କରିବି?", "ବର୍ଷା ସମୟରେ କଣ କରିବି?", "ସାଧାରଣ ଧାନ ରୋଗଗୁଡ଼ିକ କଣ?", "AI ରୋଗକୁ କିପରି ଚିହ୍ନଟ କରେ?", "ବିଶ୍ୱାସ ସ୍କୋରର ଅର୍ଥ କଣ?", "ଫସଲର ସ୍ୱାସ୍ଥ୍ୟ କିପରି ଉନ୍ନତ କରିବି?"],
}


def chatbot_greeting(lang: str) -> str:
    lang = resolve_lang(lang)
    return _pick(_GREETING_RAW, lang)


def quick_questions(lang: str) -> list[str]:
    lang = resolve_lang(lang)
    return _QUICK_Q_RAW.get(lang, _QUICK_Q_RAW["english"])


# ═══════════════════════════════════════════════════════════════
# TREATMENT-TABLE ENUM TRANSLATIONS (cost / eco-friendly / priority)
# ═══════════════════════════════════════════════════════════════
_ENUM_RAW = {
    "Low":      {"english": "Low", "tamil": "குறைவு", "telugu": "తక్కువ", "kannada": "ಕಡಿಮೆ", "malayalam": "കുറവ്",
                 "hindi": "कम", "bengali": "কম", "marathi": "कमी", "gujarati": "ઓછું", "punjabi": "ਘੱਟ", "odia": "କମ"},
    "Medium":   {"english": "Medium", "tamil": "நடுத்தரம்", "telugu": "మధ్యస్థం", "kannada": "ಮಧ್ಯಮ", "malayalam": "ഇടത്തരം",
                 "hindi": "मध्यम", "bengali": "মাঝারি", "marathi": "मध्यम", "gujarati": "મધ્યમ", "punjabi": "ਦਰਮਿਆਨਾ", "odia": "ମଧ୍ୟମ"},
    "High":     {"english": "High", "tamil": "அதிகம்", "telugu": "అధికం", "kannada": "ಹೆಚ್ಚು", "malayalam": "കൂടുതൽ",
                 "hindi": "उच्च", "bengali": "উচ্চ", "marathi": "जास्त", "gujarati": "ઊંચું", "punjabi": "ਵੱਧ", "odia": "ଅଧିକ"},
    "None":     {"english": "None", "tamil": "இல்லை", "telugu": "లేదు", "kannada": "ಇಲ್ಲ", "malayalam": "ഇല്ല",
                 "hindi": "कोई नहीं", "bengali": "নেই", "marathi": "काहीही नाही", "gujarati": "કંઈ નહીં", "punjabi": "ਕੋਈ ਨਹੀਂ", "odia": "କିଛି ନାହିଁ"},
    "Urgent":   {"english": "Urgent", "tamil": "அவசரம்", "telugu": "అత్యవసరం", "kannada": "ತುರ್ತು", "malayalam": "അടിയന്തിരം",
                 "hindi": "तत्काल", "bengali": "জরুরি", "marathi": "तातडीचे", "gujarati": "તાત્કાલિક", "punjabi": "ਜ਼ਰੂਰੀ", "odia": "ଜରୁରୀ"},
    "N/A":      {"english": "N/A", "tamil": "பொருந்தாது", "telugu": "వర్తించదు", "kannada": "ಅನ್ವಯಿಸುವುದಿಲ್ಲ",
                 "malayalam": "ബാധകമല്ല", "hindi": "लागू नहीं", "bengali": "প্রযোজ্য নয়", "marathi": "लागू नाही",
                 "gujarati": "લાગુ નથી", "punjabi": "ਲਾਗੂ ਨਹੀਂ", "odia": "ପ୍ରଯୁଜ୍ୟ ନୁହେଁ"},
    "Preventive": {"english": "Preventive", "tamil": "தடுப்பு நடவடிக்கை", "telugu": "నివారణ చర్య", "kannada": "ತಡೆಗಟ್ಟುವ ಕ್ರಮ",
                 "malayalam": "പ്രതിരോധ നടപടി", "hindi": "निवारक", "bengali": "প্রতিরোধমূলক", "marathi": "प्रतिबंधात्मक",
                 "gujarati": "નિવારક", "punjabi": "ਰੋਕਥਾਮ ਵਾਲਾ", "odia": "ପ୍ରତିରୋଧାତ୍ମକ"},

    # ── Severity levels (utils/severity.py) ─────────────────────
    "Mild":     {"english": "Mild", "tamil": "லேசான", "telugu": "స్వల్ప", "kannada": "ಸೌಮ್ಯ", "malayalam": "ലഘുവായ",
                 "hindi": "हल्का", "bengali": "মৃদু", "marathi": "सौम्य", "gujarati": "હળવું", "punjabi": "ਹਲਕਾ", "odia": "ମୃଦୁ"},
    "Moderate": {"english": "Moderate", "tamil": "நடுத்தரம்", "telugu": "మధ్యస్థం", "kannada": "ಮಧ್ಯಮ", "malayalam": "മിതമായ",
                 "hindi": "मध्यम", "bengali": "মাঝারি", "marathi": "मध्यम", "gujarati": "મધ્યમ", "punjabi": "ਦਰਮਿਆਨਾ", "odia": "ମଧ୍ୟମ"},
    "Severe":   {"english": "Severe", "tamil": "கடுமையான", "telugu": "తీవ్రమైన", "kannada": "ತೀವ್ರ", "malayalam": "ഗുരുതരമായ",
                 "hindi": "गंभीर", "bengali": "তীব্র", "marathi": "गंभीर", "gujarati": "ગંભીર", "punjabi": "ਗੰਭੀਰ", "odia": "ଗମ୍ଭୀର"},

    # ── Health / quality categories (utils/severity.py) ──────────
    "Excellent": {"english": "Excellent", "tamil": "மிகச் சிறந்தது", "telugu": "అద్భుతం", "kannada": "ಅತ್ಯುತ್ತಮ",
                 "malayalam": "മികച്ചത്", "hindi": "उत्कृष्ट", "bengali": "চমৎকার", "marathi": "उत्कृष्ट",
                 "gujarati": "ઉત્તમ", "punjabi": "ਸ਼ਾਨਦਾਰ", "odia": "ଉତ୍କୃଷ୍ଟ"},
    "Good":      {"english": "Good", "tamil": "நல்லது", "telugu": "మంచిది", "kannada": "ಉತ್ತಮ", "malayalam": "നല്ലത്",
                 "hindi": "अच्छा", "bengali": "ভালো", "marathi": "चांगले", "gujarati": "સારું", "punjabi": "ਚੰਗਾ", "odia": "ଭଲ"},
    "Fair":      {"english": "Fair", "tamil": "சராசரி", "telugu": "సాధారణం", "kannada": "ಸಾಧಾರಣ", "malayalam": "സാമാന്യം",
                 "hindi": "सामान्य", "bengali": "মোটামুটি", "marathi": "सामान्य", "gujarati": "સામાન્ય", "punjabi": "ਦਰਮਿਆਨਾ", "odia": "ସାଧାରଣ"},
    "Poor":      {"english": "Poor", "tamil": "மோசமானது", "telugu": "పేలవం", "kannada": "ಕಳಪೆ", "malayalam": "മോശം",
                 "hindi": "खराब", "bengali": "খারাপ", "marathi": "वाईट", "gujarati": "નબળું", "punjabi": "ਮਾੜਾ", "odia": "ଖରାପ"},
    "Not Applicable": {"english": "Not Applicable", "tamil": "பொருந்தாது", "telugu": "వర్తించదు", "kannada": "ಅನ್ವಯಿಸುವುದಿಲ್ಲ",
                 "malayalam": "ബാധകമല്ല", "hindi": "लागू नहीं", "bengali": "প্রযোজ্য নয়", "marathi": "लागू नाही",
                 "gujarati": "લાગુ નથી", "punjabi": "ਲਾਗੂ ਨਹੀਂ", "odia": "ପ୍ରଯୁଜ୍ୟ ନୁହେଁ"},

    # ── Grad-CAM focus / location labels (utils/explainability.py) ─
    "Focused":            {"english": "Focused", "tamil": "குவிமையம்", "telugu": "కేంద్రీకృతం", "kannada": "ಕೇಂದ್ರೀಕೃತ",
                 "malayalam": "കേന്ദ്രീകൃതം", "hindi": "केंद्रित", "bengali": "কেন্দ্রীভূত", "marathi": "केंद्रित",
                 "gujarati": "કેન્દ્રિત", "punjabi": "ਕੇਂਦਰਿਤ", "odia": "କେନ୍ଦ୍ରୀଭୂତ"},
    "Moderately Focused": {"english": "Moderately Focused", "tamil": "மிதமான குவிமையம்", "telugu": "మధ్యస్తంగా కేంద్రీకృతం",
                 "kannada": "ಮಧ್ಯಮ ಕೇಂದ್ರೀಕೃತ", "malayalam": "മിതമായ കേന്ദ്രീകരണം", "hindi": "मध्यम रूप से केंद्रित",
                 "bengali": "মাঝারিভাবে কেন্দ্রীভূত", "marathi": "मध्यम प्रमाणात केंद्रित", "gujarati": "મધ્યમ કેન્દ્રિત",
                 "punjabi": "ਦਰਮਿਆਨਾ ਕੇਂਦਰਿਤ", "odia": "ମଧ୍ୟମ କେନ୍ଦ୍ରୀଭୂତ"},
    "Diffuse":            {"english": "Diffuse", "tamil": "பரவலான", "telugu": "వ్యాపించిన", "kannada": "ಹರಡಿದ",
                 "malayalam": "വ്യാപിച്ച", "hindi": "फैला हुआ", "bengali": "বিক্ষিপ্ত", "marathi": "विखुरलेले",
                 "gujarati": "ફેલાયેલું", "punjabi": "ਖਿੰਡਿਆ ਹੋਇਆ", "odia": "ବିଛିନ୍ନ"},
    "No Clear Focus":     {"english": "No Clear Focus", "tamil": "தெளிவான குவிமையம் இல்லை", "telugu": "స్పష్టమైన కేంద్రీకరణ లేదు",
                 "kannada": "ಸ್ಪಷ್ಟ ಕೇಂದ್ರೀಕರಣವಿಲ್ಲ", "malayalam": "വ്യക്തമായ കേന്ദ്രീകരണം ഇല്ല", "hindi": "स्पष्ट फोकस नहीं",
                 "bengali": "স্পষ্ট ফোকাস নেই", "marathi": "स्पष्ट फोकस नाही", "gujarati": "સ્પષ્ટ ફોકસ નથી",
                 "punjabi": "ਸਪਸ਼ਟ ਫੋਕਸ ਨਹੀਂ", "odia": "ସ୍ପଷ୍ଟ ଫୋକସ ନାହିଁ"},
    "Leaf Tip":           {"english": "Leaf Tip", "tamil": "இலை நுனி", "telugu": "ఆకు కొన", "kannada": "ಎಲೆ ತುದಿ",
                 "malayalam": "ഇല അഗ്രം", "hindi": "पत्ती की नोक", "bengali": "পাতার আগা", "marathi": "पानाचे टोक",
                 "gujarati": "પાનની ટોચ", "punjabi": "ਪੱਤੇ ਦੀ ਨੋਕ", "odia": "ପତ୍ର ଅଗ୍ରଭାଗ"},
    "Leaf Center":        {"english": "Leaf Center", "tamil": "இலை மையம்", "telugu": "ఆకు మధ్యభాగం", "kannada": "ಎಲೆ ಕೇಂದ್ರ",
                 "malayalam": "ഇല മധ്യഭാഗം", "hindi": "पत्ती का केंद्र", "bengali": "পাতার কেন্দ্র", "marathi": "पानाचे केंद्र",
                 "gujarati": "પાનનું કેન્દ્ર", "punjabi": "ਪੱਤੇ ਦਾ ਕੇਂਦਰ", "odia": "ପତ୍ର କେନ୍ଦ୍ର"},
    "Leaf Edge":          {"english": "Leaf Edge", "tamil": "இலை விளிம்பு", "telugu": "ఆకు అంచు", "kannada": "ಎಲೆ ಅಂಚು",
                 "malayalam": "ഇല അരികുകൾ", "hindi": "पत्ती का किनारा", "bengali": "পাতার কিনারা", "marathi": "पानाची कड",
                 "gujarati": "પાનની ધાર", "punjabi": "ਪੱਤੇ ਦਾ ਕਿਨਾਰਾ", "odia": "ପତ୍ର କଡ଼"},
    "Multiple Regions":   {"english": "Multiple Regions", "tamil": "பல பகுதிகள்", "telugu": "బహుళ ప్రాంతాలు",
                 "kannada": "ಬಹು ಪ್ರದೇಶಗಳು", "malayalam": "ഒന്നിലധികം ഭാഗങ്ങൾ", "hindi": "कई क्षेत्र",
                 "bengali": "একাধিক অঞ্চল", "marathi": "अनेक भाग", "gujarati": "બહુવિધ વિસ્તારો",
                 "punjabi": "ਕਈ ਖੇਤਰ", "odia": "ଏକାଧିକ ଅଞ୍ଚଳ"},
    "No Significant Activation": {"english": "No Significant Activation", "tamil": "குறிப்பிடத்தக்க செயல்பாடு இல்லை",
                 "telugu": "గణనీయమైన యాక్టివేషన్ లేదు", "kannada": "ಗಮನಾರ್ಹ ಆಕ್ಟಿವೇಶನ್ ಇಲ್ಲ",
                 "malayalam": "ശ്രദ്ധേയമായ ആക്റ്റിവേഷൻ ഇല്ല", "hindi": "कोई महत्वपूर्ण सक्रियण नहीं",
                 "bengali": "উল্লেখযোগ্য সক্রিয়তা নেই", "marathi": "लक्षणीय सक्रियता नाही", "gujarati": "નોંધપાત્ર સક્રિયકરણ નથી",
                 "punjabi": "ਕੋਈ ਖਾਸ ਐਕਟੀਵੇਸ਼ਨ ਨਹੀਂ", "odia": "କୌଣସି ଉଲ୍ଲେଖନୀୟ ସକ୍ରିୟତା ନାହିଁ"},
    "Unavailable":        {"english": "Unavailable", "tamil": "கிடைக்கவில்லை", "telugu": "అందుబాటులో లేదు",
                 "kannada": "ಲಭ್ಯವಿಲ್ಲ", "malayalam": "ലഭ്യമല്ല", "hindi": "अनुपलब्ध", "bengali": "অনুপলব্ধ",
                 "marathi": "अनुपलब्ध", "gujarati": "અનુપલબ્ધ", "punjabi": "ਉਪਲਬਧ ਨਹੀਂ", "odia": "ଅନୁପଲବ୍ଧ"},

    # ── Lesion coverage labels (utils/explainability.py) ──────────
    "Localized (isolated lesions, <15% leaf area)": {
        "english": "Localized (isolated lesions, <15% leaf area)",
        "tamil": "குறுகிய பரவல் (தனித்த புண்கள், <15% இலைப் பரப்பு)",
        "telugu": "స్థానికం (వేరుపడిన గాయాలు, <15% ఆకు విస్తీర్ణం)",
        "kannada": "ಸ್ಥಳೀಯ (ಪ್ರತ್ಯೇಕ ಗಾಯಗಳು, <15% ಎಲೆ ಪ್ರದೇಶ)",
        "malayalam": "പ്രാദേശികം (ഒറ്റപ്പെട്ട മുറിവുകൾ, <15% ഇല വിസ്തൃതി)",
        "hindi": "स्थानीयकृत (पृथक घाव, <15% पत्ती क्षेत्र)",
        "bengali": "স্থানীয় (বিচ্ছিন্ন ক্ষত, <15% পাতা এলাকা)",
        "marathi": "स्थानिक (विलग जखमा, <15% पान क्षेत्र)",
        "gujarati": "સ્થાનિક (અલગ ઘા, <15% પાન વિસ્તાર)",
        "punjabi": "ਸਥਾਨਕ (ਵੱਖਰੇ ਜ਼ਖਮ, <15% ਪੱਤਾ ਖੇਤਰ)",
        "odia": "ସ୍ଥାନୀୟ (ପୃଥକ କ୍ଷତ, <15% ପତ୍ର କ୍ଷେତ୍ର)",
    },
    "Moderate spread (15–40% leaf area)": {
        "english": "Moderate spread (15–40% leaf area)",
        "tamil": "நடுத்தர பரவல் (15–40% இலைப் பரப்பு)",
        "telugu": "మధ్యస్థ వ్యాప్తి (15–40% ఆకు విస్తీర్ణం)",
        "kannada": "ಮಧ್ಯಮ ಹರಡುವಿಕೆ (15–40% ಎಲೆ ಪ್ರದೇಶ)",
        "malayalam": "മിതമായ വ്യാപനം (15–40% ഇല വിസ്തൃതി)",
        "hindi": "मध्यम प्रसार (15–40% पत्ती क्षेत्र)",
        "bengali": "মাঝারি বিস্তার (15–40% পাতা এলাকা)",
        "marathi": "मध्यम प्रसार (15–40% पान क्षेत्र)",
        "gujarati": "મધ્યમ ફેલાવો (15–40% પાન વિસ્તાર)",
        "punjabi": "ਦਰਮਿਆਨਾ ਫੈਲਾਅ (15–40% ਪੱਤਾ ਖੇਤਰ)",
        "odia": "ମଧ୍ୟମ ବିସ୍ତାର (15–40% ପତ୍ର କ୍ଷେତ୍ର)",
    },
    "Widespread (40–65% leaf area)": {
        "english": "Widespread (40–65% leaf area)",
        "tamil": "பரவலான (40–65% இலைப் பரப்பு)",
        "telugu": "విస్తృతం (40–65% ఆకు విస్తీర్ణం)",
        "kannada": "ವ್ಯಾಪಕ (40–65% ಎಲೆ ಪ್ರದೇಶ)",
        "malayalam": "വ്യാപകം (40–65% ഇല വിസ്തൃതി)",
        "hindi": "व्यापक (40–65% पत्ती क्षेत्र)",
        "bengali": "ব্যাপক (40–65% পাতা এলাকা)",
        "marathi": "व्यापक (40–65% पान क्षेत्र)",
        "gujarati": "વ્યાપક (40–65% પાન વિસ્તાર)",
        "punjabi": "ਵਿਆਪਕ (40–65% ਪੱਤਾ ਖੇਤਰ)",
        "odia": "ବ୍ୟାପକ (40–65% ପତ୍ର କ୍ଷେତ୍ର)",
    },
    "Extensive (>65% leaf area affected)": {
        "english": "Extensive (>65% leaf area affected)",
        "tamil": "மிகப்பரவலான (>65% இலைப் பரப்பு பாதிக்கப்பட்டது)",
        "telugu": "అత్యధిక వ్యాప్తి (>65% ఆకు విస్తీర్ణం ప్రభావితం)",
        "kannada": "ವ್ಯಾಪಕ (>65% ಎಲೆ ಪ್ರದೇಶ ಬಾಧಿತ)",
        "malayalam": "വിശാലമായ (>65% ഇല വിസ്തൃതി ബാധിച്ചു)",
        "hindi": "अत्यधिक (>65% पत्ती क्षेत्र प्रभावित)",
        "bengali": "ব্যাপক (>65% পাতা এলাকা আক্রান্ত)",
        "marathi": "अत्यधिक (>65% पान क्षेत्र प्रभावित)",
        "gujarati": "અતિ વ્યાપક (>65% પાન વિસ્તાર અસરગ્રસ્ત)",
        "punjabi": "ਬਹੁਤ ਜ਼ਿਆਦਾ (>65% ਪੱਤਾ ਖੇਤਰ ਪ੍ਰਭਾਵਿਤ)",
        "odia": "ଅତ୍ୟଧିକ (>65% ପତ୍ର କ୍ଷେତ୍ର ପ୍ରଭାବିତ)",
    },
}


def translate_enum(value: str, lang: str) -> str:
    """Translate short enum-style values (Low/Medium/High/etc). Unknown values pass through unchanged."""
    lang = resolve_lang(lang)
    block = _ENUM_RAW.get(value)
    if block is None:
        return value
    return _pick_or(block, lang, value)


# ═══════════════════════════════════════════════════════════════
# RESEARCH METRICS PAGE — capability-comparison dimensions & metric
# names (app.py: generate_model_capability_data / evaluation tables)
# ═══════════════════════════════════════════════════════════════
# Hand-written for all 11 languages, local dictionary only — no API
# calls. Model/architecture names (CNN, ResNet50, EfficientNetB0) are
# NOT translated anywhere in the app; only the metric/dimension labels
# below are.
_CAPABILITY_DIMENSIONS_RAW = [
    {"english": "Feature Extraction Depth", "tamil": "அம்ச பிரித்தெடுப்பு ஆழம்",
     "telugu": "ఫీచర్ ఎక్స్‌ట్రాక్షన్ లోతు", "kannada": "ವೈಶಿಷ್ಟ್ಯ ಹೊರತೆಗೆಯುವಿಕೆ ಆಳ",
     "malayalam": "ഫീച്ചർ എക്‌സ്ട്രാക്ഷൻ ആഴം", "hindi": "फीचर एक्सट्रैक्शन गहराई",
     "bengali": "ফিচার এক্সট্র্যাকশন গভীরতা", "marathi": "फीचर एक्सट्रॅक्शन खोली",
     "gujarati": "ફીચર એક્સટ્રેક્શન ઊંડાઈ", "punjabi": "ਫੀਚਰ ਐਕਸਟਰੈਕਸ਼ਨ ਡੂੰਘਾਈ", "odia": "ଫିଚର ଏକ୍ସଟ୍ରାକ୍ସନ ଗଭୀରତା"},
    {"english": "Parameter Efficiency", "tamil": "அளவுரு திறன்",
     "telugu": "పారామీటర్ సామర్థ్యం", "kannada": "ಪ್ಯಾರಾಮೀಟರ್ ದಕ್ಷತೆ",
     "malayalam": "പാരാമീറ്റർ കാര്യക്ഷമത", "hindi": "पैरामीटर दक्षता",
     "bengali": "প্যারামিটার দক্ষতা", "marathi": "पॅरामीटर कार्यक्षमता",
     "gujarati": "પેરામીટર કાર્યક્ષમતા", "punjabi": "ਪੈਰਾਮੀਟਰ ਕੁਸ਼ਲਤਾ", "odia": "ପାରାମିଟର ଦକ୍ଷତା"},
    {"english": "Transfer Learning Capability", "tamil": "பரிமாற்ற கற்றல் திறன்",
     "telugu": "ట్రాన్స్‌ఫర్ లెర్నింగ్ సామర్థ్యం", "kannada": "ವರ್ಗಾವಣೆ ಕಲಿಕೆ ಸಾಮರ್ಥ್ಯ",
     "malayalam": "ട്രാൻസ്ഫർ ലേണിംഗ് ശേഷി", "hindi": "ट्रांसफर लर्निंग क्षमता",
     "bengali": "ট্রান্সফার লার্নিং সক্ষমতা", "marathi": "ट्रान्सफर लर्निंग क्षमता",
     "gujarati": "ટ્રાન્સફર લર્નિંગ ક્ષમતા", "punjabi": "ਟਰਾਂਸਫਰ ਲਰਨਿੰਗ ਸਮਰੱਥਾ", "odia": "ଟ୍ରାନ୍ସଫର ଲର୍ନିଂ କ୍ଷମତା"},
    {"english": "Training Speed", "tamil": "பயிற்சி வேகம்",
     "telugu": "శిక్షణ వేగం", "kannada": "ತರಬೇತಿ ವೇಗ",
     "malayalam": "പരിശീലന വേഗത", "hindi": "प्रशिक्षण गति",
     "bengali": "প্রশিক্ষণ গতি", "marathi": "प्रशिक्षण गती",
     "gujarati": "તાલીમ ઝડપ", "punjabi": "ਸਿਖਲਾਈ ਗਤੀ", "odia": "ତାଲିମ ଗତି"},
    {"english": "Generalization Ability", "tamil": "பொதுமைப்படுத்தல் திறன்",
     "telugu": "సాధారణీకరణ సామర్థ్యం", "kannada": "ಸಾಮಾನ್ಯೀಕರಣ ಸಾಮರ್ಥ್ಯ",
     "malayalam": "സാമാന്യവൽക്കരണ ശേഷി", "hindi": "सामान्यीकरण क्षमता",
     "bengali": "সাধারণীকরণ ক্ষমতা", "marathi": "सामान्यीकरण क्षमता",
     "gujarati": "સામાન્યીકરણ ક્ષમતા", "punjabi": "ਸਧਾਰਨੀਕਰਨ ਸਮਰੱਥਾ", "odia": "ସାଧାରଣୀକରଣ କ୍ଷମତା"},
]

_METRIC_NAMES_RAW = [
    {"english": "Accuracy", "tamil": "துல்லியம்", "telugu": "ఖచ్చితత్వం", "kannada": "ನಿಖರತೆ",
     "malayalam": "കൃത്യത", "hindi": "सटीकता", "bengali": "নির্ভুলতা", "marathi": "अचूकता",
     "gujarati": "ચોકસાઈ", "punjabi": "ਸ਼ੁੱਧਤਾ", "odia": "ସଠିକତା"},
    {"english": "Precision", "tamil": "பிரிசிஷன் (துல்லியத்தன்மை)", "telugu": "ప్రెసిషన్ (నిర్దిష్టత)",
     "kannada": "ಪ್ರಿಸಿಷನ್ (ನಿಷ್ಕೃಷ್ಟತೆ)", "malayalam": "പ്രെസിഷൻ (കൃത്യതാ നിലവാരം)",
     "hindi": "परिशुद्धता (प्रिसिज़न)", "bengali": "প্রিসিশন (যথার্থতা)", "marathi": "प्रिसिजन (यथार्थता)",
     "gujarati": "પ્રિસિઝન (ચોકસાઈ દર)", "punjabi": "ਪ੍ਰੀਸੀਜ਼ਨ", "odia": "ପ୍ରିସିଜନ"},
    {"english": "Recall", "tamil": "ரீகால் (நினைவெடுப்பு விகிதம்)", "telugu": "రీకాల్ (గుర్తింపు రేటు)",
     "kannada": "ರೀಕಾಲ್ (ಮರುಸ್ಮರಣೆ ದರ)", "malayalam": "റീകോൾ (തിരിച്ചറിയൽ നിരക്ക്)",
     "hindi": "रिकॉल (स्मरण दर)", "bengali": "রিকল (স্মরণ হার)", "marathi": "रिकॉल (आठवण दर)",
     "gujarati": "રિકોલ (યાદ દર)", "punjabi": "ਰੀਕਾਲ", "odia": "ରିକଲ"},
    {"english": "F1-Score", "tamil": "F1-மதிப்பெண்", "telugu": "F1-స్కోర్", "kannada": "F1-ಸ್ಕೋರ್",
     "malayalam": "F1-സ്കോർ", "hindi": "F1-स्कोर", "bengali": "F1-স্কোর", "marathi": "F1-गुण",
     "gujarati": "F1-સ્કોર", "punjabi": "F1-ਸਕੋਰ", "odia": "F1-ସ୍କୋର"},
]


def get_capability_dimensions(lang: str) -> list[str]:
    """
    Localized x-axis category labels for the CNN vs ResNet50 vs
    EfficientNetB0 conceptual capability-comparison chart. Order is
    fixed and must match the score lists in
    app.py:generate_model_capability_data (5 dimensions). Local
    dictionary only — no API calls.
    """
    lang = resolve_lang(lang)
    return [_pick(block, lang) for block in _CAPABILITY_DIMENSIONS_RAW]


def get_metric_names(lang: str) -> list[str]:
    """
    Localized display names for the four evaluation metrics
    (Accuracy, Precision, Recall, F1-Score), same order as the stable
    internal keys used in app.py's Research Metrics comparison table.
    Local dictionary only — no API calls.
    """
    lang = resolve_lang(lang)
    return [_pick(block, lang) for block in _METRIC_NAMES_RAW]
# LOCALIZATION_COMPLETION_PATCH

# LOCALIZATION_COMPLETION_PATCH
# All normal application prose below is local/static. Gemini is not involved.
_FULL_LANGS = ("english", "tamil", "telugu", "kannada", "malayalam", "hindi", "bengali", "marathi", "gujarati", "punjabi", "odia")

_DYNAMIC = {
    "confidence": {
        "english": ("Very high confidence — the model found strong visual evidence.", "High confidence — clear disease-consistent patterns were detected.", "Moderate confidence — some disease-consistent features are present, but signs are less distinct.", "Low confidence — visual evidence is weak or ambiguous; manual verification is recommended."),
        "tamil": ("மிக உயர்ந்த நம்பிக்கை — மாதிரி வலுவான காட்சி ஆதாரங்களை கண்டறிந்தது.", "உயர் நம்பிக்கை — நோயுடன் பொருந்தும் தெளிவான வடிவங்கள் கண்டறியப்பட்டன.", "மிதமான நம்பிக்கை — நோயுடன் பொருந்தும் சில அம்சங்கள் உள்ளன, ஆனால் அறிகுறிகள் தெளிவாக இல்லை.", "குறைந்த நம்பிக்கை — காட்சி ஆதாரம் பலவீனமாக அல்லது தெளிவற்றதாக உள்ளது; நேரடி பரிசோதனை பரிந்துரைக்கப்படுகிறது."),
        "telugu": ("చాలా అధిక నమ్మకం — మోడల్ బలమైన దృశ్య ఆధారాలను గుర్తించింది.", "అధిక నమ్మకం — వ్యాధికి సరిపోయే స్పష్టమైన నమూనాలు గుర్తించబడ్డాయి.", "మధ్యస్థ నమ్మకం — వ్యాధికి సరిపోయే కొన్ని లక్షణాలు ఉన్నాయి, కానీ సంకేతాలు స్పష్టంగా లేవు.", "తక్కువ నమ్మకం — దృశ్య ఆధారాలు బలహీనంగా లేదా స్పష్టత లేకుండా ఉన్నాయి; ప్రత్యక్ష పరిశీలన అవసరం."),
        "kannada": ("ಅತ್ಯಂತ ಹೆಚ್ಚಿನ ವಿಶ್ವಾಸ — ಮಾದರಿಯು ಬಲವಾದ ದೃಶ್ಯ ಸಾಕ್ಷ್ಯವನ್ನು ಕಂಡುಹಿಡಿದಿದೆ.", "ಹೆಚ್ಚಿನ ವಿಶ್ವಾಸ — ರೋಗಕ್ಕೆ ಹೊಂದುವ ಸ್ಪಷ್ಟ ಮಾದರಿಗಳು ಕಂಡುಬಂದಿವೆ.", "ಮಧ್ಯಮ ವಿಶ್ವಾಸ — ಕೆಲವು ಹೊಂದುವ ಲಕ್ಷಣಗಳಿವೆ, ಆದರೆ ಸೂಚನೆಗಳು ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ.", "ಕಡಿಮೆ ವಿಶ್ವಾಸ — ದೃಶ್ಯ ಸಾಕ್ಷ್ಯ ದುರ್ಬಲ ಅಥವಾ ಅಸ್ಪಷ್ಟವಾಗಿದೆ; ನೇರ ಪರಿಶೀಲನೆ ಅಗತ್ಯ."),
        "malayalam": ("വളരെ ഉയർന്ന വിശ്വാസ്യത — മോഡൽ ശക്തമായ ദൃശ്യ തെളിവുകൾ കണ്ടെത്തി.", "ഉയർന്ന വിശ്വാസ്യത — രോഗവുമായി പൊരുത്തപ്പെടുന്ന വ്യക്തമായ മാതൃകകൾ കണ്ടെത്തി.", "മിതമായ വിശ്വാസ്യത — ചില പൊരുത്തമുള്ള സവിശേഷതകൾ ഉണ്ട്, പക്ഷേ അടയാളങ്ങൾ വ്യക്തമായിട്ടില്ല.", "കുറഞ്ഞ വിശ്വാസ്യത — ദൃശ്യ തെളിവുകൾ ദുർബലമോ അവ്യക്തമോ ആണ്; നേരിട്ട് പരിശോധിക്കുക."),
        "hindi": ("बहुत अधिक विश्वसनीयता — मॉडल ने मजबूत दृश्य प्रमाण पाए।", "उच्च विश्वसनीयता — रोग से मेल खाते स्पष्ट पैटर्न मिले।", "मध्यम विश्वसनीयता — रोग से मेल खाते कुछ लक्षण हैं, लेकिन संकेत कम स्पष्ट हैं।", "कम विश्वसनीयता — दृश्य प्रमाण कमजोर या अस्पष्ट हैं; खेत में प्रत्यक्ष जांच की सलाह है।"),
        "bengali": ("অত্যন্ত উচ্চ নির্ভরযোগ্যতা — মডেল শক্তিশালী দৃশ্যমান প্রমাণ পেয়েছে।", "উচ্চ নির্ভরযোগ্যতা — রোগের সঙ্গে মিলে যায় এমন স্পষ্ট ধরন পাওয়া গেছে।", "মাঝারি নির্ভরযোগ্যতা — কিছু মিল থাকা লক্ষণ আছে, তবে সংকেত কম স্পষ্ট।", "কম নির্ভরযোগ্যতা — দৃশ্যমান প্রমাণ দুর্বল বা অস্পষ্ট; সরাসরি পরীক্ষা করুন।"),
        "marathi": ("अत्यंत उच्च विश्वासार्हता — मॉडेलला ठोस दृश्य पुरावे मिळाले.", "उच्च विश्वासार्हता — रोगाशी जुळणारे स्पष्ट नमुने आढळले.", "मध्यम विश्वासार्हता — काही जुळणारी लक्षणे आहेत, पण संकेत कमी स्पष्ट आहेत.", "कमी विश्वासार्हता — दृश्य पुरावे कमकुवत किंवा अस्पष्ट आहेत; प्रत्यक्ष तपासणी करा."),
        "gujarati": ("ખૂબ ઊંચો વિશ્વાસ — મોડેલને મજબૂત દૃશ્ય પુરાવા મળ્યા.", "ઊંચો વિશ્વાસ — રોગ સાથે મેળ ખાતી સ્પષ્ટ રચનાઓ મળી.", "મધ્યમ વિશ્વાસ — કેટલાક મેળ ખાતા લક્ષણો છે, પરંતુ સંકેતો ઓછા સ્પષ્ટ છે.", "ઓછો વિશ્વાસ — દૃશ્ય પુરાવા નબળા અથવા અસ્પષ્ટ છે; ખેતરમાં તપાસ કરો."),
        "punjabi": ("ਬਹੁਤ ਉੱਚਾ ਭਰੋਸਾ — ਮਾਡਲ ਨੂੰ ਮਜ਼ਬੂਤ ਦ੍ਰਿਸ਼ਟੀਗਤ ਸਬੂਤ ਮਿਲੇ।", "ਉੱਚਾ ਭਰੋਸਾ — ਬਿਮਾਰੀ ਨਾਲ ਮਿਲਦੇ ਸਪਸ਼ਟ ਨਮੂਨੇ ਮਿਲੇ।", "ਦਰਮਿਆਨਾ ਭਰੋਸਾ — ਕੁਝ ਮਿਲਦੇ ਲੱਛਣ ਹਨ, ਪਰ ਸੰਕੇਤ ਘੱਟ ਸਪਸ਼ਟ ਹਨ।", "ਘੱਟ ਭਰੋਸਾ — ਦ੍ਰਿਸ਼ਟੀਗਤ ਸਬੂਤ ਕਮਜ਼ੋਰ ਜਾਂ ਅਸਪਸ਼ਟ ਹਨ; ਖੇਤ ਵਿੱਚ ਜਾਂਚ ਕਰੋ।"),
        "odia": ("ଅତ୍ୟଧିକ ବିଶ୍ୱସନୀୟତା — ମଡେଲ ଶକ୍ତିଶାଳୀ ଦୃଶ୍ୟ ପ୍ରମାଣ ପାଇଛି।", "ଉଚ୍ଚ ବିଶ୍ୱସନୀୟତା — ରୋଗ ସହିତ ମେଳ ଖାଉଥିବା ସ୍ପଷ୍ଟ ଢାଞ୍ଚା ମିଳିଛି।", "ମଧ୍ୟମ ବିଶ୍ୱସନୀୟତା — କିଛି ମେଳ ଖାଉଥିବା ଲକ୍ଷଣ ଅଛି, କିନ୍ତୁ ସଙ୍କେତ ସ୍ପଷ୍ଟ ନୁହେଁ।", "କମ ବିଶ୍ୱସନୀୟତା — ଦୃଶ୍ୟ ପ୍ରମାଣ ଦୁର୍ବଳ କିମ୍ବା ଅସ୍ପଷ୍ଟ; କ୍ଷେତ୍ରରେ ଯାଞ୍ଚ କରନ୍ତୁ।"),
    },
    "why": {
        "english": "The model focused mainly on {location}, showing a {focus} activation pattern and {coverage}. This visual pattern is consistent with {disease}.",
        "tamil": "மாதிரி முக்கியமாக {location} பகுதியில் கவனம் செலுத்தியது; {focus} செயல்பாட்டு வடிவமும் {coverage} காணப்பட்டது. இந்த காட்சி வடிவம் {disease} உடன் பொருந்துகிறது.",
        "telugu": "మోడల్ ప్రధానంగా {location} పై దృష్టి పెట్టింది; {focus} క్రియాశీల నమూనా మరియు {coverage} కనిపించాయి. ఈ దృశ్య నమూనా {disease}తో సరిపోతుంది.",
        "kannada": "ಮಾದರಿಯು ಮುಖ್ಯವಾಗಿ {location} ಮೇಲೆ ಗಮನ ಕೇಂದ್ರೀಕರಿಸಿದೆ; {focus} ಸಕ್ರಿಯತಾ ಮಾದರಿ ಮತ್ತು {coverage} ಕಂಡುಬಂದಿದೆ. ಈ ದೃಶ್ಯ ಮಾದರಿ {disease}ಗೆ ಹೊಂದಿಕೆಯಾಗುತ್ತದೆ.",
        "malayalam": "മോഡൽ പ്രധാനമായും {location}-ൽ ശ്രദ്ധ കേന്ദ്രീകരിച്ചു; {focus} ആക്റ്റിവേഷൻ മാതൃകയും {coverage}-യും കണ്ടു. ഈ ദൃശ്യ മാതൃക {disease}-നോട് പൊരുത്തപ്പെടുന്നു.",
        "hindi": "मॉडल ने मुख्य रूप से {location} पर ध्यान केंद्रित किया; {focus} सक्रियता पैटर्न और {coverage} देखा गया। यह दृश्य पैटर्न {disease} से मेल खाता है।",
        "bengali": "মডেল প্রধানত {location}-এ মনোযোগ দিয়েছে; {focus} সক্রিয়তার ধরন এবং {coverage} দেখা গেছে। এই দৃশ্যমান ধরন {disease}-এর সঙ্গে মেলে।",
        "marathi": "मॉडेलने मुख्यतः {location} वर लक्ष केंद्रित केले; {focus} सक्रियता नमुना आणि {coverage} दिसले. हा दृश्य नमुना {disease} शी जुळतो.",
        "gujarati": "મોડેલે મુખ્યત્વે {location} પર ધ્યાન કેન્દ્રિત કર્યું; {focus} સક્રિયતા પેટર્ન અને {coverage} જોવા મળ્યું. આ દૃશ્ય પેટર્ન {disease} સાથે મેળ ખાય છે.",
        "punjabi": "ਮਾਡਲ ਨੇ ਮੁੱਖ ਤੌਰ ਤੇ {location} ਉੱਤੇ ਧਿਆਨ ਦਿੱਤਾ; {focus} ਸਰਗਰਮੀ ਪੈਟਰਨ ਅਤੇ {coverage} ਦਿਖਾਈ ਦਿੱਤਾ। ਇਹ ਦ੍ਰਿਸ਼ਟੀਗਤ ਪੈਟਰਨ {disease} ਨਾਲ ਮਿਲਦਾ ਹੈ।",
        "odia": "ମଡେଲ ମୁଖ୍ୟତଃ {location} ଉପରେ ଧ୍ୟାନ ଦେଇଛି; {focus} ସକ୍ରିୟତା ଢାଞ୍ଚା ଏବଂ {coverage} ଦେଖାଗଲା। ଏହି ଦୃଶ୍ୟ ଢାଞ୍ଚା {disease} ସହିତ ମେଳ ଖାଏ।",
    },
    "summary": {
        "english": "The AI estimated {disease_pct}% of visible tissue as affected and {healthy_pct}% as healthy, with attention around {location}. Coverage is {coverage}. {conf}",
        "tamil": "AI காட்சியளிக்கும் திசுவில் {disease_pct}% பாதிக்கப்பட்டதாகவும் {healthy_pct}% ஆரோக்கியமாகவும் மதிப்பிட்டது; கவனம் {location} சுற்றி இருந்தது. பாதிப்பு {coverage}. {conf}",
        "telugu": "AI దృశ్య కణజాలంలో {disease_pct}% ప్రభావితమైందని, {healthy_pct}% ఆరోగ్యంగా ఉందని అంచనా వేసింది; దృష్టి {location} చుట్టూ ఉంది. వ్యాప్తి {coverage}. {conf}",
        "kannada": "AI ದೃಶ್ಯಮಾನ ಅಂಗಾಂಶದ {disease_pct}% ಹಾನಿಗೊಳಗಾಗಿದೆ ಮತ್ತು {healthy_pct}% ಆರೋಗ್ಯಕರವಾಗಿದೆ ಎಂದು ಅಂದಾಜಿಸಿದೆ; ಗಮನ {location} ಸುತ್ತ ಇತ್ತು. ವ್ಯಾಪ್ತಿ {coverage}. {conf}",
        "malayalam": "AI ദൃശ്യമായ ടിഷ്യുവിന്റെ {disease_pct}% ബാധിച്ചതും {healthy_pct}% ആരോഗ്യകരവുമാണെന്ന് കണക്കാക്കി; ശ്രദ്ധ {location}-ന് ചുറ്റുമായിരുന്നു. വ്യാപ്തി {coverage}. {conf}",
        "hindi": "AI ने दिखाई देने वाले ऊतक के {disease_pct}% को प्रभावित और {healthy_pct}% को स्वस्थ आंका; ध्यान {location} के आसपास था। फैलाव {coverage} है। {conf}",
        "bengali": "AI দৃশ্যমান টিস্যুর {disease_pct}% আক্রান্ত এবং {healthy_pct}% সুস্থ বলে অনুমান করেছে; মনোযোগ {location}-এর চারপাশে ছিল। বিস্তার {coverage}। {conf}",
        "marathi": "AI ने दृश्यमान ऊतींपैकी {disease_pct}% बाधित आणि {healthy_pct}% निरोगी असल्याचा अंदाज घेतला; लक्ष {location} भोवती होते. व्याप्ती {coverage}. {conf}",
        "gujarati": "AI એ દેખાતા પેશીના {disease_pct}% ને અસરગ્રસ્ત અને {healthy_pct}% ને તંદુરસ્ત ગણાવ્યા; ધ્યાન {location} આસપાસ હતું. ફેલાવો {coverage} છે. {conf}",
        "punjabi": "AI ਨੇ ਦਿਖਾਈ ਦੇ ਰਹੇ ਤੰਤੂ ਦਾ {disease_pct}% ਪ੍ਰਭਾਵਿਤ ਅਤੇ {healthy_pct}% ਸਿਹਤਮੰਦ ਅੰਕਿਆ; ਧਿਆਨ {location} ਦੇ ਆਲੇ-ਦੁਆਲੇ ਸੀ। ਫੈਲਾਅ {coverage} ਹੈ। {conf}",
        "odia": "AI ଦୃଶ୍ୟମାନ ତନ୍ତୁର {disease_pct}% ପ୍ରଭାବିତ ଏବଂ {healthy_pct}% ସୁସ୍ଥ ବୋଲି ଆକଳନ କରିଛି; ଧ୍ୟାନ {location} ଚାରିପାଖରେ ଥିଲା। ବିସ୍ତାର {coverage}। {conf}",
    },
}

def _lang_text(block, lang, default=''):
    return block.get(resolve_lang(lang), default)

def confidence_interpretation_text(confidence, focus_label, lang):
    lang = resolve_lang(lang); p = confidence * 100
    i = 0 if p >= 85 else 1 if p >= 65 else 2 if p >= 45 else 3
    text = _DYNAMIC['confidence'][lang][i]
    if focus_label == 'Focused':
        text += {'english':' The attention map is concentrated on specific lesions.', 'hindi':' ध्यान मानचित्र विशिष्ट घावों पर केंद्रित है।', 'tamil':' கவனம் குறிப்பிட்ட காயங்களில் குவிந்துள்ளது.', 'telugu':' దృష్టి నిర్దిష్ట గాయాలపై కేంద్రీకృతమైంది.', 'kannada':' ಗಮನವು ನಿರ್ದಿಷ್ಟ ಗಾಯಗಳ ಮೇಲೆ ಕೇಂದ್ರೀಕೃತವಾಗಿದೆ.', 'malayalam':' ശ്രദ്ധ പ്രത്യേക മുറിവുകളിൽ കേന്ദ്രീകരിച്ചിരിക്കുന്നു.', 'bengali':' মনোযোগ নির্দিষ্ট ক্ষতের উপর কেন্দ্রীভূত।', 'marathi':' लक्ष विशिष्ट जखमांवर केंद्रित आहे.', 'gujarati':' ધ્યાન ચોક્કસ ઘા પર કેન્દ્રિત છે.', 'punjabi':' ਧਿਆਨ ਖਾਸ ਘਾਵਾਂ ਉੱਤੇ ਕੇਂਦਰਿਤ ਹੈ।', 'odia':' ଧ୍ୟାନ ନିର୍ଦ୍ଦିଷ୍ଟ କ୍ଷତ ଉପରେ କେନ୍ଦ୍ରିତ ଅଛି।'}[lang]
    elif focus_label == 'Diffuse':
        text += {'english':' The attention map is spread across the leaf.', 'hindi':' ध्यान मानचित्र पूरी पत्ती पर फैला हुआ है।', 'tamil':' கவனம் இலை முழுவதும் பரவியுள்ளது.', 'telugu':' దృష్టి ఆకు అంతటా వ్యాపించింది.', 'kannada':' ಗಮನವು ಎಲೆಯಾದ್ಯಂತ ಹರಡಿದೆ.', 'malayalam':' ശ്രദ്ധ ഇലയിലുടനീളം വ്യാപിച്ചിരിക്കുന്നു.', 'bengali':' মনোযোগ পুরো পাতায় ছড়িয়ে আছে।', 'marathi':' लक्ष संपूर्ण पानावर पसरले आहे.', 'gujarati':' ધ્યાન સમગ્ર પાન પર ફેલાયેલું છે.', 'punjabi':' ਧਿਆਨ ਪੱਤੇ ਭਰ ਫੈਲਿਆ ਹੋਇਆ ਹੈ।', 'odia':' ଧ୍ୟାନ ସମଗ୍ର ପତ୍ରରେ ବିସ୍ତାରିତ ଅଛି।'}[lang]
    return text

def why_predicted_text(disease, location, coverage_label, focus_label, lang):
    lang = resolve_lang(lang); d = disease_display_name(disease, lang); loc = translate_enum(location, lang); cov = translate_enum(coverage_label, lang); foc = translate_enum(focus_label, lang)
    return _DYNAMIC['why'][lang].format(disease=d, location=loc, coverage=cov, focus=foc)

def explainability_summary_text(disease, disease_pct, healthy_pct, location, coverage_label, confidence_interp, lang):
    lang = resolve_lang(lang); return _DYNAMIC['summary'][lang].format(disease_pct=disease_pct, healthy_pct=healthy_pct, location=translate_enum(location, lang), coverage=translate_enum(coverage_label, lang), conf=confidence_interp)

def agricultural_interpretation_text(disease, location, disease_pct, lang):
    lang = resolve_lang(lang); loc = translate_enum(location, lang); d = disease_display_name(disease, lang)
    text = {
      'english':'Inspect {loc} of affected plants for symptoms typical of {d}. Early intervention can prevent further spread.', 'tamil':'பாதிக்கப்பட்ட செடிகளின் {loc} பகுதியில் {d} நோயின் அறிகுறிகளை பரிசோதிக்கவும். ஆரம்ப நடவடிக்கை பரவலைத் தடுக்க உதவும்.', 'telugu':'ప్రభావిత మొక్కల {loc} వద్ద {d} లక్షణాలను పరిశీలించండి. ముందస్తు చర్య వ్యాప్తిని అరికడుతుంది.', 'kannada':'ಬಾಧಿತ ಸಸ್ಯಗಳ {loc} ಭಾಗದಲ್ಲಿ {d} ಲಕ್ಷಣಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. ಆರಂಭಿಕ ಕ್ರಮವು ಹರಡುವಿಕೆಯನ್ನು ತಡೆಯುತ್ತದೆ.', 'malayalam':'ബാധിച്ച ചെടികളുടെ {loc} ഭാഗത്ത് {d}-ന്റെ ലക്ഷണങ്ങൾ പരിശോധിക്കുക. നേരത്തെയുള്ള നടപടി വ്യാപനം തടയും.', 'hindi':'प्रभावित पौधों के {loc} पर {d} के लक्षणों की जांच करें। शुरुआती कार्रवाई फैलाव रोक सकती है।', 'bengali':'আক্রান্ত গাছের {loc}-এ {d}-এর লক্ষণ পরীক্ষা করুন। দ্রুত ব্যবস্থা ছড়িয়ে পড়া রোধ করতে পারে।', 'marathi':'बाधित झाडांच्या {loc} भागावर {d} ची लक्षणे तपासा. लवकर उपाययोजना प्रसार रोखू शकते.', 'gujarati':'અસરગ્રસ્ત છોડના {loc} પર {d} ના લક્ષણો તપાસો. વહેલી કાર્યવાહી ફેલાવો રોકી શકે છે.', 'punjabi':'ਪ੍ਰਭਾਵਿਤ ਪੌਦਿਆਂ ਦੇ {loc} ਉੱਤੇ {d} ਦੇ ਲੱਛਣ ਜਾਂਚੋ। ਸਮੇਂ ਸਿਰ ਕਾਰਵਾਈ ਫੈਲਾਅ ਰੋਕ ਸਕਦੀ ਹੈ।', 'odia':'ପ୍ରଭାବିତ ଗଛର {loc} ଠାରେ {d} ର ଲକ୍ଷଣ ଯାଞ୍ଚ କରନ୍ତୁ। ଶୀଘ୍ର ପଦକ୍ଷେପ ବିସ୍ତାର ରୋକିପାରେ।'}[lang]
    return text.format(loc=loc, d=d)

def health_ai_summary_text(is_healthy, confidence_meter, disease, severity_label, severity_pct, health_score, health_category, recovery_label, lang):
    lang = resolve_lang(lang)
    if is_healthy:
        return {'english':'This plant shows no disease indicators. Confidence is {p}%. Continue routine monitoring.', 'tamil':'இந்த செடியில் நோய் அறிகுறிகள் இல்லை. நம்பிக்கை {p}%. வழக்கமான கண்காணிப்பை தொடரவும்.', 'telugu':'ఈ మొక్కలో వ్యాధి సూచనలు లేవు. నమ్మకం {p}%. సాధారణ పర్యవేక్షణ కొనసాగించండి.', 'kannada':'ಈ ಸಸ್ಯದಲ್ಲಿ ರೋಗದ ಸೂಚನೆಗಳಿಲ್ಲ. ವಿಶ್ವಾಸ {p}%. ನಿಯಮಿತ ಮೇಲ್ವಿಚಾರಣೆ ಮುಂದುವರಿಸಿ.', 'malayalam':'ഈ ചെടിയിൽ രോഗലക്ഷണങ്ങളില്ല. വിശ്വാസ്യത {p}%. പതിവ് നിരീക്ഷണം തുടരുക.', 'hindi':'इस पौधे में रोग के संकेत नहीं हैं। विश्वसनीयता {p}% है। नियमित निगरानी जारी रखें।', 'bengali':'এই গাছে রোগের লক্ষণ নেই। নির্ভরযোগ্যতা {p}%। নিয়মিত পর্যবেক্ষণ চালিয়ে যান।', 'marathi':'या रोपामध्ये रोगाची लक्षणे नाहीत. विश्वासार्हता {p}% आहे. नियमित निरीक्षण सुरू ठेवा.', 'gujarati':'આ છોડમાં રોગના સંકેતો નથી. વિશ્વાસ {p}% છે. નિયમિત દેખરેખ ચાલુ રાખો.', 'punjabi':'ਇਸ ਪੌਦੇ ਵਿੱਚ ਬਿਮਾਰੀ ਦੇ ਸੰਕੇਤ ਨਹੀਂ ਹਨ। ਭਰੋਸਾ {p}% ਹੈ। ਨਿਯਮਤ ਨਿਗਰਾਨੀ ਜਾਰੀ ਰੱਖੋ।', 'odia':'ଏହି ଗଛରେ ରୋଗର ଲକ୍ଷଣ ନାହିଁ। ବିଶ୍ୱାସ {p}%। ନିୟମିତ ନିରୀକ୍ଷଣ ଜାରି ରଖନ୍ତୁ।'}[lang].format(p=confidence_meter)
    labels = {'english':'{d} detected with {p}% confidence. Severity is {s} ({sp}%), crop health is {h}/100 ({c}), and recovery potential is {r}.', 'tamil':'{d} கண்டறியப்பட்டது; நம்பிக்கை {p}%. தீவிரம் {s} ({sp}%), பயிர் ஆரோக்கியம் {h}/100 ({c}), மீட்பு வாய்ப்பு {r}.', 'telugu':'{d} గుర్తించబడింది; నమ్మకం {p}%. తీవ్రత {s} ({sp}%), పంట ఆరోగ్యం {h}/100 ({c}), కోలుకునే అవకాశం {r}.', 'kannada':'{d} ಪತ್ತೆಯಾಗಿದೆ; ವಿಶ್ವಾಸ {p}%. ತೀವ್ರತೆ {s} ({sp}%), ಬೆಳೆ ಆರೋಗ್ಯ {h}/100 ({c}), ಚೇತರಿಕೆ ಸಾಧ್ಯತೆ {r}.', 'malayalam':'{d} കണ്ടെത്തി; വിശ്വാസ്യത {p}%. തീവ്രത {s} ({sp}%), വിള ആരോഗ്യം {h}/100 ({c}), വീണ്ടെടുക്കൽ സാധ്യത {r}.', 'hindi':'{d} का पता चला; विश्वसनीयता {p}%। गंभीरता {s} ({sp}%), फसल स्वास्थ्य {h}/100 ({c}), सुधार की संभावना {r} है।', 'bengali':'{d} শনাক্ত হয়েছে; নির্ভরযোগ্যতা {p}%। তীব্রতা {s} ({sp}%), ফসলের স্বাস্থ্য {h}/100 ({c}), সুস্থতার সম্ভাবনা {r}।', 'marathi':'{d} आढळले; विश्वासार्हता {p}%. तीव्रता {s} ({sp}%), पिकाचे आरोग्य {h}/100 ({c}), सुधारण्याची शक्यता {r}.', 'gujarati':'{d} મળ્યું; વિશ્વાસ {p}%. ગંભીરતા {s} ({sp}%), પાકનું આરોગ્ય {h}/100 ({c}), સુધારાની સંભાવના {r}.', 'punjabi':'{d} ਮਿਲੀ; ਭਰੋਸਾ {p}%। ਗੰਭੀਰਤਾ {s} ({sp}%), ਫਸਲ ਦੀ ਸਿਹਤ {h}/100 ({c}), ਸੁਧਾਰ ਦੀ ਸੰਭਾਵਨਾ {r} ਹੈ।', 'odia':'{d} ଚିହ୍ନଟ ହୋଇଛି; ବିଶ୍ୱାସ {p}%। ଗମ୍ଭୀରତା {s} ({sp}%), ଫସଲ ସ୍ୱାସ୍ଥ୍ୟ {h}/100 ({c}), ସୁସ୍ଥ ହେବାର ସମ୍ଭାବନା {r}।'}[lang]
    return labels.format(d=disease_display_name(disease, lang), p=confidence_meter, s=translate_enum(severity_label, lang), sp=severity_pct, h=health_score, c=translate_enum(health_category, lang), r=translate_enum(recovery_label, lang))

# Complete local coverage for every dictionary block. Missing entries become a
# visible development marker rather than silently showing English.
def _pick(block, lang):
    lang = resolve_lang(lang)
    if lang in block:
        return block[lang]
    if lang != 'english':
        return f"[{native_name(lang)} translation missing]"
    return block.get('english', '')

_UI_RAW.update({
    "voice_no_text": {"english": "No text is available for voice playback.", "tamil": "குரல் இயக்கத்திற்கு உரை இல்லை.", "telugu": "వాయిస్ ప్లేబ్యాక్‌కు వచనం లేదు.", "kannada": "ಧ್ವನಿ ಪ್ಲೇಬ್ಯಾಕ್‌ಗೆ ಪಠ್ಯವಿಲ್ಲ.", "malayalam": "ശബ്ദ പ്ലേബാക്കിന് വാചകം ലഭ്യമല്ല.", "hindi": "वॉइस चलाने के लिए कोई पाठ उपलब्ध नहीं है।", "bengali": "ভয়েস চালানোর জন্য কোনো লেখা নেই।", "marathi": "आवाज प्लेबॅकसाठी मजकूर उपलब्ध नाही.", "gujarati": "વૉઇસ ચલાવવા માટે કોઈ લખાણ ઉપલબ્ધ નથી.", "punjabi": "ਆਵਾਜ਼ ਚਲਾਉਣ ਲਈ ਕੋਈ ਲਿਖਤ ਉਪਲਬਧ ਨਹੀਂ ਹੈ।", "odia": "ଭଏସ ଚଲାଇବା ପାଇଁ କୌଣସି ପାଠ୍ୟ ନାହିଁ।"},
    "voice_unsupported_lang": {"english": "Voice playback is unavailable for code {code}; the localized text is retained.", "tamil": "{code} குறியீட்டிற்கு குரல் இயக்கம் கிடைக்கவில்லை; உள்ளூர் மொழி உரை பாதுகாக்கப்பட்டுள்ளது.", "telugu": "{code} కోడ్‌కు వాయిస్ అందుబాటులో లేదు; స్థానికీకరించిన వచనం అలాగే ఉంది.", "kannada": "{code} ಕೋಡ್‌ಗೆ ಧ್ವನಿ ಲಭ್ಯವಿಲ್ಲ; ಸ್ಥಳೀಯ ಪಠ್ಯವನ್ನು ಉಳಿಸಲಾಗಿದೆ.", "malayalam": "{code} കോഡിന് ശബ്ദ പ്ലേബാക്ക് ലഭ്യമല്ല; പ്രാദേശിക വാചകം നിലനിർത്തി.", "hindi": "{code} कोड के लिए वॉइस उपलब्ध नहीं है; स्थानीय पाठ सुरक्षित रखा गया है।", "bengali": "{code} কোডের জন্য ভয়েস চালানো যায় না; স্থানীয় লেখা রাখা হয়েছে।", "marathi": "{code} कोडसाठी आवाज उपलब्ध नाही; स्थानिक मजकूर कायम ठेवला आहे.", "gujarati": "{code} કોડ માટે વૉઇસ ઉપલબ્ધ નથી; સ્થાનિક લખાણ જાળવવામાં આવ્યું છે.", "punjabi": "{code} ਕੋਡ ਲਈ ਆਵਾਜ਼ ਉਪਲਬਧ ਨਹੀਂ; ਸਥਾਨਕ ਲਿਖਤ ਜਿਉਂ ਦੀ ਤਿਉਂ ਰੱਖੀ ਹੈ।", "odia": "{code} କୋଡ ପାଇଁ ଭଏସ ଉପଲବ୍ଧ ନାହିଁ; ସ୍ଥାନୀୟ ପାଠ୍ୟ ରଖାଯାଇଛି।"},
    "voice_audio_error": {"english": "Could not generate audio for {lang_name}.", "tamil": "{lang_name} மொழிக்கான ஒலியை உருவாக்க முடியவில்லை.", "telugu": "{lang_name} కోసం ఆడియోను రూపొందించలేకపోయాం.", "kannada": "{lang_name} ಗಾಗಿ ಧ್ವನಿಯನ್ನು ರಚಿಸಲಾಗಲಿಲ್ಲ.", "malayalam": "{lang_name} ഭാഷയ്ക്കായി ഓഡിയോ സൃഷ്ടിക്കാനായില്ല.", "hindi": "{lang_name} के लिए ऑडियो तैयार नहीं हो सका।", "bengali": "{lang_name}-এর জন্য অডিও তৈরি করা যায়নি।", "marathi": "{lang_name} साठी ऑडिओ तयार करता आले नाही.", "gujarati": "{lang_name} માટે ઑડિયો બનાવી શકાયો નથી.", "punjabi": "{lang_name} ਲਈ ਆਡੀਓ ਨਹੀਂ ਬਣ ਸਕੀ।", "odia": "{lang_name} ପାଇଁ ଅଡିଓ ତିଆରି ହୋଇପାରିଲା ନାହିଁ।"},
})

_UI_RAW.update({
    "language_selector": {"english": "Language", "tamil": "மொழி", "telugu": "భాష", "kannada": "ಭಾಷೆ", "malayalam": "ഭാഷ", "hindi": "भाषा", "bengali": "ভাষা", "marathi": "भाषा", "gujarati": "ભાષા", "punjabi": "ਭਾਸ਼ਾ", "odia": "ଭାଷା"},
    "admin_role": {"english": "Admin", "tamil": "நிர்வாகி", "telugu": "నిర్వాహకుడు", "kannada": "ನಿರ್ವಾಹಕ", "malayalam": "അഡ്മിൻ", "hindi": "व्यवस्थापक", "bengali": "অ্যাডমিন", "marathi": "प्रशासक", "gujarati": "વ્યવસ્થાપક", "punjabi": "ਪ੍ਰਬੰਧਕ", "odia": "ପ୍ରଶାସକ"},
    "guest_role": {"english": "Guest", "tamil": "விருந்தினர்", "telugu": "అతిథి", "kannada": "ಅತಿಥಿ", "malayalam": "അതിഥി", "hindi": "अतिथि", "bengali": "অতিথি", "marathi": "अतिथी", "gujarati": "મહેમાન", "punjabi": "ਮਹਿਮਾਨ", "odia": "ଅତିଥି"},
})

# Complete any legacy UI blocks that predate the 11-language expansion. This
# is intentionally local and deterministic: no translation service is called.
_UI_GENERIC_COPY = {
    "english": "Details are shown below.",
    "tamil": "விவரங்கள் கீழே காட்டப்பட்டுள்ளன.",
    "telugu": "వివరాలు క్రింద చూపబడ్డాయి.",
    "kannada": "ವಿವರಗಳನ್ನು ಕೆಳಗೆ ತೋರಿಸಲಾಗಿದೆ.",
    "malayalam": "വിശദാംശങ്ങൾ താഴെ കാണിച്ചിരിക്കുന്നു.",
    "hindi": "विवरण नीचे दिया गया है।",
    "bengali": "বিস্তারিত নিচে দেওয়া হয়েছে।",
    "marathi": "तपशील खाली दिला आहे.",
    "gujarati": "વિગતો નીચે આપવામાં આવી છે.",
    "punjabi": "ਵੇਰਵੇ ਹੇਠਾਂ ਦਿੱਤੇ ਗਏ ਹਨ।",
    "odia": "ବିବରଣୀ ତଳେ ଦିଆଯାଇଛି।",
}
_UI_WORD_COPY = {
    "english": {"title":"Title", "header":"Section", "label":"Label", "caption":"Information", "button":"Continue", "error":"An error occurred.", "option":"Option", "column":"Column", "score":"Score", "model":"Model", "data":"Data"},
    "tamil": {"title":"தலைப்பு", "header":"பிரிவு", "label":"லேபிள்", "caption":"தகவல்", "button":"தொடரவும்", "error":"பிழை ஏற்பட்டது.", "option":"விருப்பம்", "column":"நெடுவரிசை", "score":"மதிப்பெண்", "model":"மாதிரி", "data":"தரவு"},
    "telugu": {"title":"శీర్షిక", "header":"విభాగం", "label":"లేబుల్", "caption":"సమాచారం", "button":"కొనసాగించండి", "error":"లోపం జరిగింది.", "option":"ఎంపిక", "column":"కాలమ్", "score":"స్కోర్", "model":"మోడల్", "data":"డేటా"},
    "kannada": {"title":"ಶೀರ್ಷಿಕೆ", "header":"ವಿಭಾಗ", "label":"ಲೇಬಲ್", "caption":"ಮಾಹಿತಿ", "button":"ಮುಂದುವರಿಸಿ", "error":"ದೋಷ ಸಂಭವಿಸಿದೆ.", "option":"ಆಯ್ಕೆ", "column":"ಕಾಲಮ್", "score":"ಅಂಕ", "model":"ಮಾದರಿ", "data":"ದತ್ತಾಂಶ"},
    "malayalam": {"title":"ശീർഷകം", "header":"വിഭാഗം", "label":"ലേബൽ", "caption":"വിവരം", "button":"തുടരുക", "error":"ഒരു പിശക് സംഭവിച്ചു.", "option":"ഓപ്ഷൻ", "column":"നിര", "score":"സ്കോർ", "model":"മോഡൽ", "data":"ഡാറ്റ"},
    "hindi": {"title":"शीर्षक", "header":"अनुभाग", "label":"लेबल", "caption":"जानकारी", "button":"जारी रखें", "error":"त्रुटि हुई।", "option":"विकल्प", "column":"स्तंभ", "score":"स्कोर", "model":"मॉडल", "data":"डेटा"},
    "bengali": {"title":"শিরোনাম", "header":"বিভাগ", "label":"লেবেল", "caption":"তথ্য", "button":"চালিয়ে যান", "error":"একটি ত্রুটি হয়েছে।", "option":"বিকল্প", "column":"কলাম", "score":"স্কোর", "model":"মডেল", "data":"ডেটা"},
    "marathi": {"title":"शीर्षक", "header":"विभाग", "label":"लेबल", "caption":"माहिती", "button":"पुढे जा", "error":"त्रुटी झाली.", "option":"पर्याय", "column":"स्तंभ", "score":"गुण", "model":"मॉडेल", "data":"डेटा"},
    "gujarati": {"title":"શીર્ષક", "header":"વિભાગ", "label":"લેબલ", "caption":"માહિતી", "button":"ચાલુ રાખો", "error":"ભૂલ થઈ.", "option":"વિકલ્પ", "column":"કૉલમ", "score":"સ્કોર", "model":"મોડેલ", "data":"ડેટા"},
    "punjabi": {"title":"ਸਿਰਲੇਖ", "header":"ਭਾਗ", "label":"ਲੇਬਲ", "caption":"ਜਾਣਕਾਰੀ", "button":"ਜਾਰੀ ਰੱਖੋ", "error":"ਗਲਤੀ ਹੋਈ।", "option":"ਵਿਕਲਪ", "column":"ਕਾਲਮ", "score":"ਸਕੋਰ", "model":"ਮਾਡਲ", "data":"ਡਾਟਾ"},
    "odia": {"title":"ଶୀର୍ଷକ", "header":"ବିଭାଗ", "label":"ଲେବେଲ", "caption":"ସୂଚନା", "button":"ଆଗକୁ ବଢ଼ନ୍ତୁ", "error":"ତ୍ରୁଟି ଘଟିଛି।", "option":"ବିକଳ୍ପ", "column":"ସ୍ତମ୍ଭ", "score":"ସ୍କୋର", "model":"ମଡେଲ", "data":"ତଥ୍ୟ"},
}
def _legacy_local_copy(key, lang):
    words = _UI_WORD_COPY.get(lang, _UI_WORD_COPY['english'])
    lowered = key.lower()
    for token in ("error", "invalid", "failed", "denied"):
        if token in lowered: return words["error"]
    for token in ("button", "download", "upload", "login", "logout", "clear", "send", "save"):
        if token in lowered: return words["button"]
    for token in ("title", "name"): 
        if token in lowered: return words["title"]
    for token in ("header", "section", "dashboard", "distribution", "trend", "history", "comparison"):
        if token in lowered: return words["header"]
    for token in ("label", "column", "col_", "axis", "metric", "option"):
        if token in lowered: return words["label"]
    if "model" in lowered: return words["model"]
    if "score" in lowered or "confidence" in lowered: return words["score"]
    if "data" in lowered or "csv" in lowered: return words["data"]
    return _UI_GENERIC_COPY[lang]
for _key, _block in _UI_RAW.items():
    for _lang in _FULL_LANGS:
        _block.setdefault(_lang, _legacy_local_copy(_key, _lang))

_UI_RAW.update({
    "chatbot_thinking": {"english": "Thinking…", "tamil": "சிந்திக்கிறது…", "telugu": "ఆలోచిస్తోంది…", "kannada": "ಆಲೋಚಿಸುತ್ತಿದೆ…", "malayalam": "ചിന്തിക്കുന്നു…", "hindi": "सोच रहा हूँ…", "bengali": "ভাবছি…", "marathi": "विचार करत आहे…", "gujarati": "વિચારી રહ્યું છે…", "punjabi": "ਸੋਚ ਰਿਹਾ ਹਾਂ…", "odia": "ଚିନ୍ତା କରୁଛି…"},
    "chatbot_offtopic": {"english": "I’m your Paddy Farming Assistant. I can help with paddy diseases, crop health, treatment, prevention, cultivation, and related questions.", "tamil": "நான் உங்கள் நெல் விவசாய உதவியாளர். நெல் நோய்கள், பயிர் ஆரோக்கியம், சிகிச்சை, தடுப்பு மற்றும் சாகுபடி தொடர்பான கேள்விகளில் உதவ முடியும்.", "telugu": "నేను మీ వరి వ్యవసాయ సహాయకుడిని. వరి వ్యాధులు, పంట ఆరోగ్యం, చికిత్స, నివారణ మరియు సాగుకు సంబంధించిన ప్రశ్నల్లో సహాయం చేయగలను.", "kannada": "ನಾನು ನಿಮ್ಮ ಭತ್ತ ಕೃಷಿ ಸಹಾಯಕ. ಭತ್ತದ ರೋಗಗಳು, ಬೆಳೆ ಆರೋಗ್ಯ, ಚಿಕಿತ್ಸೆ, ತಡೆಗಟ್ಟುವಿಕೆ ಮತ್ತು ಕೃಷಿಗೆ ಸಂಬಂಧಿಸಿದ ಪ್ರಶ್ನೆಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ.", "malayalam": "ഞാൻ നിങ്ങളുടെ നെൽകൃഷി സഹായി. നെൽ രോഗങ്ങൾ, വിള ആരോഗ്യം, ചികിത്സ, പ്രതിരോധം, കൃഷി എന്നിവയുമായി ബന്ധപ്പെട്ട ചോദ്യങ്ങളിൽ സഹായിക്കാം.", "hindi": "मैं आपका धान कृषि सहायक हूँ। मैं धान के रोग, फसल स्वास्थ्य, उपचार, रोकथाम, खेती और संबंधित प्रश्नों में मदद कर सकता हूँ।", "bengali": "আমি আপনার ধান চাষ সহায়ক। ধানের রোগ, ফসলের স্বাস্থ্য, চিকিৎসা, প্রতিরোধ, চাষাবাদ ও সংশ্লিষ্ট প্রশ্নে সাহায্য করতে পারি।", "marathi": "मी तुमचा भात शेती सहाय्यक आहे. भाताचे रोग, पिकाचे आरोग्य, उपचार, प्रतिबंध, लागवड आणि संबंधित प्रश्नांमध्ये मदत करू शकतो.", "gujarati": "હું તમારો ડાંગર ખેતી સહાયક છું. ડાંગરના રોગો, પાકનું આરોગ્ય, સારવાર, નિવારણ, ખેતી અને સંબંધિત પ્રશ્નોમાં મદદ કરી શકું છું.", "punjabi": "ਮੈਂ ਤੁਹਾਡਾ ਝੋਨਾ ਖੇਤੀ ਸਹਾਇਕ ਹਾਂ। ਮੈਂ ਝੋਨੇ ਦੀਆਂ ਬਿਮਾਰੀਆਂ, ਫਸਲ ਦੀ ਸਿਹਤ, ਇਲਾਜ, ਰੋਕਥਾਮ, ਕਾਸ਼ਤ ਅਤੇ ਸੰਬੰਧਿਤ ਸਵਾਲਾਂ ਵਿੱਚ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ।", "odia": "ମୁଁ ଆପଣଙ୍କର ଧାନ ଚାଷ ସହାୟକ। ଧାନ ରୋଗ, ଫସଲ ସ୍ୱାସ୍ଥ୍ୟ, ଚିକିତ୍ସା, ପ୍ରତିରୋଧ, ଚାଷ ଏବଂ ସମ୍ବନ୍ଧିତ ପ୍ରଶ୍ନରେ ସାହାଯ୍ୟ କରିପାରିବି।"},
})

_UI_RAW.update({
    "chatbot_service_unavailable": {"english": "🌾 I’m temporarily unable to reach the AI services. Please ask a Paddy-related question about diseases, symptoms, treatment, prevention, cultivation, fertilizer, irrigation, or crop health.", "tamil": "🌾 AI சேவைகளை தற்போது அணுக முடியவில்லை. நெல் நோய், அறிகுறிகள், சிகிச்சை, தடுப்பு, சாகுபடி, உரம், நீர்ப்பாசனம் அல்லது பயிர் ஆரோக்கியம் பற்றி கேளுங்கள்.", "telugu": "🌾 ప్రస్తుతం AI సేవలను చేరుకోలేకపోతున్నాను. వరి వ్యాధులు, లక్షణాలు, చికిత్స, నివారణ, సాగు, ఎరువులు, నీటిపారుదల లేదా పంట ఆరోగ్యం గురించి అడగండి.", "kannada": "🌾 ಪ್ರಸ್ತುತ AI ಸೇವೆಗಳನ್ನು ತಲುಪಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ. ಭತ್ತದ ರೋಗಗಳು, ಲಕ್ಷಣಗಳು, ಚಿಕಿತ್ಸೆ, ತಡೆಗಟ್ಟುವಿಕೆ, ಕೃಷಿ, ಗೊಬ್ಬರ, ನೀರಾವರಿ ಅಥವಾ ಬೆಳೆ ಆರೋಗ್ಯದ ಬಗ್ಗೆ ಕೇಳಿ.", "malayalam": "🌾 AI സേവനങ്ങളിലേക്ക് ഇപ്പോൾ എത്തിച്ചേരാൻ കഴിയുന്നില്ല. നെൽ രോഗങ്ങൾ, ലക്ഷണങ്ങൾ, ചികിത്സ, പ്രതിരോധം, കൃഷി, വളം, ജലസേചനം, വിള ആരോഗ്യം എന്നിവയെക്കുറിച്ച് ചോദിക്കൂ.", "hindi": "🌾 AI सेवाएं अभी उपलब्ध नहीं हैं। धान के रोग, लक्षण, उपचार, रोकथाम, खेती, उर्वरक, सिंचाई या फसल स्वास्थ्य के बारे में पूछें।", "bengali": "🌾 এই মুহূর্তে AI পরিষেবায় সংযোগ করা যাচ্ছে না। ধানের রোগ, লক্ষণ, চিকিৎসা, প্রতিরোধ, চাষ, সার, সেচ বা ফসলের স্বাস্থ্য সম্পর্কে জিজ্ঞাসা করুন।", "marathi": "🌾 सध्या AI सेवांशी संपर्क होऊ शकत नाही. भाताचे रोग, लक्षणे, उपचार, प्रतिबंध, लागवड, खत, सिंचन किंवा पिकाच्या आरोग्याबद्दल विचारा.", "gujarati": "🌾 હાલમાં AI સેવાઓ સાથે જોડાઈ શકાતું નથી. ડાંગરના રોગો, લક્ષણો, સારવાર, નિવારણ, ખેતી, ખાતર, સિંચાઈ અથવા પાકના આરોગ્ય વિશે પૂછો.", "punjabi": "🌾 ਇਸ ਸਮੇਂ AI ਸੇਵਾਵਾਂ ਨਾਲ ਜੁੜਿਆ ਨਹੀਂ ਜਾ ਸਕਦਾ। ਝੋਨੇ ਦੀਆਂ ਬਿਮਾਰੀਆਂ, ਲੱਛਣ, ਇਲਾਜ, ਰੋਕਥਾਮ, ਕਾਸ਼ਤ, ਖਾਦ, ਸਿੰਚਾਈ ਜਾਂ ਫਸਲ ਦੀ ਸਿਹਤ ਬਾਰੇ ਪੁੱਛੋ।", "odia": "🌾 ବର୍ତ୍ତମାନ AI ସେବା ସହିତ ଯୋଗାଯୋଗ ହୋଇପାରୁନାହିଁ। ଧାନ ରୋଗ, ଲକ୍ଷଣ, ଚିକିତ୍ସା, ପ୍ରତିରୋଧ, ଚାଷ, ସାର, ଜଳସେଚନ କିମ୍ବା ଫସଲ ସ୍ୱାସ୍ଥ୍ୟ ବିଷୟରେ ପଚାରନ୍ତୁ।"},
})
