"""
utils/pdf_report.py — Smart Paddy AI: PDF Report Generator
Place at: smart_paddy_ai/utils/pdf_report.py

Generates a downloadable diagnostic report containing:
  - Header with logo/title
  - Uploaded image + Grad-CAM image side-by-side
  - Disease prediction + confidence
  - Per-class probability breakdown
  - Severity analysis
  - Crop Health Index
  - Full treatment/prevention/fertilizer recommendations
  - Date & time stamp
"""

import io
import datetime
from PIL import Image

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage,
)


# ─────────────────────── COLOUR PALETTE ───────────────────────
GREEN  = colors.HexColor("#2d7a2d")
LIME   = colors.HexColor("#e8f5e9")
AMBER  = colors.HexColor("#fff3e0")
RED    = colors.HexColor("#ffebee")
DARK   = colors.HexColor("#1a1a2e")
GREY   = colors.HexColor("#f5f5f5")
WHITE  = colors.white


# ─────────────────────── PIL → ReportLab Image ────────────────
def _pil_to_rl_image(pil_img: Image.Image, width_cm: float, height_cm: float) -> RLImage:
    """Convert a PIL image to a ReportLab Image flowable."""
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)
    return RLImage(buf, width=width_cm * cm, height=height_cm * cm)


# ─────────────────────── STYLES ───────────────────────────────
def _build_styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=base["Title"],
        fontSize=20,
        textColor=GREEN,
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )
    subtitle_style = ParagraphStyle(
        "SubTitle",
        parent=base["Normal"],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=base["Heading2"],
        fontSize=12,
        textColor=GREEN,
        spaceBefore=10,
        spaceAfter=4,
        fontName="Helvetica-Bold",
    )
    body_style = ParagraphStyle(
        "BodyText",
        parent=base["Normal"],
        fontSize=9,
        leading=14,
        textColor=DARK,
    )
    bullet_style = ParagraphStyle(
        "BulletItem",
        parent=base["Normal"],
        fontSize=9,
        leading=14,
        leftIndent=12,
        bulletIndent=4,
        textColor=DARK,
    )
    label_style = ParagraphStyle(
        "Label",
        parent=base["Normal"],
        fontSize=8,
        textColor=colors.grey,
    )

    return {
        "title":    title_style,
        "subtitle": subtitle_style,
        "heading":  heading_style,
        "body":     body_style,
        "bullet":   bullet_style,
        "label":    label_style,
    }


# ─────────────────────── LOCALIZED LABELS ─────────────────────
# Static PDF headings/labels, hand-written for all 11 languages — local
# dictionary only, no runtime translation API calls. Chemical/product/
# model names (e.g. "EfficientNetB0 Transfer Learning" in footer_line2)
# are intentionally left untranslated.
_PDF_LABELS = {
    "report_subtitle": {
        "english": "Rice Disease Detection & Agricultural Decision Support Report",
        "tamil": "நெல் நோய் கண்டறிதல் மற்றும் விவசாய முடிவு ஆதரவு அறிக்கை",
        "telugu": "వరి వ్యాధి గుర్తింపు మరియు వ్యవసాయ నిర్ణయ మద్దతు నివేదిక",
        "kannada": "ಭತ್ತದ ರೋಗ ಪತ್ತೆ ಮತ್ತು ಕೃಷಿ ನಿರ್ಧಾರ ಬೆಂಬಲ ವರದಿ",
        "malayalam": "നെല്ല് രോഗനിർണയവും കാർഷിക തീരുമാന പിന്തുണാ റിപ്പോർട്ടും",
        "hindi": "धान रोग पहचान एवं कृषि निर्णय सहायता रिपोर्ट",
        "bengali": "ধান রোগ সনাক্তকরণ ও কৃষি সিদ্ধান্ত সহায়তা প্রতিবেদন",
        "marathi": "भात रोग ओळख आणि कृषी निर्णय सहाय्य अहवाल",
        "gujarati": "ડાંગર રોગ ઓળખ અને કૃષિ નિર્ણય સહાય અહેવાલ",
        "punjabi": "ਝੋਨਾ ਰੋਗ ਪਛਾਣ ਅਤੇ ਖੇਤੀ ਫੈਸਲਾ ਸਹਾਇਤਾ ਰਿਪੋਰਟ",
        "odia": "ଧାନ ରୋଗ ଚିହ୍ନଟ ଏବଂ କୃଷି ନିଷ୍ପତ୍ତି ସହାୟତା ରିପୋର୍ଟ",
    },
    "report_date": {
        "english": "Report Date:", "tamil": "அறிக்கை தேதி:", "telugu": "నివేదిక తేదీ:",
        "kannada": "ವರದಿ ದಿನಾಂಕ:", "malayalam": "റിപ്പോർട്ട് തീയതി:", "hindi": "रिपोर्ट तिथि:",
        "bengali": "প্রতিবেদনের তারিখ:", "marathi": "अहवाल तारीख:", "gujarati": "અહેવાલ તારીખ:",
        "punjabi": "ਰਿਪੋਰਟ ਮਿਤੀ:", "odia": "ରିପୋର୍ଟ ତାରିଖ:",
    },
    "farmer": {
        "english": "Farmer:", "tamil": "விவசாயி:", "telugu": "రైతు:", "kannada": "ರೈತ:",
        "malayalam": "കർഷകൻ:", "hindi": "किसान:", "bengali": "কৃষক:", "marathi": "शेतकरी:",
        "gujarati": "ખેડૂત:", "punjabi": "ਕਿਸਾਨ:", "odia": "କୃଷକ:",
    },
    "location": {
        "english": "Location:", "tamil": "இடம்:", "telugu": "ప్రదేశం:", "kannada": "ಸ್ಥಳ:",
        "malayalam": "സ്ഥലം:", "hindi": "स्थान:", "bengali": "অবস্থান:", "marathi": "स्थान:",
        "gujarati": "સ્થળ:", "punjabi": "ਸਥਾਨ:", "odia": "ସ୍ଥାନ:",
    },
    "model": {
        "english": "Model:", "tamil": "மாதிரி:", "telugu": "మోడల్:", "kannada": "ಮಾದರಿ:",
        "malayalam": "മോഡൽ:", "hindi": "मॉडल:", "bengali": "মডেল:", "marathi": "मॉडेल:",
        "gujarati": "મોડેલ:", "punjabi": "ਮਾਡਲ:", "odia": "ମଡେଲ:",
    },
    "leaf_image_analysis": {
        "english": "Leaf Image Analysis", "tamil": "இலை படப் பகுப்பாய்வு", "telugu": "ఆకు చిత్ర విశ్లేషణ",
        "kannada": "ಎಲೆ ಚಿತ್ರ ವಿಶ್ಲೇಷಣೆ", "malayalam": "ഇല ചിത്ര വിശകലനം", "hindi": "पत्ती छवि विश्लेषण",
        "bengali": "পাতার ছবি বিশ্লেষণ", "marathi": "पान प्रतिमा विश्लेषण", "gujarati": "પર્ણ છબી વિશ્લેષણ",
        "punjabi": "ਪੱਤਾ ਚਿੱਤਰ ਵਿਸ਼ਲੇਸ਼ਣ", "odia": "ପତ୍ର ପ୍ରତିଛବି ବିଶ୍ଳେଷଣ",
    },
    "original_image": {
        "english": "Original Image", "tamil": "மூல படம்", "telugu": "అసలు చిత్రం", "kannada": "ಮೂಲ ಚಿತ್ರ",
        "malayalam": "ഒറിജിനൽ ചിത്രം", "hindi": "मूल छवि", "bengali": "মূল ছবি", "marathi": "मूळ प्रतिमा",
        "gujarati": "મૂળ છબી", "punjabi": "ਮੂਲ ਚਿੱਤਰ", "odia": "ମୂଳ ପ୍ରତିଛବି",
    },
    "gradcam_heatmap": {
        "english": "Grad-CAM Heatmap (Infected Regions)",
        "tamil": "Grad-CAM வெப்பப்படம் (பாதிக்கப்பட்ட பகுதிகள்)",
        "telugu": "Grad-CAM హీట్‌మ్యాప్ (వ్యాధిగ్రస్త ప్రాంతాలు)",
        "kannada": "Grad-CAM ಹೀಟ್‌ಮ್ಯಾಪ್ (ಸೋಂಕಿತ ಪ್ರದೇಶಗಳು)",
        "malayalam": "Grad-CAM ഹീറ്റ്മാപ്പ് (ബാധിത പ്രദേശങ്ങൾ)",
        "hindi": "Grad-CAM हीटमैप (संक्रमित क्षेत्र)",
        "bengali": "Grad-CAM হিটম্যাপ (আক্রান্ত অঞ্চল)",
        "marathi": "Grad-CAM हीटमॅप (संक्रमित भाग)",
        "gujarati": "Grad-CAM હીટમેપ (ચેપગ્રસ્ત વિસ્તારો)",
        "punjabi": "Grad-CAM ਹੀਟਮੈਪ (ਸੰਕਰਮਿਤ ਖੇਤਰ)",
        "odia": "Grad-CAM ହିଟମ୍ୟାପ (ସଂକ୍ରମିତ ଅଞ୍ଚଳ)",
    },
    "prediction_results": {
        "english": "Prediction Results", "tamil": "கணிப்பு முடிவுகள்", "telugu": "అంచనా ఫలితాలు",
        "kannada": "ಮುನ್ಸೂಚನೆ ಫಲಿತಾಂಶಗಳು", "malayalam": "പ്രവചന ഫലങ്ങൾ", "hindi": "पूर्वानुमान परिणाम",
        "bengali": "পূর্বাভাস ফলাফল", "marathi": "अंदाज निकाल", "gujarati": "આગાહી પરિણામો",
        "punjabi": "ਭਵਿੱਖਬਾਣੀ ਨਤੀਜੇ", "odia": "ପୂର୍ବାନୁମାନ ଫଳାଫଳ",
    },
    "detected_disease": {
        "english": "Detected Disease", "tamil": "கண்டறியப்பட்ட நோய்", "telugu": "గుర్తించిన వ్యాధి",
        "kannada": "ಪತ್ತೆಯಾದ ರೋಗ", "malayalam": "കണ്ടെത്തിയ രോഗം", "hindi": "पहचाना गया रोग",
        "bengali": "শনাক্তকৃত রোগ", "marathi": "आढळलेला रोग", "gujarati": "શોધાયેલ રોગ",
        "punjabi": "ਪਛਾਣਿਆ ਗਿਆ ਰੋਗ", "odia": "ଚିହ୍ନଟ ହୋଇଥିବା ରୋଗ",
    },
    "confidence": {
        "english": "Confidence", "tamil": "நம்பகத்தன்மை", "telugu": "విశ్వసనీయత", "kannada": "ವಿಶ್ವಾಸಾರ್ಹತೆ",
        "malayalam": "വിശ്വാസ്യത", "hindi": "विश्वास स्तर", "bengali": "নির্ভরযোগ্যতা", "marathi": "विश्वासार्हता",
        "gujarati": "વિશ્વસનીયતા", "punjabi": "ਭਰੋਸੇਯੋਗਤਾ", "odia": "ବିଶ୍ୱସନୀୟତା",
    },
    "severity": {
        "english": "Severity", "tamil": "தீவிரம்", "telugu": "తీవ్రత", "kannada": "ತೀವ್ರತೆ",
        "malayalam": "തീവ്രത", "hindi": "गंभीरता", "bengali": "তীব্রতা", "marathi": "तीव्रता",
        "gujarati": "તીવ્રતા", "punjabi": "ਗੰਭੀਰਤਾ", "odia": "ତୀବ୍ରତା",
    },
    "crop_health_index": {
        "english": "Crop Health Index", "tamil": "பயிர் ஆரோக்கிய குறியீடு", "telugu": "పంట ఆరోగ్య సూచిక",
        "kannada": "ಬೆಳೆ ಆರೋಗ್ಯ ಸೂಚ್ಯಂಕ", "malayalam": "വിള ആരോഗ്യ സൂചിക", "hindi": "फसल स्वास्थ्य सूचकांक",
        "bengali": "ফসল স্বাস্থ্য সূচক", "marathi": "पीक आरोग्य निर्देशांक", "gujarati": "પાક આરોગ્ય સૂચકાંક",
        "punjabi": "ਫਸਲ ਸਿਹਤ ਸੂਚਕ ਅੰਕ", "odia": "ଫସଲ ସ୍ୱାସ୍ଥ୍ୟ ସୂଚକାଙ୍କ",
    },
    "class_probability_breakdown": {
        "english": "Class Probability Breakdown", "tamil": "வகைவாரி நிகழ்தகவு பகுப்பாய்வு",
        "telugu": "తరగతి సంభావ్యత విభజన", "kannada": "ವರ್ಗ ಸಂಭವನೀಯತೆ ವಿಭಜನೆ",
        "malayalam": "ക്ലാസ് സാധ്യതാ വിഭജനം", "hindi": "श्रेणी संभावना विवरण",
        "bengali": "শ্রেণী সম্ভাবনা বিভাজন", "marathi": "वर्ग संभाव्यता विभाजन",
        "gujarati": "વર્ગ સંભાવના વિભાજન", "punjabi": "ਸ਼੍ਰੇਣੀ ਸੰਭਾਵਨਾ ਵੰਡ", "odia": "ଶ୍ରେଣୀ ସମ୍ଭାବନା ବିଭାଜନ",
    },
    "class": {
        "english": "Class", "tamil": "வகை", "telugu": "తరగతి", "kannada": "ವರ್ಗ", "malayalam": "ക്ലാസ്",
        "hindi": "श्रेणी", "bengali": "শ্রেণী", "marathi": "वर्ग", "gujarati": "વર્ગ", "punjabi": "ਸ਼੍ਰੇਣੀ", "odia": "ଶ୍ରେଣୀ",
    },
    "probability": {
        "english": "Probability", "tamil": "நிகழ்தகவு", "telugu": "సంభావ్యత", "kannada": "ಸಂಭವನೀಯತೆ",
        "malayalam": "സാധ്യത", "hindi": "संभावना", "bengali": "সম্ভাবনা", "marathi": "संभाव्यता",
        "gujarati": "સંભાવના", "punjabi": "ਸੰਭਾਵਨਾ", "odia": "ସମ୍ଭାବନା",
    },
    "visual": {
        "english": "Visual", "tamil": "காட்சிப்படுத்தல்", "telugu": "దృశ్యం", "kannada": "ದೃಶ್ಯ",
        "malayalam": "ദൃശ്യം", "hindi": "दृश्य", "bengali": "ভিজ্যুয়াল", "marathi": "दृश्य",
        "gujarati": "વિઝ્યુઅલ", "punjabi": "ਵਿਜ਼ੂਅਲ", "odia": "ଭିଜୁଆଲ",
    },
    "agricultural_advisory": {
        "english": "Agricultural Advisory", "tamil": "விவசாய ஆலோசனை", "telugu": "వ్యవసాయ సలహా",
        "kannada": "ಕೃಷಿ ಸಲಹೆ", "malayalam": "കാർഷിക ഉപദേശം", "hindi": "कृषि सलाह",
        "bengali": "কৃষি পরামর্শ", "marathi": "कृषी सल्ला", "gujarati": "કૃષિ સલાહ",
        "punjabi": "ਖੇਤੀ ਸਲਾਹ", "odia": "କୃଷି ପରାମର୍ଶ",
    },
    "treatment": {
        "english": "Treatment:", "tamil": "சிகிச்சை:", "telugu": "చికిత్స:", "kannada": "ಚಿಕಿತ್ಸೆ:",
        "malayalam": "ചികിത്സ:", "hindi": "उपचार:", "bengali": "চিকিৎসা:", "marathi": "उपचार:",
        "gujarati": "સારવાર:", "punjabi": "ਇਲਾਜ:", "odia": "ଚିକିତ୍ସା:",
    },
    "prevention": {
        "english": "Prevention:", "tamil": "தடுப்பு:", "telugu": "నివారణ:", "kannada": "ತಡೆಗಟ್ಟುವಿಕೆ:",
        "malayalam": "പ്രതിരോധം:", "hindi": "रोकथाम:", "bengali": "প্রতিরোধ:", "marathi": "प्रतिबंध:",
        "gujarati": "નિવારણ:", "punjabi": "ਰੋਕਥਾਮ:", "odia": "ପ୍ରତିରୋଧ:",
    },
    "fertilizer_advice": {
        "english": "Fertilizer Advice", "tamil": "உர ஆலோசனை", "telugu": "ఎరువుల సలహా",
        "kannada": "ಗೊಬ್ಬರ ಸಲಹೆ", "malayalam": "വള ഉപദേശം", "hindi": "उर्वरक सलाह",
        "bengali": "সার পরামর্শ", "marathi": "खत सल्ला", "gujarati": "ખાતર સલાહ",
        "punjabi": "ਖਾਦ ਸਲਾਹ", "odia": "ସାର ପରାମର୍ଶ",
    },
    "irrigation_advice": {
        "english": "Irrigation Advice", "tamil": "நீர்ப்பாசன ஆலோசனை", "telugu": "నీటిపారుదల సలహా",
        "kannada": "ನೀರಾವರಿ ಸಲಹೆ", "malayalam": "ജലസേചന ഉപദേശം", "hindi": "सिंचाई सलाह",
        "bengali": "সেচ পরামর্শ", "marathi": "सिंचन सल्ला", "gujarati": "સિંચાઈ સલાહ",
        "punjabi": "ਸਿੰਚਾਈ ਸਲਾਹ", "odia": "ଜଳସେଚନ ପରାମର୍ଶ",
    },
    "footer_line1": {
        "english": "Generated by Smart Paddy AI — Research-Oriented Agricultural Decision Support System",
        "tamil": "ஸ்மார்ட் பேடி AI ஆல் உருவாக்கப்பட்டது — ஆராய்ச்சி சார்ந்த விவசாய முடிவு ஆதரவு அமைப்பு",
        "telugu": "స్మార్ట్ పాడీ AI ద్వారా రూపొందించబడింది — పరిశోధన ఆధారిత వ్యవసాయ నిర్ణయ మద్దతు వ్యవస్థ",
        "kannada": "ಸ್ಮಾರ್ಟ್ ಪ್ಯಾಡಿ AI ನಿಂದ ರಚಿಸಲಾಗಿದೆ — ಸಂಶೋಧನಾ ಆಧಾರಿತ ಕೃಷಿ ನಿರ್ಧಾರ ಬೆಂಬಲ ವ್ಯವಸ್ಥೆ",
        "malayalam": "സ്മാർട്ട് പാഡി AI സൃഷ്ടിച്ചത് — ഗവേഷണാധിഷ്ഠിത കാർഷിക തീരുമാന പിന്തുണാ സംവിധാനം",
        "hindi": "स्मार्ट पैडी AI द्वारा तैयार — शोध-आधारित कृषि निर्णय सहायता प्रणाली",
        "bengali": "স্মার্ট প্যাডি AI দ্বারা তৈরি — গবেষণাভিত্তিক কৃষি সিদ্ধান্ত সহায়তা ব্যবস্থা",
        "marathi": "स्मार्ट पॅडी AI द्वारे तयार — संशोधन-आधारित कृषी निर्णय सहाय्य प्रणाली",
        "gujarati": "સ્માર્ટ પેડી AI દ્વારા બનાવેલ — સંશોધન-આધારિત કૃષિ નિર્ણય સહાય પ્રણાલી",
        "punjabi": "ਸਮਾਰਟ ਪੈਡੀ AI ਦੁਆਰਾ ਤਿਆਰ — ਖੋਜ-ਆਧਾਰਿਤ ਖੇਤੀ ਫੈਸਲਾ ਸਹਾਇਤਾ ਪ੍ਰਣਾਲੀ",
        "odia": "ସ୍ମାର୍ଟ ପେଡି AI ଦ୍ୱାରା ପ୍ରସ୍ତୁତ — ଗବେଷଣା-ଆଧାରିତ କୃଷି ନିଷ୍ପତ୍ତି ସହାୟତା ପ୍ରଣାଳୀ",
    },
    "footer_line2": {
        "english": "Report generated on {ts}  |  AI Model: EfficientNetB0 Transfer Learning",
        "tamil": "அறிக்கை உருவாக்கப்பட்ட நேரம் {ts}  |  AI மாதிரி: EfficientNetB0 Transfer Learning",
        "telugu": "నివేదిక రూపొందించిన సమయం {ts}  |  AI మోడల్: EfficientNetB0 Transfer Learning",
        "kannada": "ವರದಿ ರಚಿಸಲಾದ ಸಮಯ {ts}  |  AI ಮಾದರಿ: EfficientNetB0 Transfer Learning",
        "malayalam": "റിപ്പോർട്ട് സൃഷ്ടിച്ച സമയം {ts}  |  AI മോഡൽ: EfficientNetB0 Transfer Learning",
        "hindi": "रिपोर्ट तैयार करने का समय {ts}  |  AI मॉडल: EfficientNetB0 Transfer Learning",
        "bengali": "প্রতিবেদন তৈরির সময় {ts}  |  AI মডেল: EfficientNetB0 Transfer Learning",
        "marathi": "अहवाल तयार केल्याची वेळ {ts}  |  AI मॉडेल: EfficientNetB0 Transfer Learning",
        "gujarati": "અહેવાલ બનાવ્યાનો સમય {ts}  |  AI મોડેલ: EfficientNetB0 Transfer Learning",
        "punjabi": "ਰਿਪੋਰਟ ਬਣਾਉਣ ਦਾ ਸਮਾਂ {ts}  |  AI ਮਾਡਲ: EfficientNetB0 Transfer Learning",
        "odia": "ରିପୋର୍ଟ ପ୍ରସ୍ତୁତ ସମୟ {ts}  |  AI ମଡେଲ: EfficientNetB0 Transfer Learning",
    },
}


def _labels(lang: str) -> dict:
    """Every PDF label for `lang`, local dictionary only (no API calls). Falls back to English per key if missing."""
    return {key: block.get(lang, block["english"]) for key, block in _PDF_LABELS.items()}


# ─────────────────────── MAIN GENERATOR ───────────────────────
def generate_pdf_report(
    original_image:  Image.Image,
    gradcam_image:   Image.Image | None,
    disease:         str,
    confidence:      float,
    all_probs:       dict,
    severity:        dict,
    health_index:    dict,
    advisory:        dict,
    location:        str = "",
    farmer_name:     str = "",
    lang:            str = "english",
) -> bytes:
    """
    Build and return a PDF report as raw bytes.

    Parameters
    ----------
    original_image : PIL Image — uploaded leaf photo
    gradcam_image  : PIL Image | None — Grad-CAM overlay
    disease        : str — predicted disease name (pass a display name
                     already localized via utils.i18n.disease_display_name
                     if you want the disease name itself translated too)
    confidence     : float — 0–1 model confidence
    all_probs      : dict — {class_name: pct_float}
    severity       : dict — from severity.estimate_severity()
    health_index   : dict — from severity.crop_health_index()
    advisory       : dict — from advisory.get_advisory(disease, lang) —
                     pass the ALREADY-LOCALIZED advisory dict for `lang`
                     so the PDF body text matches the PDF's own language.
    location       : str — optional farmer location
    farmer_name    : str — optional farmer name
    lang           : str — one of utils.i18n.LANGUAGE_ORDER; controls every
                     heading/label in the generated PDF.
    """
    T = _labels(lang)
    buf    = io.BytesIO()
    doc    = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = _build_styles()
    story  = []

    ts = datetime.datetime.now().strftime("%d %B %Y  %H:%M:%S")

    # ── HEADER ────────────────────────────────────────────────
    story.append(Paragraph("🌾 Smart Paddy AI", styles["title"]))
    story.append(Paragraph(
        T["report_subtitle"],
        styles["subtitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN))
    story.append(Spacer(1, 0.3 * cm))

    # Meta table
    meta_data = [
        [T["report_date"], ts,              T["farmer"], farmer_name or "—"],
        [T["location"],    location or "—", T["model"],  "EfficientNetB0"],
    ]
    meta_table = Table(meta_data, colWidths=[3 * cm, 5 * cm, 3 * cm, 5 * cm])
    meta_table.setStyle(TableStyle([
        ("FONTSIZE",    (0, 0), (-1, -1), 8),
        ("TEXTCOLOR",   (0, 0), (0, -1), colors.grey),
        ("TEXTCOLOR",   (2, 0), (2, -1), colors.grey),
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",    (2, 0), (2, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.4 * cm))

    # ── IMAGES ────────────────────────────────────────────────
    story.append(Paragraph(T["leaf_image_analysis"], styles["heading"]))

    img_row = [_pil_to_rl_image(original_image.resize((224, 224)), 7, 7)]
    labels_row = [T["original_image"]]

    if gradcam_image is not None:
        img_row.append(_pil_to_rl_image(gradcam_image.resize((224, 224)), 7, 7))
        labels_row.append(T["gradcam_heatmap"])

    img_table = Table([img_row], colWidths=[8 * cm] * len(img_row))
    img_table.setStyle(TableStyle([
        ("ALIGN",   (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",  (0, 0), (-1, -1), "MIDDLE"),
        ("BOX",     (0, 0), (0, 0), 1, colors.lightgrey),
        ("BOX",     (1, 0), (1, 0), 1, colors.lightgrey) if len(img_row) > 1 else ("", (0,0),(0,0), 0, WHITE),
    ]))
    story.append(img_table)

    lbl_table = Table(
        [[Paragraph(l, styles["label"]) for l in labels_row]],
        colWidths=[8 * cm] * len(labels_row)
    )
    lbl_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(lbl_table)
    story.append(Spacer(1, 0.4 * cm))

    # ── PREDICTION RESULTS ────────────────────────────────────
    story.append(Paragraph(T["prediction_results"], styles["heading"]))

    # Severity colour choice
    from utils.i18n import translate_enum, disease_display_name
    sev_pct   = severity.get("percentage", 0)
    sev_label = translate_enum(severity.get("label", "N/A"), lang)
    health_category = translate_enum(health_index.get("category", ""), lang)
    sev_bg    = LIME if sev_pct < 31 else (AMBER if sev_pct < 71 else RED)

    pred_data = [
        [T["detected_disease"], disease,
         T["confidence"],       f"{confidence * 100:.1f}%"],
        [T["severity"],         f"{sev_label}  ({sev_pct}%)",
         T["crop_health_index"], f"{health_index['score']}/100  — {health_category}"],
    ]
    pred_table = Table(pred_data, colWidths=[4 * cm, 5 * cm, 4 * cm, 5 * cm])
    pred_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREY),
        ("BACKGROUND", (0, 0), (0, 0), GREEN),
        ("TEXTCOLOR",  (0, 0), (0, 0), WHITE),
        ("FONTNAME",   (0, 0), (0, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [GREY, sev_bg]),
        ("BOX",        (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("INNERGRID",  (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(pred_table)
    story.append(Spacer(1, 0.3 * cm))

    # Per-class probabilities
    story.append(Paragraph(T["class_probability_breakdown"], styles["heading"]))
    sorted_probs = sorted(all_probs.items(), key=lambda x: -x[1])
    prob_rows    = [[
        Paragraph(disease_display_name(str(cls), lang), styles["body"]),
        Paragraph(f"{pct:.1f}%", styles["body"]),
        Paragraph("█" * int(pct / 5), styles["body"]),
    ] for cls, pct in sorted_probs]

    prob_table = Table(
        [[T["class"], T["probability"], T["visual"]]] + prob_rows,
        colWidths=[5 * cm, 3 * cm, 9 * cm],
    )
    prob_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR",    (0, 0), (-1, 0), WHITE),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GREY]),
        ("INNERGRID",    (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BOX",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 0.3 * cm))

    # ── ADVISORY ──────────────────────────────────────────────
    # NOTE: `advisory` should already be the LOCALIZED dict for `lang`
    # (i.e. call utils.advisory.get_advisory(disease, lang) before passing
    # it in) — this function only localizes the surrounding headings.
    story.append(Paragraph(T["agricultural_advisory"], styles["heading"]))

    # Description
    story.append(Paragraph(
        advisory.get("description", ""), styles["body"]
    ))
    story.append(Spacer(1, 0.2 * cm))

    # Treatment
    story.append(Paragraph(T["treatment"], styles["body"]))
    for item in advisory.get("treatment", []):
        story.append(Paragraph(f"• {item}", styles["bullet"]))

    story.append(Spacer(1, 0.15 * cm))

    # Prevention
    story.append(Paragraph(T["prevention"], styles["body"]))
    for item in advisory.get("prevention", []):
        story.append(Paragraph(f"• {item}", styles["bullet"]))

    story.append(Spacer(1, 0.15 * cm))

    # Fertilizer + irrigation
    adv_data = [
        [T["fertilizer_advice"], advisory.get("fertilizer", "—")],
        [T["irrigation_advice"], advisory.get("irrigation", "—")],
    ]
    adv_table = Table(adv_data, colWidths=[4 * cm, 14 * cm])
    adv_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (0, -1), LIME),
        ("FONTNAME",     (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("INNERGRID",    (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BOX",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
    ]))
    story.append(adv_table)
    story.append(Spacer(1, 0.5 * cm))

    # ── FOOTER ────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        T["footer_line1"],
        ParagraphStyle("Footer", fontSize=7, textColor=colors.grey, alignment=TA_CENTER)
    ))
    story.append(Paragraph(
        T["footer_line2"].format(ts=ts),
        ParagraphStyle("Footer2", fontSize=7, textColor=colors.grey, alignment=TA_CENTER)
    ))

    doc.build(story)
    return buf.getvalue()
