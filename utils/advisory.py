"""
utils/advisory.py — Smart Paddy AI: Agricultural Advisory Engine

LOCAL, OFFLINE ONLY: hand-written source copy exists for English + Tamil
(_ADVICE below — unchanged from the original). For the other 9 supported
languages (Telugu, Kannada, Malayalam, Hindi, Bengali, Marathi, Gujarati,
Punjabi, Odia), get_advisory() falls back to the English copy — there is
NO runtime translation API call here (Gemini is used only by the chatbot,
see utils/ai_expert.py). This matches utils/i18n.py's fallback rule:
missing translations show English, never crash, never hit an API.
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


_HAND_WRITTEN_LANGS = {"english", "tamil", "telugu", "kannada", "malayalam", "hindi", "bengali", "marathi", "gujarati", "punjabi", "odia"}

# Local advisory templates preserve scientific/product names and localize the
# complete surrounding content. Disease keys and prediction mappings remain
# unchanged.
_ADVISORY_TEXT = {
"english": ("{d} is a rice-crop condition that can reduce leaf and panicle health. Inspect affected tissue and confirm the diagnosis in the field.", ["Use the recommended product according to its label and crop stage.", "Remove severely affected material and monitor nearby plants.", "Repeat treatment only at the interval stated on the product label."], ["Use healthy seed and suitable resistant varieties.", "Avoid excess nitrogen and maintain field hygiene.", "Improve spacing, drainage, and regular scouting."], "Maintain balanced NPK and adjust nitrogen according to a soil test.", "Maintain suitable moisture; avoid prolonged waterlogging and follow AWD where appropriate."),
"tamil": ("{d} என்பது நெல் பயிரின் இலை மற்றும் கதிர் ஆரோக்கியத்தை குறைக்கக்கூடிய நிலையாகும். பாதிக்கப்பட்ட பகுதியை ஆய்வு செய்து வயலில் உறுதி செய்யவும்.", ["பயிர் நிலைக்கு ஏற்ப லேபிளில் கூறிய மருந்தை பயன்படுத்தவும்.", "கடுமையாக பாதிக்கப்பட்ட பகுதிகளை அகற்றி அருகிலுள்ள செடிகளை கண்காணிக்கவும்.", "லேபிளில் கூறிய இடைவெளியில் மட்டும் சிகிச்சையை மீண்டும் செய்யவும்."], ["ஆரோக்கியமான விதைகள் மற்றும் எதிர்ப்பு திறன் கொண்ட ரகங்களை பயன்படுத்தவும்.", "அதிக நைட்ரஜனை தவிர்த்து வயல் சுத்தத்தை பராமரிக்கவும்.", "சரியான இடைவெளி, வடிகால் மற்றும் வழக்கமான கண்காணிப்பை உறுதி செய்யவும்."], "மண் பரிசோதனைக்கு ஏற்ப சமநிலை NPK உரம் பயன்படுத்தவும்.", "பொருத்தமான ஈரப்பதத்தை பராமரிக்கவும்; நீர் தேக்கத்தை தவிர்த்து AWD முறையை பின்பற்றவும்."),
"telugu": ("{d} వరి పంట ఆకులు మరియు కంకుల ఆరోగ్యాన్ని తగ్గించగల పరిస్థితి. ప్రభావిత భాగాన్ని పరిశీలించి పొలంలో నిర్ధారించండి.", ["పంట దశకు అనుగుణంగా లేబుల్‌లో సూచించిన మందును ఉపయోగించండి.", "తీవ్రంగా ప్రభావిత భాగాలను తొలగించి సమీప మొక్కలను గమనించండి.", "లేబుల్‌లో సూచించిన వ్యవధిలో మాత్రమే చికిత్సను పునరావృతం చేయండి."], ["ఆరోగ్యకరమైన విత్తనాలు మరియు నిరోధక రకాలను ఉపయోగించండి.", "అధిక నత్రజనిని నివారించి పొల పరిశుభ్రతను పాటించండి.", "సరైన దూరం, నీటి పారుదల మరియు క్రమమైన పరిశీలన ఉండాలి."], "మట్టి పరీక్ష ఆధారంగా సమతుల్య NPK ఎరువును వాడండి.", "తగిన తేమను ఉంచండి; నీరు నిల్వ ఉండకుండా AWD పద్ధతిని అనుసరించండి."),
"kannada": ("{d} ಭತ್ತದ ಎಲೆಗಳು ಮತ್ತು ತೆನೆಗಳ ಆರೋಗ್ಯವನ್ನು ಕಡಿಮೆ ಮಾಡಬಹುದಾದ ಸ್ಥಿತಿ. ബാധಿತ ಭಾಗವನ್ನು ಪರಿಶೀಲಿಸಿ ಹೊಲದಲ್ಲಿ ದೃಢಪಡಿಸಿ.", ["ಬೆಳೆ ಹಂತಕ್ಕೆ ಅನುಗುಣವಾಗಿ ಲೇಬಲ್ ಸೂಚಿಸಿದ ಔಷಧಿಯನ್ನು ಬಳಸಿ.", "ತೀವ್ರವಾಗಿ ബാധಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದು ಸಮೀಪದ ಸಸ್ಯಗಳನ್ನು ಗಮನಿಸಿ.", "ಲೇಬಲ್ ಸೂಚಿಸಿದ ಅವಧಿಯಲ್ಲಿ ಮಾತ್ರ ಚಿಕಿತ್ಸೆಯನ್ನು ಪುನರಾವರ್ತಿಸಿ."], ["ಆರೋಗ್ಯಕರ ಬೀಜ ಮತ್ತು ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ.", "ಹೆಚ್ಚುವರಿ ನೈಟ್ರೋಜನ್ ತಪ್ಪಿಸಿ ಹೊಲದ ಸ್ವಚ್ಛತೆ ಕಾಯ್ದುಕೊಳ್ಳಿ.", "ಸರಿಯಾದ ಅಂತರ, ನೀರು ಹರಿವು ಮತ್ತು ನಿಯಮಿತ ಪರಿಶೀಲನೆ ಖಚಿತಪಡಿಸಿ."], "ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯಂತೆ ಸಮತೋಲನದ NPK ಗೊಬ್ಬರ ಬಳಸಿ.", "ಸೂಕ್ತ ತೇವಾಂಶ ಕಾಯ್ದುಕೊಳ್ಳಿ; ನೀರು ನಿಲ್ಲದಂತೆ AWD ವಿಧಾನ ಅನುಸರಿಸಿ."),
"malayalam": ("{d} നെല്ലിന്റെ ഇലകളുടെയും കതിരുകളുടെയും ആരോഗ്യം കുറയ്ക്കാൻ കഴിയുന്ന അവസ്ഥയാണ്. ബാധിച്ച ഭാഗം പരിശോധിച്ച് വയലിൽ സ്ഥിരീകരിക്കുക.", ["വിളയുടെ ഘട്ടത്തിന് അനുസരിച്ച് ലേബലിൽ നിർദ്ദേശിച്ച മരുന്ന് ഉപയോഗിക്കുക.", "ഗുരുതരമായി ബാധിച്ച ഭാഗങ്ങൾ നീക്കി സമീപ ചെടികൾ നിരീക്ഷിക്കുക.", "ലേബലിൽ പറഞ്ഞ ഇടവേളയിൽ മാത്രം ചികിത്സ ആവർത്തിക്കുക."], ["ആരോഗ്യമുള്ള വിത്തുകളും പ്രതിരോധ ശേഷിയുള്ള ഇനങ്ങളും ഉപയോഗിക്കുക.", "അധിക നൈട്രജൻ ഒഴിവാക്കി വയൽ ശുചിത്വം പാലിക്കുക.", "ശരിയായ അകലം, നീർവാർച്ച, സ്ഥിരമായ നിരീക്ഷണം എന്നിവ ഉറപ്പാക്കുക."], "മണ്ണ് പരിശോധന അനുസരിച്ച് സമീകൃത NPK വളം നൽകുക.", "അനുയോജ്യമായ ഈർപ്പം നിലനിർത്തുക; വെള്ളക്കെട്ട് ഒഴിവാക്കി AWD പിന്തുടരുക."),
"hindi": ("{d} धान की पत्तियों और बालियों के स्वास्थ्य को कम करने वाली स्थिति है। प्रभावित भाग की जांच करके खेत में पुष्टि करें।", ["फसल की अवस्था के अनुसार लेबल पर बताए गए उत्पाद का उपयोग करें।", "बहुत प्रभावित भाग हटाकर आसपास के पौधों की निगरानी करें।", "उत्पाद के लेबल पर दिए अंतराल पर ही उपचार दोहराएं।"], ["स्वस्थ बीज और रोग-प्रतिरोधी किस्मों का उपयोग करें।", "अधिक नाइट्रोजन से बचें और खेत की स्वच्छता रखें।", "उचित दूरी, जल निकास और नियमित निरीक्षण सुनिश्चित करें।"], "मृदा जांच के अनुसार संतुलित NPK उर्वरक दें।", "उचित नमी बनाए रखें; जलभराव से बचें और जहां उपयुक्त हो AWD अपनाएं।"),
"bengali": ("{d} ধানের পাতা ও শীষের স্বাস্থ্য কমাতে পারে এমন একটি অবস্থা। আক্রান্ত অংশ পরীক্ষা করে মাঠে নিশ্চিত করুন।", ["ফসলের পর্যায় অনুযায়ী লেবেলে উল্লেখিত পণ্য ব্যবহার করুন।", "অতিরিক্ত আক্রান্ত অংশ সরিয়ে আশেপাশের গাছ পর্যবেক্ষণ করুন।", "লেবেলে দেওয়া বিরতিতে তবেই চিকিৎসা পুনরাবৃত্তি করুন।"], ["সুস্থ বীজ ও প্রতিরোধী জাত ব্যবহার করুন।", "অতিরিক্ত নাইট্রোজেন এড়িয়ে মাঠ পরিষ্কার রাখুন।", "সঠিক দূরত্ব, নিষ্কাশন ও নিয়মিত পর্যবেক্ষণ নিশ্চিত করুন।"], "মাটি পরীক্ষার ভিত্তিতে সুষম NPK সার ব্যবহার করুন।", "উপযুক্ত আর্দ্রতা বজায় রাখুন; জলাবদ্ধতা এড়িয়ে AWD অনুসরণ করুন।"),
"marathi": ("{d} ही भाताच्या पानांचे आणि कणसांचे आरोग्य कमी करणारी स्थिती आहे. बाधित भाग तपासून शेतात खात्री करा.", ["पिकाच्या अवस्थेनुसार लेबलवर दिलेले उत्पादन वापरा.", "जास्त बाधित भाग काढून जवळच्या झाडांचे निरीक्षण करा.", "लेबलवर दिलेल्या अंतरानेच उपचार पुन्हा करा."], ["निरोगी बियाणे आणि प्रतिरोधक वाण वापरा.", "अति नत्र टाळा आणि शेताची स्वच्छता राखा.", "योग्य अंतर, निचरा आणि नियमित पाहणी सुनिश्चित करा."], "माती परीक्षणानुसार संतुलित NPK खत द्या.", "योग्य ओलावा राखा; पाणी साचू देऊ नका आणि योग्य ठिकाणी AWD वापरा."),
"gujarati": ("{d} ધાનના પાન અને ડૂંડાના આરોગ્યને ઘટાડી શકે તેવી સ્થિતિ છે. અસરગ્રસ્ત ભાગ તપાસીને ખેતરમાં ખાતરી કરો.", ["પાકની અવસ્થા મુજબ લેબલમાં જણાવેલ ઉત્પાદન વાપરો.", "ખૂબ અસરગ્રસ્ત ભાગ દૂર કરીને નજીકના છોડનું નિરીક્ષણ કરો.", "લેબલમાં આપેલા અંતરે જ સારવાર ફરી કરો."], ["સ્વસ્થ બીજ અને રોગપ્રતિરોધક જાતો વાપરો.", "વધુ નાઇટ્રોજન ટાળો અને ખેતરની સ્વચ્છતા જાળવો.", "યોગ્ય અંતર, નિકાસ અને નિયમિત દેખરેખ સુનિશ્ચિત કરો."], "માટી પરીક્ષણ મુજબ સંતુલિત NPK ખાતર આપો.", "યોગ્ય ભેજ જાળવો; પાણી ભરાવું ટાળો અને યોગ્ય હોય ત્યાં AWD અપનાવો."),
"punjabi": ("{d} ਝੋਨੇ ਦੇ ਪੱਤਿਆਂ ਅਤੇ ਬਾਲੀਆਂ ਦੀ ਸਿਹਤ ਘਟਾ ਸਕਦੀ ਹੈ। ਪ੍ਰਭਾਵਿਤ ਹਿੱਸੇ ਦੀ ਜਾਂਚ ਕਰਕੇ ਖੇਤ ਵਿੱਚ ਪੁਸ਼ਟੀ ਕਰੋ।", ["ਫਸਲ ਦੀ ਅਵਸਥਾ ਅਨੁਸਾਰ ਲੇਬਲ ਉੱਤੇ ਦਿੱਤਾ ਉਤਪਾਦ ਵਰਤੋ।", "ਬਹੁਤ ਪ੍ਰਭਾਵਿਤ ਹਿੱਸੇ ਹਟਾ ਕੇ ਨੇੜਲੇ ਪੌਦਿਆਂ ਦੀ ਨਿਗਰਾਨੀ ਕਰੋ।", "ਲੇਬਲ ਵਿੱਚ ਦਿੱਤੇ ਅੰਤਰਾਲ ਉੱਤੇ ਹੀ ਇਲਾਜ ਦੁਹਰਾਓ।"], ["ਸਿਹਤਮੰਦ ਬੀਜ ਅਤੇ ਰੋਗ-ਰੋਧੀ ਕਿਸਮਾਂ ਵਰਤੋ।", "ਵਾਧੂ ਨਾਈਟ੍ਰੋਜਨ ਤੋਂ ਬਚੋ ਅਤੇ ਖੇਤ ਦੀ ਸਫਾਈ ਰੱਖੋ।", "ਸਹੀ ਦੂਰੀ, ਨਿਕਾਸ ਅਤੇ ਨਿਯਮਤ ਜਾਂਚ ਯਕੀਨੀ ਬਣਾਓ।"], "ਮਿੱਟੀ ਜਾਂਚ ਅਨੁਸਾਰ ਸੰਤੁਲਿਤ NPK ਖਾਦ ਦਿਓ।", "ਉਚਿਤ ਨਮੀ ਰੱਖੋ; ਪਾਣੀ ਖੜ੍ਹਾ ਨਾ ਹੋਣ ਦਿਓ ਅਤੇ ਜਿੱਥੇ ਢੁਕਵਾਂ ਹੋਵੇ AWD ਅਪਣਾਓ।"),
"odia": ("{d} ଧାନର ପତ୍ର ଏବଂ ଶୀଷର ସ୍ୱାସ୍ଥ୍ୟ କମାଇପାରେ। ପ୍ରଭାବିତ ଅଂଶ ଯାଞ୍ଚ କରି କ୍ଷେତରେ ନିଶ୍ଚିତ କରନ୍ତୁ।", ["ଫସଲ ଅବସ୍ଥା ଅନୁସାରେ ଲେବେଲରେ ଦିଆଯାଇଥିବା ଉତ୍ପାଦ ବ୍ୟବହାର କରନ୍ତୁ।", "ଅଧିକ ପ୍ରଭାବିତ ଅଂଶ କାଢ଼ି ନିକଟସ୍ଥ ଗଛଗୁଡ଼ିକୁ ନିରୀକ୍ଷଣ କରନ୍ତୁ।", "ଲେବେଲରେ ଦିଆଯାଇଥିବା ବ୍ୟବଧାନରେ ମାତ୍ର ଚିକିତ୍ସା ପୁନରାବୃତ୍ତି କରନ୍ତୁ।"], ["ସୁସ୍ଥ ବୀଜ ଏବଂ ପ୍ରତିରୋଧୀ କିସମ ବ୍ୟବହାର କରନ୍ତୁ।", "ଅଧିକ ନାଇଟ୍ରୋଜେନ ଏଡ଼ାଇ କ୍ଷେତର ପରିଷ୍କାରତା ରଖନ୍ତୁ।", "ଉପଯୁକ୍ତ ଦୂରତା, ଜଳ ନିଷ୍କାସନ ଏବଂ ନିୟମିତ ନିରୀକ୍ଷଣ ନିଶ୍ଚିତ କରନ୍ତୁ।"], "ମାଟି ପରୀକ୍ଷା ଅନୁସାରେ ସନ୍ତୁଳିତ NPK ସାର ଦିଅନ୍ତୁ।", "ଉପଯୁକ୍ତ ଆର୍ଦ୍ରତା ରଖନ୍ତୁ; ଜଳ ଜମିବା ଏଡ଼ାଇ ଉପଯୁକ୍ତ ସ୍ଥାନରେ AWD ଅନୁସରଣ କରନ୍ତୁ।"),
}

def get_advisory(disease: str, lang: str = "english") -> dict:
    """Return disease-specific advisory content without any runtime API call."""
    from utils.i18n import resolve_lang, disease_display_name

    lang = resolve_lang(lang)
    key = _ALIASES.get(disease.lower().strip(), disease.lower().strip())
    disease_record = _ADVICE.get(key)
    if disease_record is None:
        disease_record = _ADVICE.get("healthy", _ADVICE["normal"])

    # The hand-written disease-specific English/Tamil records are the source
    # of truth and preserve exact chemical/product names.
    if lang in disease_record:
        return {field: (value.copy() if isinstance(value, list) else value)
                for field, value in disease_record[lang].items()}

    # For the other supported languages, use the localized explanatory
    # templates but keep the disease-specific product recommendation from the
    # English record technically unchanged. This avoids one static treatment
    # being shown for every disease and never translates chemical names.
    d = disease_display_name(key, lang)
    desc, treatment, prevention, fertilizer, irrigation = _ADVISORY_TEXT[lang]
    localized = {
        "description": desc.format(d=d),
        "treatment": treatment.copy(),
        "prevention": prevention.copy(),
        "fertilizer": fertilizer,
        "irrigation": irrigation,
    }
    english_treatment = disease_record.get("english", {}).get("treatment", [])
    if english_treatment:
        localized["treatment"][0] = english_treatment[0]
    return localized

def get_advisory_both_langs(disease: str) -> dict:
    return {"english": get_advisory(disease, "english"), "tamil": get_advisory(disease, "tamil")}

def get_advisory_all_langs(disease: str) -> dict:
    from utils.i18n import LANGUAGE_ORDER
    return {lang: get_advisory(disease, lang) for lang in LANGUAGE_ORDER}

