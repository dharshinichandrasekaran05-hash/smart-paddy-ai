"""
utils/advisory.py — Smart Paddy AI: Agricultural Advisory Engine
"""

_ADVICE = {
    # ── 1. BLAST ──────────────────────────────────────────────
    "blast": {
        "english": {
            "description": (
                "Rice Blast (Magnaporthe oryzae) is a destructive fungal disease "
                "affecting leaves, nodes, necks, and panicles."
            ),
            "treatment": [
                "Spray Tricyclazole 75 WP @ 0.6 g/L or Isoprothiolane 40 EC @ 1.5 mL/L.",
                "Apply fungicide at early morning or evening for best absorption.",
                "Repeat spray after 10–14 days if symptoms persist.",
            ],
            "prevention": [
                "Use blast-resistant varieties (ADT 43, CO 51).",
                "Avoid excess nitrogen application.",
                "Maintain proper spacing for air circulation.",
                "Drain field for 3–4 days during infection risk.",
            ],
            "fertilizer": "Reduce nitrogen, increase potassium (MOP @ 50 kg/ha).",
            "irrigation": "Drain excess water; alternate wetting and drying (AWD) method.",
        },
        "tamil": {
            "description": (
                "நெல் பிளாஸ்ட் (Magnaporthe oryzae) என்பது இலை, தண்டு மற்றும் "
                "கதிர்களை பாதிக்கும் பூஞ்சை நோய்."
            ),
            "treatment": [
                "டிரைசைக்கிளசோல் 75 WP @ 0.6 கி/லி அல்லது இசோபுரோத்தியோலேன் 40 EC @ 1.5 மிலி/லி தெளிக்கவும்.",
                "காலை அல்லது மாலை நேரத்தில் மருந்து தெளிக்கவும்.",
                "10–14 நாட்களுக்கு பிறகு மீண்டும் தெளிக்கவும்.",
            ],
            "prevention": [
                "நோய் எதிர்ப்பு திறன் கொண்ட ரகங்களை (ADT 43) பயன்படுத்தவும்.",
                "அதிக நைட்ரஜன் உரம் தவிர்க்கவும்.",
                "சரியான இடைவெளியில் நடவு செய்யவும்.",
            ],
            "fertilizer": "நைட்ரஜன் குறைத்து பொட்டாசியம் உரம் (MOP @ 50 கி/ஹெக்.) இடவும்.",
            "irrigation": "மாற்று நனைப்பு மற்றும் உலர்த்தல் முறையை பயன்படுத்தவும்.",
        },
    },

    # ── 2. BROWN SPOT ─────────────────────────────────────────
    "brown spot": {
        "english": {
            "description": (
                "Brown Spot (Bipolaris oryzae) is a fungal disease linked to "
                "nutritional deficiency, especially potassium and silicon."
            ),
            "treatment": [
                "Apply Mancozeb 75 WP @ 2.5 g/L or Iprobenfos 48 EC @ 1.0 mL/L.",
                "Foliar spray of Zinc Sulphate @ 0.5% to correct micronutrient deficiency.",
            ],
            "prevention": [
                "Apply balanced NPK fertilizer.",
                "Use silicon-rich amendments or slag.",
                "Avoid water stress during crop growth.",
            ],
            "fertilizer": "Apply FYM @ 12.5 t/ha + NPK 120:60:60 kg/ha.",
            "irrigation": "Maintain 2–3 cm water depth consistently.",
        },
        "tamil": {
            "description": (
                "பழுப்பு புள்ளி நோய் (Bipolaris oryzae) ஊட்டச்சத்து குறைபாடு "
                "காரணமாக ஏற்படும் பூஞ்சை நோய்."
            ),
            "treatment": [
                "மாங்கோசெப் 75 WP @ 2.5 கி/லி தெளிக்கவும்.",
                "துத்தநாக சல்பேட் @ 0.5% தெளிப்பு மூலம் நுண்ணூட்டச்சத்து குறைபாட்டை சரிசெய்யவும்.",
            ],
            "prevention": [
                "சம விகித NPK உரம் பயன்படுத்தவும்.",
                "சிலிக்கன் உரம் இடவும்.",
            ],
            "fertilizer": "FYM @ 12.5 ட/ஹெக் + NPK 120:60:60 கி/ஹெக் இடவும்.",
            "irrigation": "2–3 செமீ நீர் ஆழம் சீராக பராமரிக்கவும்.",
        },
    },

    # ── 3. TUNGRO ─────────────────────────────────────────────
    "tungro": {
        "english": {
            "description": (
                "Rice Tungro Disease (RTD) is a viral disease transmitted by "
                "green leafhopper (Nephotettix virescens)."
            ),
            "treatment": [
                "No direct cure; remove and destroy infected plants immediately.",
                "Control vector insects: spray Imidacloprid 17.8 SL @ 0.3 mL/L.",
                "Apply neem-based pesticides as vector deterrent.",
            ],
            "prevention": [
                "Plant resistant varieties (TN1, IR36 are susceptible — avoid).",
                "Adjust planting time to avoid peak leafhopper season.",
                "Maintain field hygiene; remove weed hosts.",
            ],
            "fertilizer": "Balanced nutrition; avoid excess nitrogen that attracts leafhoppers.",
            "irrigation": "Drain nursery periodically to deter leafhopper population.",
        },
        "tamil": {
            "description": (
                "நெல் டங்க்ரோ நோய் பச்சை தத்துப்பூச்சியால் பரவும் வைரஸ் நோய்."
            ),
            "treatment": [
                "நேரடி சிகிச்சை இல்லை — பாதிக்கப்பட்ட செடிகளை உடனே அகற்றவும்.",
                "இமிடாக்ளோப்ரிட் 17.8 SL @ 0.3 மிலி/லி தெளிக்கவும்.",
                "வேப்பம் அடிப்படையிலான பூச்சிக்கொல்லி பயன்படுத்தவும்.",
            ],
            "prevention": [
                "எதிர்ப்பு திறன் ரகங்களை பயன்படுத்தவும்.",
                "தத்துப்பூச்சி அதிகரிக்கும் காலத்தை தவிர்த்து நடவு செய்யவும்.",
            ],
            "fertilizer": "அதிக நைட்ரஜன் தவிர்க்கவும் — இது பூச்சிகளை கவர்கிறது.",
            "irrigation": "நாற்றங்காலில் இடைவிடாத வடிகால் வசதி அமைக்கவும்.",
        },
    },

    # ── 4. BACTERIAL PANICLE BLIGHT ───────────────────────────
    "bacterial panicle blight": {
        "english": {
            "description": (
                "Bacterial Panicle Blight (Burkholderia glumae) causes grain sterility "
                "and discolouration of rice panicles, leading to significant yield loss."
            ),
            "treatment": [
                "Spray Copper Oxychloride 50 WP @ 3 g/L at panicle initiation stage.",
                "Apply Streptomycin Sulphate @ 0.5 g/L as foliar spray.",
                "Repeat spray after 7–10 days if infection persists.",
            ],
            "prevention": [
                "Use certified disease-free seeds.",
                "Treat seeds with hot water (52°C for 10 minutes) before sowing.",
                "Avoid high nitrogen doses which promote bacterial growth.",
                "Ensure proper field drainage to reduce humidity.",
            ],
            "fertilizer": "Reduce nitrogen; apply potassium (MOP @ 50 kg/ha) to strengthen crop.",
            "irrigation": "Avoid excessive irrigation; drain field periodically to reduce humidity.",
        },
        "tamil": {
            "description": (
                "பாக்டீரியல் பேனிக்கல் பிளைட் (Burkholderia glumae) நெல் கதிர்களில் "
                "விதை கருக்கல் மற்றும் நிற மாற்றம் ஏற்படுத்தி விளைச்சல் இழப்பை உண்டாக்கும்."
            ),
            "treatment": [
                "காப்பர் ஆக்சிகுளோரைடு 50 WP @ 3 கி/லி கதிர் தோன்றும் தருணத்தில் தெளிக்கவும்.",
                "ஸ்ட்ரெப்டோமைசின் சல்பேட் @ 0.5 கி/லி இலைத் தெளிப்பாக பயன்படுத்தவும்.",
                "7–10 நாட்களில் மீண்டும் தெளிக்கவும்.",
            ],
            "prevention": [
                "சான்றளிக்கப்பட்ட விதைகளை பயன்படுத்தவும்.",
                "விதைகளை 52°C சூடான நீரில் 10 நிமிடம் ஊற வைக்கவும்.",
                "அதிக நைட்ரஜன் உரம் தவிர்க்கவும்.",
                "வயலில் நல்ல வடிகால் வசதி அமைக்கவும்.",
            ],
            "fertilizer": "நைட்ரஜன் குறைத்து பொட்டாசியம் உரம் (MOP @ 50 கி/ஹெக்.) இடவும்.",
            "irrigation": "அதிக நீர்ப்பாசனம் தவிர்க்கவும்; வயலை இடையிடையே வடிகட்டவும்.",
        },
    },

    # ── 5. BACTERIAL LEAF BLIGHT ──────────────────────────────
    "bacterial leaf blight": {
        "english": {
            "description": (
                "Bacterial Leaf Blight (Xanthomonas oryzae pv. oryzae) causes water-soaked "
                "lesions on leaf margins that turn yellow then white, severely reducing photosynthesis."
            ),
            "treatment": [
                "Spray Copper Hydroxide 77 WP @ 2 g/L or Copper Oxychloride @ 3 g/L.",
                "Apply Streptomycin Sulphate + Tetracycline @ 0.5 g/L combination spray.",
                "Remove and burn severely infected leaves to reduce inoculum.",
            ],
            "prevention": [
                "Use resistant varieties (IR64, Swarna Sub1).",
                "Avoid flood irrigation that spreads bacteria.",
                "Use disease-free seedlings from certified nurseries.",
                "Avoid injuries to plants during transplanting.",
            ],
            "fertilizer": "Reduce nitrogen; apply silica (slag @ 500 kg/ha) to strengthen cell walls.",
            "irrigation": "Use clean water sources; avoid field-to-field water flow during outbreak.",
        },
        "tamil": {
            "description": (
                "பாக்டீரியல் இலை அழுகல் (Xanthomonas oryzae) நெல் இலை விளிம்பில் "
                "மஞ்சள் மற்றும் வெள்ளை புண்களை உண்டாக்கி ஒளிச்சேர்க்கையை குறைக்கும்."
            ),
            "treatment": [
                "காப்பர் ஹைட்ராக்சைடு 77 WP @ 2 கி/லி தெளிக்கவும்.",
                "ஸ்ட்ரெப்டோமைசின் + டெட்ராசைக்லின் @ 0.5 கி/லி கலந்து தெளிக்கவும்.",
                "கடுமையாக பாதிக்கப்பட்ட இலைகளை எரிக்கவும்.",
            ],
            "prevention": [
                "எதிர்ப்பு திறன் ரகங்களை (IR64) பயன்படுத்தவும்.",
                "வெள்ளப்பெருக்கு நீர்ப்பாசனம் தவிர்க்கவும்.",
                "சான்றளிக்கப்பட்ட நாற்றுகளை மட்டும் பயன்படுத்தவும்.",
            ],
            "fertilizer": "நைட்ரஜன் குறைத்து சிலிக்கா உரம் (ஸ்லாக் @ 500 கி/ஹெக்.) இடவும்.",
            "irrigation": "தூய்மையான நீர் பயன்படுத்தவும்; நோய் பரவும் போது வயல் இணைப்பு தவிர்க்கவும்.",
        },
    },

    # ── 6. BACTERIAL LEAF STREAK ──────────────────────────────
    "bacterial leaf streak": {
        "english": {
            "description": (
                "Bacterial Leaf Streak (Xanthomonas oryzae pv. oryzicola) causes narrow "
                "water-soaked interveinal streaks that turn brown, weakening the leaf structure."
            ),
            "treatment": [
                "Spray Copper Oxychloride 50 WP @ 3 g/L at early infection stage.",
                "Apply Bronopol-based bactericide as per label recommendation.",
                "Repeat application every 10 days during wet weather.",
            ],
            "prevention": [
                "Use certified disease-free seeds; avoid infected seed lots.",
                "Avoid overhead irrigation; use drip or furrow irrigation.",
                "Maintain wide row spacing for better air circulation.",
                "Remove volunteer rice and weed hosts from field borders.",
            ],
            "fertilizer": "Avoid excess nitrogen; maintain balanced K and Si nutrition.",
            "irrigation": "Minimize leaf wetness; irrigate at base of plants, not overhead.",
        },
        "tamil": {
            "description": (
                "பாக்டீரியல் இலை கோடு நோய் (Xanthomonas oryzae pv. oryzicola) "
                "இலை நரம்புகளுக்கு இடையே நீர் கசிவு கோடுகளை உண்டாக்கும்."
            ),
            "treatment": [
                "காப்பர் ஆக்சிகுளோரைடு 50 WP @ 3 கி/லி ஆரம்ப கட்டத்தில் தெளிக்கவும்.",
                "பிரோனோபால் அடிப்படை பாக்டீரியா மருந்தை பயன்படுத்தவும்.",
                "மழை காலத்தில் 10 நாட்களுக்கு ஒருமுறை தெளிக்கவும்.",
            ],
            "prevention": [
                "சான்றளிக்கப்பட்ட விதை பயன்படுத்தவும்.",
                "மேலிருந்து நீர்ப்பாசனம் தவிர்க்கவும்.",
                "சரியான இடைவெளியில் நடவு செய்யவும்.",
            ],
            "fertilizer": "அதிக நைட்ரஜன் தவிர்க்கவும்; பொட்டாசியம் மற்றும் சிலிக்கன் சீராக இடவும்.",
            "irrigation": "இலைகள் நனையாமல் தடுக்க வேர் பகுதியில் மட்டும் நீர் பாய்ச்சவும்.",
        },
    },

    # ── 7. DEAD HEART ─────────────────────────────────────────
    "dead heart": {
        "english": {
            "description": (
                "Dead Heart is caused by stem borer (Scirpophaga incertulas) larvae boring "
                "into rice stems during vegetative stage, killing the central shoot (dead heart)."
            ),
            "treatment": [
                "Apply Cartap Hydrochloride 4G @ 18 kg/ha as granules into standing water.",
                "Spray Chlorpyrifos 20 EC @ 2 mL/L or Fipronil 0.3 GR @ 25 kg/ha.",
                "Release Trichogramma japonicum egg parasitoids @ 50,000/ha/week.",
            ],
            "prevention": [
                "Clip and destroy egg masses from nursery seedlings before transplanting.",
                "Set up light traps to monitor and trap adult moths.",
                "Avoid synchronous planting in large areas — stagger planting dates.",
                "Maintain field hygiene; remove stubbles after harvest.",
            ],
            "fertilizer": "Apply potash (MOP @ 40 kg/ha) to strengthen stem tissue.",
            "irrigation": "Maintain 2–5 cm water level; flooding helps drown hatched larvae.",
        },
        "tamil": {
            "description": (
                "டெட் ஹார்ட் நோய் தண்டு துளைப்பான் (Scirpophaga incertulas) புழுக்களால் "
                "நெல் தண்டுகள் துளைக்கப்பட்டு மையத்தண்டு இறந்து போவதால் ஏற்படும்."
            ),
            "treatment": [
                "கார்டாப் ஹைட்ரோகுளோரைடு 4G @ 18 கி/ஹெக் நீர் நிறைந்த வயலில் இடவும்.",
                "குளோர்பைரிபாஸ் 20 EC @ 2 மிலி/லி தெளிக்கவும்.",
                "ட்ரைக்கோக்ராம்மா ஒட்டுண்ணிகளை @ 50,000/ஹெக்/வாரம் வெளியிடவும்.",
            ],
            "prevention": [
                "நாற்றுகளில் முட்டை கூட்டங்களை நடவிற்கு முன் அகற்றவும்.",
                "விளக்கு விளக்கு அமைத்து அந்துப்பூச்சிகளை கவர்ந்து அழிக்கவும்.",
                "ஒரே நேரத்தில் பெரிய பரப்பில் நடவு தவிர்க்கவும்.",
            ],
            "fertilizer": "பொட்டாசியம் உரம் (MOP @ 40 கி/ஹெக்.) இட்டு தண்டை வலுப்படுத்தவும்.",
            "irrigation": "2–5 செமீ நீர் ஆழம் பராமரிக்கவும்; வெள்ளம் புழுக்களை மூழ்கடிக்கும்.",
        },
    },

    # ── 8. HISPA ──────────────────────────────────────────────
    "hispa": {
        "english": {
            "description": (
                "Rice Hispa (Dicladispa armigera) is an insect pest whose larvae mine "
                "inside leaves causing white parallel streaks, while adults scrape leaf surfaces."
            ),
            "treatment": [
                "Spray Malathion 50 EC @ 2 mL/L or Chlorpyrifos 20 EC @ 2 mL/L.",
                "Apply Neem Seed Kernel Extract (NSKE) @ 5% as eco-friendly option.",
                "Hand-pick and destroy adults during early infestation.",
            ],
            "prevention": [
                "Clip infested leaf tips before transplanting to remove egg masses.",
                "Avoid dense planting; maintain recommended spacing.",
                "Use light traps during adult flight period.",
                "Keep field bunds free of grassy weeds that harbor adults.",
            ],
            "fertilizer": "Avoid excess nitrogen which causes lush growth attractive to hispa.",
            "irrigation": "Maintain shallow flooding; dry conditions worsen hispa population.",
        },
        "tamil": {
            "description": (
                "நெல் ஹிஸ்பா (Dicladispa armigera) பூச்சியின் புழுக்கள் இலைகளுக்குள் "
                "துளைத்து வெள்ளை கோடுகளை உண்டாக்கும்; பெரிய பூச்சிகள் இலை மேற்பரப்பை சுரண்டும்."
            ),
            "treatment": [
                "மலாத்தியான் 50 EC @ 2 மிலி/லி அல்லது குளோர்பைரிபாஸ் @ 2 மிலி/லி தெளிக்கவும்.",
                "வேப்பம் கொட்டை சாறு (NSKE) @ 5% தெளிக்கவும்.",
                "ஆரம்ப தொற்றில் பூச்சிகளை கையால் பொறுக்கி அழிக்கவும்.",
            ],
            "prevention": [
                "நடவிற்கு முன் பாதிக்கப்பட்ட இலை நுனிகளை கத்தரிக்கவும்.",
                "அடர்த்தியான நடவு தவிர்க்கவும்.",
                "விளக்கு விளக்கு பயன்படுத்தவும்.",
            ],
            "fertilizer": "அதிக நைட்ரஜன் தவிர்க்கவும் — இது பூச்சி தாக்குதலை அதிகரிக்கும்.",
            "irrigation": "ஆழமற்ற நீர் வைத்திருக்கவும்; வறட்சி ஹிஸ்பா பரவலை அதிகரிக்கும்.",
        },
    },

    # ── 9. DOWNY MILDEW ───────────────────────────────────────
    "downy mildew": {
        "english": {
            "description": (
                "Downy Mildew in rice (caused by Sclerophthora macrospora) produces "
                "yellowish leaf streaks and stunted, malformed tillers with grassy appearance."
            ),
            "treatment": [
                "Spray Metalaxyl + Mancozeb (Ridomil Gold) @ 2.5 g/L.",
                "Apply Fosetyl-Al 80 WP @ 3 g/L as systemic fungicide.",
                "Drain field immediately to reduce soil moisture and disease spread.",
            ],
            "prevention": [
                "Avoid waterlogged conditions; improve field drainage.",
                "Use tolerant varieties and treated certified seeds.",
                "Remove and destroy infected tillers and ratoon crops.",
                "Avoid excess irrigation especially during cool humid weather.",
            ],
            "fertilizer": "Apply phosphorus (SSP @ 250 kg/ha) to strengthen root health.",
            "irrigation": "Drain field immediately when symptoms appear; avoid waterlogging.",
        },
        "tamil": {
            "description": (
                "நெல் டவுனி மில்டியூ (Sclerophthora macrospora) மஞ்சள் கோடுகள் மற்றும் "
                "வளர்ச்சி குன்றிய, புல்வெளி தோற்றமுள்ள தூர்களை உண்டாக்கும்."
            ),
            "treatment": [
                "மெட்டாலாக்சில் + மாங்கோசெப் (ரிடோமில் கோல்ட்) @ 2.5 கி/லி தெளிக்கவும்.",
                "போசெட்டில்-அல் 80 WP @ 3 கி/லி அமைப்பு பூஞ்சை மருந்தாக பயன்படுத்தவும்.",
                "வயலை உடனடியாக வடிகட்டவும்.",
            ],
            "prevention": [
                "நீர் தேங்காமல் பார்த்துக்கொள்ளவும்.",
                "சான்றளிக்கப்பட்ட விதை மட்டும் பயன்படுத்தவும்.",
                "பாதிக்கப்பட்ட தூர்களை அகற்றி எரிக்கவும்.",
            ],
            "fertilizer": "பாஸ்பரஸ் உரம் (SSP @ 250 கி/ஹெக்.) இட்டு வேர் ஆரோக்கியம் மேம்படுத்தவும்.",
            "irrigation": "அறிகுறி தெரிந்தவுடன் வயலை வடிகட்டவும்; நீர் தேங்குவதை முற்றிலும் தவிர்க்கவும்.",
        },
    },

    # ── 10. NORMAL / HEALTHY ──────────────────────────────────
    "normal": {
        "english": {
            "description": "Your crop shows no visible disease symptoms and is in good health.",
            "treatment": ["No treatment required at this time."],
            "prevention": [
                "Continue balanced fertilization schedule.",
                "Monitor weekly for early signs of disease.",
                "Maintain irrigation consistency.",
            ],
            "fertilizer": "Maintain regular NPK schedule as per crop stage.",
            "irrigation": "Continue AWD (Alternate Wetting and Drying) method.",
        },
        "tamil": {
            "description": "உங்கள் பயிர் ஆரோக்கியமாக உள்ளது. எந்த நோய் அறிகுறியும் இல்லை.",
            "treatment": ["இப்போது சிகிச்சை தேவையில்லை."],
            "prevention": [
                "சம விகித உரம் தொடர்ந்து இடவும்.",
                "வாராந்திர கண்காணிப்பு செய்யவும்.",
            ],
            "fertilizer": "பயிர் வளர்ச்சி நிலைக்கு ஏற்ப NPK உரம் இடவும்.",
            "irrigation": "மாற்று நனைப்பு முறையை தொடர்ந்து பின்பற்றவும்.",
        },
    },
    "healthy": {
        "english": {
            "description": "Your crop shows no visible disease symptoms and is in good health.",
            "treatment": ["No treatment required at this time."],
            "prevention": [
                "Continue balanced fertilization schedule.",
                "Monitor weekly for early signs of disease.",
                "Maintain irrigation consistency.",
            ],
            "fertilizer": "Maintain regular NPK schedule as per crop stage.",
            "irrigation": "Continue AWD (Alternate Wetting and Drying) method.",
        },
        "tamil": {
            "description": "உங்கள் பயிர் ஆரோக்கியமாக உள்ளது. எந்த நோய் அறிகுறியும் இல்லை.",
            "treatment": ["இப்போது சிகிச்சை தேவையில்லை."],
            "prevention": [
                "சம விகித உரம் தொடர்ந்து இடவும்.",
                "வாராந்திர கண்காணிப்பு செய்யவும்.",
            ],
            "fertilizer": "பயிர் வளர்ச்சி நிலைக்கு ஏற்ப NPK உரம் இடவும்.",
            "irrigation": "மாற்று நனைப்பு முறையை தொடர்ந்து பின்பற்றவும்.",
        },
    },
}

# ─── ALIASES: model uses underscore names ─────────────────────
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


def get_advisory(disease: str, lang: str = "english") -> dict:
    key = disease.lower().strip()
    # resolve alias first
    key = _ALIASES.get(key, key)
    advice_block = _ADVICE.get(key)

    if advice_block is None:
        for k in _ADVICE:
            if k in key or key in k:
                advice_block = _ADVICE[k]
                break

    if advice_block is None:
        return {
            "description": f"No specific advisory found for '{disease}'.",
            "treatment":   ["Consult your local agriculture extension officer."],
            "prevention":  ["Maintain general crop hygiene."],
            "fertilizer":  "Use balanced NPK as per soil test recommendation.",
            "irrigation":  "Maintain optimal moisture for crop stage.",
        }

    return advice_block.get(lang, advice_block["english"])


def get_advisory_both_langs(disease: str) -> dict:
    return {
        "english": get_advisory(disease, "english"),
        "tamil":   get_advisory(disease, "tamil"),
    }