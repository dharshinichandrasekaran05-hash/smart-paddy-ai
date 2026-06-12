"""
utils/ai_expert.py — Smart Paddy AI: AI Chatbot & Recommendation Engine
Place at: smart_paddy_ai/utils/ai_expert.py

Modular agriculture chatbot supporting:
  - Disease-specific guidance
  - Fertilizer advice
  - Irrigation suggestions
  - Crop care tips
  - Both English and Tamil responses
"""

from __future__ import annotations
import re


# ─────────────────────── INTENT PATTERNS ──────────────────────
_INTENTS = [
    # (pattern_list, handler_key)
    (["blast", "leaf blast", "fungus", "fungal"],      "blast"),
    (["brown spot", "brown"],                           "brown_spot"),
    (["tungro", "virus", "yellow leaf"],                "tungro"),
    (["fertilizer", "fertiliser", "npk", "urea", "dap", "potassium", "nitrogen"], "fertilizer"),
    (["water", "irrigation", "watering", "moisture", "flood"], "irrigation"),
    (["weather", "rain", "temperature", "forecast"],   "weather"),
    (["price", "msp", "cost", "market", "mandi"],      "price"),
    (["pest", "insect", "leafhopper", "bug", "spray"], "pest"),
    (["soil", "soil test", "ph", "nutrient"],          "soil"),
    (["healthy", "good crop", "no disease"],           "healthy"),
    (["harvest", "yield", "reaping", "paddy ready"],   "harvest"),
    (["seed", "variety", "germination", "nursery"],    "seed"),
    (["organic", "bio", "natural farming", "compost"], "organic"),
]

# ─────────────────────── RESPONSES ────────────────────────────
_RESPONSES: dict[str, dict[str, str]] = {
    "blast": {
        "english": (
            "🍃 **Rice Blast (Magnaporthe oryzae)**\n\n"
            "**Symptoms:** Spindle-shaped lesions with grey centers on leaves.\n\n"
            "**Treatment:** Spray Tricyclazole 75 WP @ 0.6 g/L. "
            "Apply at early morning or evening. Repeat after 10–14 days.\n\n"
            "**Prevention:** Use resistant varieties; avoid excess nitrogen; "
            "ensure good drainage and plant spacing."
        ),
        "tamil": (
            "🍃 **நெல் பிளாஸ்ட் நோய்**\n\n"
            "**அறிகுறிகள்:** இலைகளில் சாம்பல் நிற வடிவ புண்கள்.\n\n"
            "**சிகிச்சை:** டிரைசைக்கிளசோல் 75 WP @ 0.6 கி/லி தெளிக்கவும். "
            "காலை அல்லது மாலை தெளிக்கவும்.\n\n"
            "**தடுப்பு:** எதிர்ப்பு ரகங்கள் பயன்படுத்தவும்; அதிக நைட்ரஜன் தவிர்க்கவும்."
        ),
    },
    "brown_spot": {
        "english": (
            "🟤 **Brown Spot (Bipolaris oryzae)**\n\n"
            "**Cause:** Fungal disease worsened by potassium/silicon deficiency.\n\n"
            "**Treatment:** Mancozeb 75 WP @ 2.5 g/L spray. "
            "Foliar spray of Zinc Sulphate @ 0.5%.\n\n"
            "**Fertilizer fix:** Apply balanced NPK + organic manure."
        ),
        "tamil": (
            "🟤 **பழுப்பு புள்ளி நோய்**\n\n"
            "**காரணம்:** பொட்டாசியம் குறைபாடு மற்றும் பூஞ்சை.\n\n"
            "**சிகிச்சை:** மாங்கோசெப் 75 WP @ 2.5 கி/லி தெளிக்கவும். "
            "துத்தநாக சல்பேட் @ 0.5% தெளிக்கவும்.\n\n"
            "**உரம்:** சம விகித NPK + தொழு உரம் இடவும்."
        ),
    },
    "tungro": {
        "english": (
            "🦠 **Rice Tungro Disease (Viral)**\n\n"
            "**Vector:** Green Leafhopper (Nephotettix virescens).\n\n"
            "**Action:** Remove and destroy infected plants immediately. "
            "Spray Imidacloprid 17.8 SL @ 0.3 mL/L to control vectors.\n\n"
            "**Prevention:** Adjust planting date; remove weed hosts; "
            "use resistant varieties."
        ),
        "tamil": (
            "🦠 **நெல் டங்க்ரோ நோய் (வைரஸ்)**\n\n"
            "**பரவும் பூச்சி:** பச்சை தத்துப்பூச்சி.\n\n"
            "**நடவடிக்கை:** பாதிக்கப்பட்ட செடிகளை உடனே அகற்றவும். "
            "இமிடாக்ளோப்ரிட் 17.8 SL @ 0.3 மிலி/லி தெளிக்கவும்.\n\n"
            "**தடுப்பு:** நடவு நேரம் மாற்றவும்; களைகளை அகற்றவும்."
        ),
    },
    "fertilizer": {
        "english": (
            "🌱 **Fertilizer Guidance for Paddy**\n\n"
            "**Recommended NPK:** 120:60:60 kg/ha (Nitrogen : Phosphorus : Potassium)\n\n"
            "**Stages:**\n"
            "• Basal: Apply full P + K + 1/3 N at transplanting.\n"
            "• Tillering (21 DAT): 1/3 N as Urea.\n"
            "• Panicle initiation (42 DAT): Remaining 1/3 N.\n\n"
            "**Micronutrients:** Zinc Sulphate @ 25 kg/ha in first season."
        ),
        "tamil": (
            "🌱 **நெல் உர வழிகாட்டுதல்**\n\n"
            "**NPK பரிந்துரை:** 120:60:60 கி/ஹெக்.\n\n"
            "**கட்டங்கள்:**\n"
            "• நடவு: முழு P+K + 1/3 N இடவும்.\n"
            "• கண்ணே பருவம் (21 DAT): 1/3 N யூரியா.\n"
            "• கதிர் தொடக்கம் (42 DAT): மீதமுள்ள 1/3 N.\n\n"
            "**நுண்ணூட்டம்:** துத்தநாக சல்பேட் @ 25 கி/ஹெக்."
        ),
    },
    "irrigation": {
        "english": (
            "💧 **Irrigation Advice for Paddy**\n\n"
            "**Recommended:** Alternate Wetting and Drying (AWD) method.\n\n"
            "• Flood to 5 cm → allow to dry to 15 cm below soil → re-flood.\n"
            "• AWD saves 30% water vs continuous flooding.\n"
            "• Critical stages needing constant water: flowering and grain filling.\n\n"
            "**Avoid:** Water stress at panicle initiation and anthesis stages."
        ),
        "tamil": (
            "💧 **நெல் நீர் மேலாண்மை**\n\n"
            "**பரிந்துரை:** மாற்று நனைப்பு மற்றும் உலர்த்தல் (AWD) முறை.\n\n"
            "• 5 செமீ நீர் நிரப்பு → மண் 15 செமீ கீழ் நிலைவரை வற்ற விடு → மீண்டும் நிரப்பு.\n"
            "• தொடர் நீர் தேக்கத்தை விட 30% நீர் சேமிப்பு.\n\n"
            "**முக்கியம்:** பூக்கும் காலம் மற்றும் தானிய நிரப்பு கட்டத்தில் தொடர்ந்து நீர் தேவை."
        ),
    },
    "weather": {
        "english": (
            "🌦️ **Weather Advisory**\n\n"
            "Check the India Meteorological Department (IMD) website or Meghdoot app "
            "for localised 5-day forecasts before spraying or major operations.\n\n"
            "**Tips:**\n"
            "• Spray fungicides only when no rain is forecast for 4+ hours.\n"
            "• Delay transplanting if heavy rain (>50 mm/day) is expected.\n"
            "• Wind speed < 15 km/h is ideal for spray operations."
        ),
        "tamil": (
            "🌦️ **வானிலை ஆலோசனை**\n\n"
            "IMD இணையதளம் அல்லது Meghdoot செயலியில் 5-நாள் வானிலை முன்னறிவிப்பு பார்க்கவும்.\n\n"
            "• மழை இல்லாத 4 மணி நேரத்திற்குப் பிறகு பூஞ்சைக்கொல்லி தெளிக்கவும்.\n"
            "• 50 மிமீ/நாள் மழை எதிர்பார்க்கும்போது நடவு தவிர்க்கவும்."
        ),
    },
    "price": {
        "english": (
            "📊 **Crop Price Information**\n\n"
            "Crop prices change daily. Check:\n"
            "• **eNAM portal** (enam.gov.in) for real-time mandi prices.\n"
            "• **Agmarknet** (agmarknet.gov.in) for district-level prices.\n"
            "• **State Agriculture Dept** website for MSP announcements.\n\n"
            "Current MSP for paddy (Common): ₹2,183/quintal (as per last announcement)."
        ),
        "tamil": (
            "📊 **பயிர் விலை தகவல்**\n\n"
            "தினசரி விலை மாற்றம் ஏற்படும். இந்த இணையதளங்களில் பார்க்கவும்:\n"
            "• eNAM போர்டல் (enam.gov.in)\n"
            "• Agmarknet (agmarknet.gov.in)\n\n"
            "தற்போதைய MSP: ₹2,183/குவிண்டால் (சாதா நெல்)."
        ),
    },
    "pest": {
        "english": (
            "🐛 **Pest Management for Paddy**\n\n"
            "**Common pests:** Brown planthopper (BPH), Green leafhopper, Stem borer, Gall midge.\n\n"
            "**IPM Approach:**\n"
            "• Use light traps to monitor pest populations.\n"
            "• Spray neem-based pesticides (Azadirachtin 1500 ppm) as first line.\n"
            "• For BPH: Buprofezin 25 SC @ 1.6 mL/L or Imidacloprid @ 0.3 mL/L.\n"
            "• For stem borer: Cartap hydrochloride 4G @ 18 kg/ha."
        ),
        "tamil": (
            "🐛 **நெல் பூச்சி மேலாண்மை**\n\n"
            "**பொதுவான பூச்சிகள்:** புயல் தத்துப்பூச்சி, பச்சை தத்துப்பூச்சி, தண்டு துளைப்பான்.\n\n"
            "• வேப்பம் அடிப்படையிலான பூச்சிக்கொல்லி முதலில் பயன்படுத்தவும்.\n"
            "• புயல் தத்துப்பூச்சிக்கு: இமிடாக்ளோப்ரிட் @ 0.3 மிலி/லி.\n"
            "• தண்டு துளைப்பானுக்கு: கார்டேப் ஹைட்ரோகுளோரைட் 4G @ 18 கி/ஹெக்."
        ),
    },
    "soil": {
        "english": (
            "🌍 **Soil Health for Paddy**\n\n"
            "**Ideal pH:** 5.5 – 6.5\n\n"
            "• Get a soil test done at your nearest Soil Testing Laboratory every 3 years.\n"
            "• Apply lime if pH < 5.5; gypsum if pH > 7.0.\n"
            "• Add FYM @ 12.5 t/ha to improve soil organic matter.\n"
            "• Use Soil Health Card recommendations for precise fertilizer application."
        ),
        "tamil": (
            "🌍 **நெல் மண் ஆரோக்கியம்**\n\n"
            "**சிறந்த pH:** 5.5 – 6.5\n\n"
            "• 3 ஆண்டுகளுக்கு ஒரு முறை மண் பரிசோதனை செய்யவும்.\n"
            "• pH < 5.5 ஆனால் சுண்ணாம்பு இடவும்; pH > 7.0 ஆனால் ஜிப்சம் இடவும்.\n"
            "• FYM @ 12.5 ட/ஹெக் இடவும்."
        ),
    },
    "healthy": {
        "english": (
            "✅ **Crop Health Maintenance**\n\n"
            "Your crop appears healthy. Here's how to keep it that way:\n\n"
            "• **Weekly scouting:** Check for early disease or pest signs.\n"
            "• **Balanced nutrition:** Don't over-apply nitrogen.\n"
            "• **AWD irrigation:** Saves water, reduces methane, deters pests.\n"
            "• **Weed management:** Manual or herbicide weeding at 20 and 40 DAT."
        ),
        "tamil": (
            "✅ **ஆரோக்கியமான பயிர் பராமரிப்பு**\n\n"
            "உங்கள் பயிர் நலமாக உள்ளது. தொடர்ந்து பராமரிக்க:\n\n"
            "• வாராந்திர கண்காணிப்பு செய்யவும்.\n"
            "• சம விகித NPK உரம் இடவும்.\n"
            "• மாற்று நனைப்பு முறை பின்பற்றவும்.\n"
            "• 20 மற்றும் 40 DAT-ல் களை நீக்கம் செய்யவும்."
        ),
    },
    "harvest": {
        "english": (
            "🌾 **Harvest Guidance**\n\n"
            "• Harvest when 85–90% of grains are golden yellow.\n"
            "• Grain moisture should be 20–25% at harvest.\n"
            "• Dry to 14% moisture for safe storage.\n"
            "• Use combine harvester or reaper-binder for large fields.\n"
            "• Avoid harvesting during or right after heavy rain."
        ),
        "tamil": (
            "🌾 **அறுவடை வழிகாட்டுதல்**\n\n"
            "• 85–90% தானியங்கள் தங்க மஞ்சள் நிறம் ஆகும்போது அறுவடை செய்யவும்.\n"
            "• அறுவடை நேரத்தில் ஈரப்பதம் 20–25% இருக்க வேண்டும்.\n"
            "• சேமிப்புக்கு 14% ஈரப்பதமாக உலர்த்தவும்."
        ),
    },
    "seed": {
        "english": (
            "🌱 **Seed Selection & Nursery Tips**\n\n"
            "• Use certified seeds from government-approved sources.\n"
            "• Soak seeds in salt water (1 kg salt in 10 L water); use seeds that sink.\n"
            "• Treat with Carbendazim @ 2 g/kg seed before sowing.\n"
            "• Raise nursery in well-prepared beds; apply FYM.\n"
            "• Transplant 21–25-day-old seedlings at 2–3 per hill."
        ),
        "tamil": (
            "🌱 **விதை தேர்வு மற்றும் நாற்றங்கால் குறிப்புகள்**\n\n"
            "• அரசு அங்கீகரிக்கப்பட்ட விதைகளை பயன்படுத்தவும்.\n"
            "• உப்பு நீரில் (10 லி நீரில் 1 கி உப்பு) மூழ்கும் விதைகள் எடுக்கவும்.\n"
            "• கார்பென்டாசிம் @ 2 கி/கி விதை சோக்கவும்.\n"
            "• 21–25 நாள் நாற்றுகளை மலைக்கு 2–3 நடவும்."
        ),
    },
    "organic": {
        "english": (
            "♻️ **Organic / Natural Farming Tips**\n\n"
            "• **Green manure:** Incorporate Sesbania (Dhaincha) before transplanting.\n"
            "• **Vermicompost:** Apply @ 2–3 t/ha for improved soil health.\n"
            "• **Jeevamrutha:** Mix 200 L cow dung + 200 L cow urine + 2 kg jaggery "
            "+ 2 kg pulse flour in 1000 L water; apply 200 L/acre.\n"
            "• **Panchagavya:** 3% foliar spray at tillering and panicle initiation."
        ),
        "tamil": (
            "♻️ **இயற்கை விவசாய குறிப்புகள்**\n\n"
            "• பசுந்தாள் உரம் (செஸ்பேனியா) நடவிற்கு முன் சேர்க்கவும்.\n"
            "• மண்புழு உரம் @ 2–3 ட/ஹெக் இடவும்.\n"
            "• ஜீவாமிர்தம்: பசுவின் சாணம் 200 லி + கோமியம் 200 லி + வெல்லம் 2 கி + "
            "பருப்பு மாவு 2 கி → 1000 லி நீரில் கலந்து ஏக்கருக்கு 200 லி இடவும்."
        ),
    },
    "default": {
        "english": (
            "🤖 **Smart Paddy AI Assistant**\n\n"
            "I can help you with:\n"
            "• **Diseases:** blast, brown spot, tungro\n"
            "• **Fertilizer** planning and timing\n"
            "• **Irrigation** methods (AWD)\n"
            "• **Pest management**\n"
            "• **Soil health** and testing\n"
            "• **Harvest** guidance\n"
            "• **Weather** advisory tips\n\n"
            "Try asking: *'How to treat blast disease?'* or *'When should I irrigate?'*"
        ),
        "tamil": (
            "🤖 **ஸ்மார்ட் பேடி AI உதவியாளர்**\n\n"
            "நான் இவற்றில் உதவ முடியும்:\n"
            "• நோய்கள்: பிளாஸ்ட், பழுப்பு புள்ளி, டங்க்ரோ\n"
            "• உர திட்டமிடல்\n"
            "• நீர்ப்பாசன முறைகள்\n"
            "• பூச்சி மேலாண்மை\n"
            "• மண் ஆரோக்கியம்\n\n"
            "கேளுங்கள்: *'பிளாஸ்ட் நோய் சிகிச்சை என்ன?'*"
        ),
    },
}


# ─────────────────────── INTENT DETECTION ─────────────────────
def _detect_intent(query: str, disease: str | None) -> str:
    """
    Classify a user query into an intent key.
    Disease context from prediction takes priority.
    """
    q = query.lower()

    # Disease-seeded intent
    if disease:
        d = disease.lower()
        if "blast" in d:
            return "blast"
        if "brown" in d:
            return "brown_spot"
        if "tungro" in d:
            return "tungro"
        if "healthy" in d:
            return "healthy"

    # Pattern-match the query
    for patterns, intent in _INTENTS:
        if any(p in q for p in patterns):
            return intent

    return "default"


# ─────────────────────── PUBLIC API ───────────────────────────
def smart_farming_bot(
    query:   str,
    disease: str | None = None,
    lang:    str = "english",
) -> str:
    """
    Main chatbot entry point.

    Parameters
    ----------
    query   : user's question string
    disease : predicted disease name (from model), or None
    lang    : "english" or "tamil"

    Returns
    -------
    Formatted markdown response string
    """
    intent   = _detect_intent(query, disease)
    response = _RESPONSES.get(intent, _RESPONSES["default"])
    return response.get(lang, response["english"])