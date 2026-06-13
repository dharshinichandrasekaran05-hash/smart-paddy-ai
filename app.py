"""
app.py — Smart Paddy AI: Main Application
Fix applied: downy_mildew confidence boost (threshold trick) — no retraining needed.
"""

import os
import json
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

from utils.predict    import predict_image, get_model
from utils.advisory   import get_advisory, get_advisory_both_langs
from utils.ai_expert  import smart_farming_bot
from utils.voice      import speak_tamil, speak_english
from utils.logger     import (
    init_db, log_prediction, get_all_predictions,
    get_disease_counts, get_monthly_trends,
)
from utils.severity   import estimate_severity, crop_health_index
from utils.gradcam    import generate_gradcam, pil_to_bytes
from utils.pdf_report import generate_pdf_report
from utils.evaluation import (
    plot_confusion_matrix, compute_classification_report,
    plot_roc_curves, load_training_plots,
)

# ─────────────────────── APP CONFIG ───────────────────────────
st.set_page_config(
    page_title="Smart Paddy AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────── CUSTOM CSS ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d3b1e 0%, #145a32 60%, #1e8449 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.1);
}

.stat-card {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    border-left: 4px solid #27ae60;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 10px;
}
.stat-card h4 { margin: 0 0 4px; font-size: 13px; color: #666; font-weight: 500; }
.stat-card .val { font-size: 26px; font-weight: 700; color: #1a1a2e; }

.section-header {
    font-size: 18px;
    font-weight: 700;
    color: #145a32;
    border-bottom: 2px solid #27ae60;
    padding-bottom: 6px;
    margin: 20px 0 12px;
}

.chat-user {
    background: #d0e8ff;
    border-radius: 12px 12px 2px 12px;
    padding: 10px 14px;
    margin: 6px 0;
    max-width: 80%;
    margin-left: auto;
    font-size: 14px;
    color: #1a1a2e !important;
}
.chat-bot {
    background: #d4edda;
    border-radius: 12px 12px 12px 2px;
    padding: 10px 14px;
    margin: 6px 0;
    max-width: 85%;
    font-size: 14px;
    color: #1a1a2e !important;
    border-left: 3px solid #27ae60;
}
.chat-user *, .chat-bot * { color: #1a1a2e !important; }

.stButton > button {
    background: linear-gradient(135deg, #27ae60, #1e8449);
    color: white !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 20px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e8449, #145a32);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(39,174,96,0.3);
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-high   { background: #ffcdd2; color: #c62828; }
.badge-medium { background: #fff9c4; color: #f57f17; }
.badge-low    { background: #c8e6c9; color: #1b5e20; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────── INIT ─────────────────────────────────
init_db()
model, class_names = get_model()

# ─────────────────────── DOWNY MILDEW FIX ─────────────────────
# The model has 59.79% recall for downy_mildew despite balanced data.
# This is a visual similarity problem — the model rarely predicts it.
# Fix: boost downy_mildew's raw probability by 30% before argmax decision.
# This does NOT change the model weights — just adjusts the decision threshold.

DOWNY_MILDEW_BOOST = 1.30  # 30% boost — tune up/down if needed

def predict_with_fix(image):
    """
    Wraps predict_image() and applies downy_mildew confidence boost.
    Returns: (label, confidence, all_probs_dict)
    """
    label, confidence, all_probs = predict_image(image)

    # Build raw prob array in class order
    probs_array = np.array([all_probs.get(cn, 0.0) for cn in class_names])

    # Apply boost to downy_mildew
    if "downy_mildew" in class_names:
        dm_idx = class_names.index("downy_mildew")
        probs_array[dm_idx] *= DOWNY_MILDEW_BOOST

    # Re-normalise so probs sum to 1
    probs_array = probs_array / probs_array.sum()

    # Re-derive label and confidence
    best_idx   = int(np.argmax(probs_array))
    label      = class_names[best_idx]
    confidence = float(probs_array[best_idx])

    # Rebuild all_probs dict as percentages
    all_probs_fixed = {cn: round(float(probs_array[i]) * 100, 2)
                       for i, cn in enumerate(class_names)}

    return label, confidence, all_probs_fixed

# ─────────────────────── I18N ─────────────────────────────────
LABELS = {
    "english": {
        "title":        "Smart Paddy AI",
        "subtitle":     "Rice Disease Detection & Agricultural Decision Support",
        "upload":       "Upload Paddy Leaf Image",
        "detected":     "Detected Disease",
        "confidence":   "Model Confidence",
        "severity":     "Severity",
        "health":       "Crop Health Index",
        "risk":         "Risk Level",
        "advisory":     "Agricultural Advisory",
        "treatment":    "Treatment",
        "prevention":   "Prevention",
        "fertilizer":   "Fertilizer",
        "irrigation":   "Irrigation",
        "chatbot":      "Farming Assistant",
        "analytics":    "Analytics Dashboard",
        "research":     "Research Metrics",
        "hear_tamil":   "Hear Tamil Audio",
        "hear_eng":     "Hear English Audio",
        "download_pdf": "Download PDF Report",
        "all_conf":     "All Class Probabilities",
        "gradcam":      "Grad-CAM Explainability",
        "orig":         "Original Image",
        "heatmap":      "Infected Region Heatmap",
        "download_cam": "Download Heatmap",
        "ask":          "Ask the AI assistant...",
    },
    "tamil": {
        "title":        "ஸ்மார்ட் பேடி AI",
        "subtitle":     "நெல் நோய் கண்டறிதல் மற்றும் விவசாய ஆலோசனை",
        "upload":       "நெல் இலை படம் பதிவேற்றவும்",
        "detected":     "கண்டறியப்பட்ட நோய்",
        "confidence":   "மாதிரி நம்பகத்தன்மை",
        "severity":     "தீவிரம்",
        "health":       "பயிர் ஆரோக்கிய குறியீடு",
        "risk":         "அபாய நிலை",
        "advisory":     "விவசாய ஆலோசனை",
        "treatment":    "சிகிச்சை",
        "prevention":   "தடுப்பு",
        "fertilizer":   "உரம்",
        "irrigation":   "நீர்ப்பாசனம்",
        "chatbot":      "விவசாய உதவியாளர்",
        "analytics":    "ஆய்வு டாஷ்போர்டு",
        "research":     "ஆராய்ச்சி அளவீடுகள்",
        "hear_tamil":   "தமிழில் கேளுங்கள்",
        "hear_eng":     "ஆங்கிலத்தில் கேளுங்கள்",
        "download_pdf": "PDF அறிக்கை பதிவிறக்கம்",
        "all_conf":     "அனைத்து வகை நிகழ்தகவுகள்",
        "gradcam":      "தொற்று பகுதி வரைபடம்",
        "orig":         "அசல் படம்",
        "heatmap":      "தொற்று பகுதி வரைபடம்",
        "download_cam": "வரைபடம் பதிவிறக்கம்",
        "ask":          "AI உதவியாளரிடம் கேளுங்கள்...",
    },
}

# ─────────────────────── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 Smart Paddy AI")
    st.markdown("---")

    lang = st.selectbox(
        "🌐 Language / மொழி",
        ["english", "tamil"],
        format_func=lambda x: "English" if x == "english" else "தமிழ்",
    )
    L = LABELS[lang]

    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🔬 Diagnosis", "💬 Chatbot", "📊 Analytics", "📐 Research Metrics"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Optional Details**")
    farmer_name = st.text_input("Farmer Name", placeholder="e.g. Murugan")
    location    = st.text_input("Location",    placeholder="e.g. Thanjavur")


# ═══════════════════════════════════════════════════════════════
# PAGE: DIAGNOSIS
# ═══════════════════════════════════════════════════════════════
if "🔬 Diagnosis" in page:

    st.markdown(f"<h1 style='color:#145a32'>🌾 {L['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#555;font-size:15px'>{L['subtitle']}</p>", unsafe_allow_html=True)
    st.markdown("---")

    uploaded_file = st.file_uploader(L["upload"], type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        with st.spinner("Analysing leaf..."):
            # ✅ Using fixed predict function with downy_mildew boost
            label, confidence, all_probs = predict_with_fix(image)

        advisory_both = get_advisory_both_langs(label)
        advisory      = advisory_both[lang]

        # ── GRAD-CAM ──────────────────────────────────────────
        with st.spinner("Generating explainability heatmap..."):
            try:
                class_index       = class_names.index(label)
                orig_img, cam_img = generate_gradcam(model, image, class_index)
                gradcam_available = True
            except Exception:
                gradcam_available = False
                cam_img  = None
                orig_img = image.resize((224, 224))

        # ── SEVERITY + HEALTH ─────────────────────────────────
        if gradcam_available:
            from utils.gradcam import compute_gradcam
            from utils.predict import preprocess
            img_arr = preprocess(image)
            heatmap = compute_gradcam(model, img_arr, class_index)
        else:
            heatmap = None

        severity = estimate_severity(label, confidence, heatmap)
        health   = crop_health_index(label, confidence, severity["percentage"])

        log_prediction(
            disease=label,
            confidence=confidence,
            severity=severity["percentage"],
            health_idx=health["score"],
            location=location,
        )

        # ── GRADCAM + RESULT COLUMNS ───────────────────────────
        col_img, col_res = st.columns([1, 1], gap="large")

        with col_img:
            st.markdown(
                f"<div class='section-header'>{L['gradcam']}</div>",
                unsafe_allow_html=True,
            )
            img_col1, img_col2 = st.columns(2)
            with img_col1:
                st.image(orig_img, caption=L["orig"], use_column_width=True)
            with img_col2:
                if gradcam_available:
                    st.image(cam_img, caption=L["heatmap"], use_column_width=True)
                    st.download_button(
                        label=L["download_cam"],
                        data=pil_to_bytes(cam_img),
                        file_name="gradcam_heatmap.png",
                        mime="image/png",
                    )
                else:
                    st.info("Grad-CAM unavailable for this model layer.")

        with col_res:
            st.markdown(
                f"<div class='section-header'>{L['detected']}</div>",
                unsafe_allow_html=True,
            )

            disease_color = {
                "blast": "#f39c12", "brown_spot": "#e74c3c",
                "tungro": "#5c6bc0", "normal": "#27ae60",
                "healthy": "#27ae60",
            }.get(label.lower(), "#555")

            st.markdown(
                f"<div style='font-size:30px;font-weight:800;color:{disease_color}'>"
                f"{'🌿' if label.lower() in ['healthy','normal'] else '⚠️'} {label.replace('_',' ').title()}"
                f"</div>",
                unsafe_allow_html=True,
            )

            # ✅ FIX: Risk level should reflect BOTH confidence AND whether plant is healthy
            is_healthy = label.lower() in ("normal", "healthy")

            if is_healthy:
                risk, badge_cls, action_text = "LOW", "badge-low", (
                    "Crop looks healthy — routine monitoring sufficient" if lang == "english"
                    else "பயிர் ஆரோக்கியமாக உள்ளது — வழக்கமான கண்காணிப்பு போதுமானது"
                )
            elif confidence > 0.8:
                risk, badge_cls, action_text = "HIGH", "badge-high", (
                    "Immediate action required within 24 hrs" if lang == "english"
                    else "24 மணி நேரத்தில் உடனடி நடவடிக்கை தேவை"
                )
            elif confidence > 0.5:
                risk, badge_cls, action_text = "MEDIUM", "badge-medium", (
                    "Monitor and treat within 3 days" if lang == "english"
                    else "3 நாட்களுக்குள் கண்காணித்து சிகிச்சை அளிக்கவும்"
                )
            else:
                risk, badge_cls, action_text = "LOW", "badge-low", (
                    "Routine monitoring sufficient" if lang == "english"
                    else "வழக்கமான கண்காணிப்பு போதுமானது"
                )

            st.markdown(
                f"<span class='badge {badge_cls}'>{L['risk']}: {risk}</span>",
                unsafe_allow_html=True,
            )
            st.caption(f"⏱ {action_text}")
            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f"<div class='stat-card'>"
                    f"<h4>{L['confidence']}</h4>"
                    f"<div class='val'>{confidence * 100:.1f}%</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            with c2:
                sev_color = severity["color"]
                sev_label = severity["label"]
                sev_pct   = severity["percentage"]
                st.markdown(
                    f"<div class='stat-card' style='border-color:{sev_color}'>"
                    f"<h4>{L['severity']}</h4>"
                    f"<div class='val' style='color:{sev_color}'>"
                    f"{sev_label}<br>"
                    f"<span style='font-size:15px'>{sev_pct}%</span>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )
            with c3:
                hlth_color    = health["color"]
                hlth_score    = health["score"]
                hlth_category = health["category"]
                st.markdown(
                    f"<div class='stat-card' style='border-color:{hlth_color}'>"
                    f"<h4>{L['health']}</h4>"
                    f"<div class='val' style='color:{hlth_color}'>"
                    f"{hlth_score}/100<br>"
                    f"<span style='font-size:15px'>{hlth_category}</span>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # ── ALL CLASS PROBABILITIES ────────────────────────────
        st.markdown(
            f"<div class='section-header'>{L['all_conf']}</div>",
            unsafe_allow_html=True,
        )

        sorted_probs = sorted(all_probs.items(), key=lambda x: -x[1])
        cols = st.columns(len(sorted_probs))
        for i, (cls, pct) in enumerate(sorted_probs):
            with cols[i]:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=pct,
                    number={"suffix": "%", "font": {"size": 16}},
                    title={"text": cls.replace("_", " ").title(), "font": {"size": 11}},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar":  {"color": "#27ae60" if cls == label else "#bdc3c7"},
                        "steps": [
                            {"range": [0,   50], "color": "#f9f9f9"},
                            {"range": [50, 100], "color": "#eafaf1"},
                        ],
                    },
                ))
                fig_gauge.update_layout(height=160, margin=dict(l=5, r=5, t=30, b=5))
                st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("#### Severity & Health Overview")
        sev_fig = go.Figure()
        sev_fig.add_trace(go.Bar(
            x=["Severity %", "Health Index"],
            y=[severity["percentage"], health["score"]],
            marker_color=[severity["color"], health["color"]],
            text=[f"{severity['percentage']}%", f"{health['score']}/100"],
            textposition="outside",
        ))
        sev_fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=20, b=20),
            yaxis_range=[0, 110],
            showlegend=False,
        )
        st.plotly_chart(sev_fig, use_container_width=True)

        st.markdown("---")

        # ── ADVISORY ──────────────────────────────────────────
        st.markdown(
            f"<div class='section-header'>🌱 {L['advisory']}</div>",
            unsafe_allow_html=True,
        )

        adv_col1, adv_col2 = st.columns([1, 1], gap="large")

        with adv_col1:
            en_adv = advisory_both["english"]
            st.markdown("**🇬🇧 English**")
            st.info(en_adv["description"])
            st.markdown(f"**{L['treatment']}**")
            for item in en_adv["treatment"]:
                st.markdown(f"• {item}")
            st.markdown(f"**{L['prevention']}**")
            for item in en_adv["prevention"]:
                st.markdown(f"• {item}")
            col_f, col_i = st.columns(2)
            with col_f:
                st.success(f"🌱 **{L['fertilizer']}**\n\n{en_adv['fertilizer']}")
            with col_i:
                st.info(f"💧 **{L['irrigation']}**\n\n{en_adv['irrigation']}")
            if st.button(f"🔊 {L['hear_eng']}"):
                speak_english(en_adv["description"] + " " + " ".join(en_adv["treatment"]))

        with adv_col2:
            ta_adv = advisory_both["tamil"]
            st.markdown("**🇮🇳 தமிழ்**")
            st.info(ta_adv["description"])
            st.markdown("**சிகிச்சை**")
            for item in ta_adv["treatment"]:
                st.markdown(f"• {item}")
            st.markdown("**தடுப்பு**")
            for item in ta_adv["prevention"]:
                st.markdown(f"• {item}")
            col_f2, col_i2 = st.columns(2)
            with col_f2:
                st.success(f"🌱 **உரம்**\n\n{ta_adv['fertilizer']}")
            with col_i2:
                st.info(f"💧 **நீர்ப்பாசனம்**\n\n{ta_adv['irrigation']}")
            if st.button(f"🔊 {L['hear_tamil']}"):
                speak_tamil(ta_adv["description"] + " " + " ".join(ta_adv["treatment"]))

        st.markdown("---")

        # ── PDF REPORT ────────────────────────────────────────
        st.markdown("<div class='section-header'>📄 Report</div>", unsafe_allow_html=True)
        if st.button(f"📥 {L['download_pdf']}", type="primary"):
            with st.spinner("Building PDF report..."):
                pdf_bytes = generate_pdf_report(
                    original_image=image,
                    gradcam_image=cam_img if gradcam_available else None,
                    disease=label,
                    confidence=confidence,
                    all_probs=all_probs,
                    severity=severity,
                    health_index=health,
                    advisory=advisory_both["english"],
                    location=location,
                    farmer_name=farmer_name,
                )
            st.download_button(
                label="📄 Click to Save PDF",
                data=pdf_bytes,
                file_name=f"paddy_report_{label.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )

    else:
        st.markdown(
            "<div style='text-align:center;padding:60px 20px;color:#888'>"
            "<div style='font-size:80px'>🌾</div>"
            "<h3 style='color:#555'>Upload a paddy leaf image to begin diagnosis</h3>"
            "<p>Supports JPG, PNG, JPEG &nbsp;•&nbsp; EfficientNetB0 CNN Model</p>"
            "</div>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════
# PAGE: CHATBOT
# ═══════════════════════════════════════════════════════════════
elif "💬 Chatbot" in page:

    st.markdown(f"<h2 style='color:#145a32'>💬 {L['chatbot']}</h2>", unsafe_allow_html=True)
    st.caption("Ask about crop diseases, fertilizers, irrigation, pests, and more.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        greeting = (
            "Hello! I'm your Smart Paddy AI assistant. Ask me about rice diseases, "
            "fertilizers, irrigation, pests, or harvest tips!"
            if lang == "english" else
            "வணக்கம்! நான் ஸ்மார்ட் பேடி AI உதவியாளர். "
            "நெல் நோய்கள், உரம், நீர்ப்பாசனம் பற்றி கேளுங்கள்!"
        )
        st.session_state.chat_history.append({"role": "bot", "text": greeting})

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='chat-user'>👤 {msg['text']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='chat-bot'>🤖 {msg['text']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("**Quick questions:**")
    qcols = st.columns(4)
    quick = (
        ["How to treat blast?", "Fertilizer schedule", "Irrigation tips", "Pest control"]
        if lang == "english" else
        ["பிளாஸ்ட் சிகிச்சை?", "உர அட்டவணை", "நீர்ப்பாசன குறிப்புகள்", "பூச்சி மேலாண்மை"]
    )
    for i, q in enumerate(quick):
        with qcols[i]:
            if st.button(q, key=f"quick_{i}"):
                response = smart_farming_bot(q, lang=lang)
                st.session_state.chat_history.append({"role": "user", "text": q})
                st.session_state.chat_history.append({"role": "bot",  "text": response})
                st.rerun()

    user_query = st.text_input(
        L["ask"], key="chat_input",
        label_visibility="collapsed", placeholder=L["ask"],
    )
    send_col, clear_col = st.columns([4, 1])
    with send_col:
        if st.button("Send 📨", use_container_width=True) and user_query.strip():
            response = smart_farming_bot(user_query, lang=lang)
            st.session_state.chat_history.append({"role": "user", "text": user_query})
            st.session_state.chat_history.append({"role": "bot",  "text": response})
            st.rerun()
    with clear_col:
        if st.button("Clear 🗑", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ═══════════════════════════════════════════════════════════════
elif "📊 Analytics" in page:

    st.markdown(f"<h2 style='color:#145a32'>📊 {L['analytics']}</h2>", unsafe_allow_html=True)

    preds = get_all_predictions()

    if not preds:
        st.info("📤 Upload images on the Diagnosis page to populate the dashboard.")
    else:
        df = pd.DataFrame(preds)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["month"]     = df["timestamp"].dt.strftime("%Y-%m")

        total       = len(df)
        most_common = df["disease"].value_counts().idxmax()
        avg_conf    = df["confidence"].mean() * 100
        avg_health  = df["health_idx"].mean()

        s1, s2, s3, s4 = st.columns(4)
        for col, val, label_text, color in [
            (s1, str(total),              "Total Scans",         "#3498db"),
            (s2, most_common,             "Most Common Disease",  "#e74c3c"),
            (s3, f"{avg_conf:.1f}%",      "Avg Confidence",       "#27ae60"),
            (s4, f"{avg_health:.0f}/100", "Avg Health Index",     "#f39c12"),
        ]:
            with col:
                st.markdown(
                    f"<div class='stat-card' style='border-color:{color}'>"
                    f"<h4>{label_text}</h4><div class='val'>{val}</div></div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Disease Distribution")
            disease_counts         = df["disease"].value_counts().reset_index()
            disease_counts.columns = ["Disease", "Count"]
            fig_pie = px.pie(
                disease_counts, names="Disease", values="Count",
                color_discrete_sequence=["#27ae60","#e74c3c","#f39c12","#3498db","#9b59b6"],
                hole=0.35,
            )
            fig_pie.update_layout(height=320, margin=dict(l=0,r=0,t=20,b=0))
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.markdown("#### Scan Count by Disease")
            fig_bar = px.bar(
                disease_counts, x="Disease", y="Count",
                color="Disease",
                color_discrete_sequence=["#27ae60","#e74c3c","#f39c12","#3498db"],
                text="Count",
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(
                height=320, margin=dict(l=0,r=0,t=20,b=0), showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### Monthly Scan Trends")
        monthly = df.groupby("month").size().reset_index(name="count")
        fig_line = px.line(
            monthly, x="month", y="count",
            markers=True, line_shape="spline",
            color_discrete_sequence=["#27ae60"],
        )
        fig_line.update_layout(
            height=280, margin=dict(l=0,r=0,t=20,b=0),
            xaxis_title="Month", yaxis_title="Scans",
        )
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("#### Severity Distribution")
        fig_hist = px.histogram(df, x="severity", nbins=20,
                                color_discrete_sequence=["#f39c12"])
        fig_hist.update_layout(height=250, margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("#### Recent Predictions")
        disp               = df[["timestamp","disease","confidence","severity","health_idx"]].copy()
        disp["confidence"] = (disp["confidence"] * 100).round(1).astype(str) + "%"
        disp["severity"]   = disp["severity"].round(1).astype(str) + "%"
        disp["health_idx"] = disp["health_idx"].round(0).astype(int)
        disp.columns       = ["Timestamp","Disease","Confidence","Severity","Health Index"]
        st.dataframe(disp.head(20), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: RESEARCH METRICS
# ═══════════════════════════════════════════════════════════════
elif "📐 Research" in page:

    st.markdown(f"<h2 style='color:#145a32'>📐 {L['research']}</h2>", unsafe_allow_html=True)
    st.caption(
        "Confusion matrix, classification report, and training curves "
        "from the last training run."
    )

    train_curves, saved_cm = load_training_plots()

    if train_curves:
        st.markdown("#### Training Curves (from last training run)")
        st.image(train_curves, use_column_width=True)

    if saved_cm:
        st.markdown("#### Confusion Matrix (from last training run)")
        st.image(saved_cm, use_column_width=True)

    st.markdown("---")
    st.markdown("#### Upload Evaluation Data (Optional)")
    st.caption("Upload a CSV with columns `true_label` and `pred_label`.")

    eval_file = st.file_uploader("Upload evaluation CSV", type=["csv"])

    if eval_file:
        eval_df = pd.read_csv(eval_file)
        if "true_label" not in eval_df.columns or "pred_label" not in eval_df.columns:
            st.error("CSV must have columns: `true_label` and `pred_label`")
        else:
            all_cls = sorted(eval_df["true_label"].unique().tolist())
            cls_map = {c: i for i, c in enumerate(all_cls)}
            y_true  = eval_df["true_label"].map(cls_map).tolist()
            y_pred  = eval_df["pred_label"].map(cls_map).fillna(0).astype(int).tolist()

            cm_bytes = plot_confusion_matrix(y_true, y_pred, class_names=all_cls)
            st.image(cm_bytes, caption="Confusion Matrix", width=600)

            report = compute_classification_report(y_true, y_pred, class_names=all_cls)
            st.markdown(f"#### Overall Accuracy: **{report['accuracy']}%**")

            rep_rows = []
            for cls, m in report["per_class"].items():
                rep_rows.append({
                    "Class":     cls,
                    "Precision": f"{m['precision']}%",
                    "Recall":    f"{m['recall']}%",
                    "F1 Score":  f"{m['f1']}%",
                    "Support":   m["support"],
                })
            st.dataframe(pd.DataFrame(rep_rows), use_container_width=True)

            mc, wc = st.columns(2)
            with mc:
                st.markdown("**Macro Average**")
                st.json(report["macro_avg"])
            with wc:
                st.markdown("**Weighted Average**")
                st.json(report["weighted_avg"])

    st.markdown("---")
    st.markdown("#### Model Architecture Summary")
    model_info = {
        "Backbone":     "EfficientNetB0",
        "Input Size":   "128 x 128 x 3",
        "Head":         "GAP -> BN -> Dense(256) -> Dropout(0.4) -> Dense(128) -> Softmax",
        "Optimizer":    "Adam (lr=1e-3 -> 1e-5 fine-tune)",
        "Loss":         "Categorical Cross-Entropy + Label Smoothing",
        "Augmentation": "Rotation, Flip, Zoom, Brightness, Shear",
        "Balancing":    "Sklearn compute_class_weight (balanced)",
        "Callbacks":    "EarlyStopping, ReduceLROnPlateau, ModelCheckpoint",
        "DM Fix":       "downy_mildew threshold boost x1.30 at inference",
    }
    info_rows = [{"Parameter": k, "Value": v} for k, v in model_info.items()]
    st.dataframe(pd.DataFrame(info_rows), use_container_width=True, hide_index=True)