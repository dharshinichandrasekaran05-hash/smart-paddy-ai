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
    return block.get(lang, block["english"])


# ═══════════════════════════════════════════════════════════════
# UI LABELS
# ═══════════════════════════════════════════════════════════════
# Every key below MUST exist for every language in LANGUAGE_ORDER + "english".
_UI_RAW = {
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
}


def get_ui_labels(lang: str) -> dict:
    """Return the full UI-label dict for a given language (English fallback per key)."""
    lang = resolve_lang(lang)
    return {key: block.get(lang, block["english"]) for key, block in _UI_RAW.items()}


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
    return _RISK_RAW.get(level, _RISK_RAW["low"]).get(lang, _RISK_RAW[level]["english"])


def action_text(level: str, lang: str) -> str:
    lang = resolve_lang(lang)
    return _ACTION_RAW.get(level, _ACTION_RAW["low"]).get(lang, _ACTION_RAW[level]["english"])


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
    "english": ["How to treat blast?", "Fertilizer schedule", "Irrigation tips", "Pest control"],
    "tamil": ["பிளாஸ்ட் சிகிச்சை?", "உர அட்டவணை", "நீர்ப்பாசன குறிப்புகள்", "பூச்சி மேலாண்மை"],
    "telugu": ["బ్లాస్ట్ చికిత్స ఎలా?", "ఎరువుల షెడ్యూల్", "నీటిపారుదల చిట్కాలు", "పురుగు నియంత్రణ"],
    "kannada": ["ಬ್ಲಾಸ್ಟ್ ಚಿಕಿತ್ಸೆ ಹೇಗೆ?", "ಗೊಬ್ಬರ ವೇಳಾಪಟ್ಟಿ", "ನೀರಾವರಿ ಸಲಹೆಗಳು", "ಕೀಟ ನಿಯಂತ್ರಣ"],
    "malayalam": ["ബ്ലാസ്റ്റ് ചികിത്സ എങ്ങനെ?", "വളം ഷെഡ്യൂൾ", "ജലസേചന നുറുങ്ങുകൾ", "കീട നിയന്ത്രണം"],
    "hindi": ["ब्लास्ट का उपचार कैसे करें?", "उर्वरक अनुसूची", "सिंचाई सुझाव", "कीट नियंत्रण"],
    "bengali": ["ব্লাস্ট রোগের চিকিৎসা কীভাবে?", "সার সময়সূচী", "সেচের টিপস", "পোকা নিয়ন্ত্রণ"],
    "marathi": ["ब्लास्टवर उपचार कसे करावे?", "खत वेळापत्रक", "सिंचन टिप्स", "किड नियंत्रण"],
    "gujarati": ["બ્લાસ્ટની સારવાર કેવી રીતે?", "ખાતર સમયપત્રક", "સિંચાઈ ટિપ્સ", "જીવાત નિયંત્રણ"],
    "punjabi": ["ਬਲਾਸਟ ਦਾ ਇਲਾਜ ਕਿਵੇਂ ਕਰੀਏ?", "ਖਾਦ ਸਮਾਂ-ਸਾਰਣੀ", "ਸਿੰਚਾਈ ਸੁਝਾਅ", "ਕੀੜੇ ਕੰਟਰੋਲ"],
    "odia": ["ବ୍ଲାଷ୍ଟର ଚିକିତ୍ସା କିପରି?", "ସାର ସମୟସୂଚୀ", "ଜଳସେଚନ ଟିପ୍ସ", "ପୋକ ନିୟନ୍ତ୍ରଣ"],
}


def chatbot_greeting(lang: str) -> str:
    lang = resolve_lang(lang)
    return _GREETING_RAW.get(lang, _GREETING_RAW["english"])


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
    return block.get(lang, value)
