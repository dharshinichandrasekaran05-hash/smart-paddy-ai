# app.py — Smart Paddy AI: Main Application
# Role-based access control:
#   - Admin  (dharshu / admin123): all pages
#   - Guest  (no login required):  Diagnosis + Chatbot

import os
import csv
import json
import io
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

from utils.predict    import predict_image, get_model
from utils.advisory   import get_advisory, get_advisory_both_langs
from utils.ai_expert  import smart_farming_bot
from utils.voice      import speak
from utils.logger     import (
    init_db, log_prediction, get_all_predictions,
    get_disease_counts, get_monthly_trends,
)
from utils.severity   import estimate_severity, crop_health_index, advanced_health_dashboard
from utils.gradcam    import generate_gradcam, pil_to_bytes
from utils.pdf_report import generate_pdf_report
from utils.evaluation import (
    plot_confusion_matrix, compute_classification_report,
    plot_roc_curves, load_training_plots,
)
from utils.explainability     import generate_explainability_report
from utils.gemini_client      import is_configured as gemini_is_configured
from utils.treatment_analysis import get_treatment_effectiveness
from utils.paddy_buddy        import render_paddy_buddy, render_paddy_chat_panel
from utils.i18n import (
    LANGUAGE_ORDER, DEFAULT_LANGUAGE, native_name, resolve_lang,
    get_ui_labels, ui_text, disease_display_name, risk_label, action_text,
    chatbot_greeting, quick_questions, translate_enum, tts_code,
    get_capability_dimensions, get_metric_names,
    translate_treatment_name, translate_treatment_stage,
)

# ═══════════════════════════════════════════════════════════════
# APP CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Smart Paddy AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
ADMIN_USERNAME = "dharshu"
ADMIN_PASSWORD = "admin123"
PRED_LOG_FILE  = "predictions_log.csv"

# ── Palette used only by the Model Performance page (added feature) ──
PALETTE = {
    "bg":            "#0b2117",
    "bg_soft":       "#103323",
    "grid":          "#28523b",
    "text":          "#f1f7f2",
    "text_muted":    "#a9beb0",
    "primary":       "#17693b",
    "primary_light": "#5fd17d",
    "secondary":     "#8aa39a",
    "accent_blue":   "#3b82c4",
    "accent_amber":  "#e0a72e",
    "accent_red":    "#d1495b",
    "accent_purple": "#8e6bb0",
}

def style_fig(fig, height=360, showlegend=True):
    """Apply a single consistent, professional theme to any Plotly figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor=PALETTE["bg"],
        plot_bgcolor=PALETTE["bg"],
        font=dict(family="Inter, sans-serif", color=PALETTE["text"], size=13),
        title_font=dict(family="Poppins, sans-serif", color=PALETTE["text"]),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)", font=dict(color=PALETTE["text_muted"]),
        ) if showlegend else dict(),
        showlegend=showlegend,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_xaxes(
        showgrid=False, zeroline=False,
        linecolor=PALETTE["grid"], tickfont=dict(color=PALETTE["text_muted"]),
        title_font=dict(color=PALETTE["text_muted"]),
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=PALETTE["grid"], zeroline=False,
        tickfont=dict(color=PALETTE["text_muted"]),
        title_font=dict(color=PALETTE["text_muted"]),
    )
    return fig

# Pages each role can access — used for nav AND access-guard
GUEST_PAGES = ["🔬 Diagnosis", "💬 Chatbot", "📊 Model Performance"]
ADMIN_PAGES = ["🔬 Diagnosis", "💬 Chatbot", "📊 Model Performance", "📊 Analytics",
               "👑 Admin Dashboard", "📋 Full History"]

# ═══════════════════════════════════════════════════════════════
# SESSION STATE — initialise once
# ═══════════════════════════════════════════════════════════════
for key, default in {
    "logged_in": False,
    "is_admin":  False,
    "username":  "Guest",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ═══════════════════════════════════════════════════════════════
# CSV PREDICTION LOGGER
# ═══════════════════════════════════════════════════════════════
def init_pred_log():
    if not os.path.exists(PRED_LOG_FILE):
        with open(PRED_LOG_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["Username", "Time", "Predicted Disease"])

def log_pred_csv(username: str, disease: str):
    init_pred_log()
    with open(PRED_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), disease])

def load_pred_log() -> pd.DataFrame:
    init_pred_log()
    try:
        return pd.read_csv(PRED_LOG_FILE)
    except Exception:
        return pd.DataFrame(columns=["Username", "Time", "Predicted Disease"])

# ═══════════════════════════════════════════════════════════════
# ACCESS GUARD  — call at the top of every restricted page
# ═══════════════════════════════════════════════════════════════
def require_admin():
    """Stop rendering and show an error if the current user is not admin."""
    if not st.session_state.is_admin:
        # `L` is set once the sidebar (language selector) has rendered,
        # which always happens before any page body — safe to read here.
        st.error(L["access_denied"])
        st.stop()

# ═══════════════════════════════════════════════════════════════
# MODEL PERFORMANCE — sample research data generator (added feature)
# ═══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def generate_research_data(lang: str = "english"):
    """
    Produces a fixed, realistic-looking sample dataset comparing an
    'Existing System' against the 'Proposed Smart Paddy AI' system.
    Values are deterministic (seeded) so charts/tables/cards always agree.

    `lang` only affects the DISPLAYED column/row labels (via utils.i18n) —
    cached separately per language since it's part of the function's
    argument signature, so switching language always shows fresh labels.
    """
    from utils.i18n import get_ui_labels, get_metric_names
    Lx = get_ui_labels(lang)

    rng = np.random.default_rng(42)

    metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]   # stable internal keys
    metrics_display = get_metric_names(lang)                    # localized labels, same order
    existing_scores = {
        "Accuracy":  84.2,
        "Precision": 81.7,
        "Recall":    80.5,
        "F1-Score":  81.1,
    }
    proposed_scores = {
        "Accuracy":  96.4,
        "Precision": 95.8,
        "Recall":    95.1,
        "F1-Score":  95.4,
    }

    col_metric    = Lx["col_metric"]
    col_existing  = Lx["col_existing_system_pct"]
    col_proposed  = Lx["col_proposed_system_pct"]
    col_improve   = Lx["col_improvement_pct"]

    comparison_df = pd.DataFrame({
        col_metric:   metrics_display,
        col_existing: [existing_scores[m] for m in metrics],
        col_proposed: [proposed_scores[m] for m in metrics],
    })
    comparison_df[col_improve] = (
        comparison_df[col_proposed] - comparison_df[col_existing]
    ).round(1)

    epochs = list(range(1, 11))
    existing_trend = np.round(np.linspace(75.0, 84.2, 10) + rng.uniform(-0.6, 0.6, 10), 1)
    proposed_trend = np.round(np.linspace(85.0, 96.4, 10) + rng.uniform(-0.4, 0.4, 10), 1)

    trend_df = pd.DataFrame({
        "Epoch": epochs,
        "Existing System": existing_trend,
        "Proposed Smart Paddy AI": proposed_trend,
    })

    return {
        "metrics": metrics,
        "existing_scores": existing_scores,
        "proposed_scores": proposed_scores,
        "comparison_df": comparison_df,
        "trend_df": trend_df,
        "col_existing": col_existing,
        "col_proposed": col_proposed,
        "col_improve": col_improve,
    }

# ═══════════════════════════════════════════════════════════════
# MODEL COMPARISON — conceptual capability comparison (added feature)
# ═══════════════════════════════════════════════════════════════
# NOTE: These are NOT measured accuracy/precision/recall/F1 values.
# They are a qualitative, design-rationale rating (1-5) used only to
# visually justify why EfficientNetB0 was selected as the proposed
# model. No experimental results are implied or claimed.
@st.cache_data(show_spinner=False)
def generate_model_capability_data(lang: str = "english"):
    """
    Conceptual capability comparison — CNN vs ResNet50 vs EfficientNetB0.
    Scores are normalized 1-5 design-rationale ratings reflecting known
    architectural properties (depth, compound scaling, parameter
    efficiency, transfer learning), NOT measured accuracy/precision/
    recall/F1 results from a held-out test set.

    `lang` localizes the dimension names shown as chart x-axis categories
    (via utils.i18n.get_capability_dimensions) — cached per language.
    """
    dimensions = get_capability_dimensions(lang)

    scores = {
        "CNN (Baseline)":            [2.5, 4.0, 3.0, 2.0, 2.4],
        "ResNet50 (Benchmark)":      [4.2, 2.0, 2.5, 3.5, 3.4],
        "EfficientNetB0 (Proposed)": [4.8, 4.7, 4.8, 4.7, 4.9],
    }

    model_comparison_df = pd.DataFrame({"Dimension": dimensions, **scores})
    return {"dimensions": dimensions, "scores": scores, "model_comparison_df": model_comparison_df}


# ═══════════════════════════════════════════════════════════════
# FEATURE COVERAGE — existing system vs Smart Paddy AI (added feature)
# ═══════════════════════════════════════════════════════════════
# NOTE: This graph represents the presence/scope of system features,
# NOT model accuracy. It is used only to communicate the functional
# innovation of Smart Paddy AI relative to a conventional paddy
# disease classification system.
#
# NOTE: This function is intentionally no longer called from the
# Research Metrics page — that page must contain only the capability
# comparison, model-selection rationale, accuracy/precision/recall/F1
# comparison, and final conclusion (no separate feature table/list).
# The function is kept here in case another page wants to use it.
@st.cache_data(show_spinner=False)
def generate_feature_coverage_data():
    """
    Feature coverage comparison — Existing Disease Classification
    System vs Smart Paddy AI. Values are 0 (not present) / 1 (present),
    reflecting system functionality scope only.
    """
    features = [
        "Leaf Disease Detection",
        "Severity Analysis",
        "Explainable AI (Grad-CAM)",
        "Crop Health Index / Estimation",
        "Treatment & Advisory Recommendations",
        "Tamil and English Support",
        "Voice Guidance",
        "Farmer Assistance Chatbot",
        "Government Scheme Suggestions",
        "Prediction History & Analytics",
    ]
    existing = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    smart_paddy = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    feature_df = pd.DataFrame({
        "Feature": features,
        "Existing Disease Classification System": existing,
        "Smart Paddy AI": smart_paddy,
    })
    return {"features": features, "existing": existing, "smart_paddy": smart_paddy, "feature_df": feature_df}

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d3b1e 0%, #145a32 60%, #1e8449 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background: rgba(255,255,255,0.1); }
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: white !important;
    border-radius: 6px;
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

.chat-user, .chat-bot {
    display: block;
    box-sizing: border-box;
    padding: 10px 14px;
    margin: 7px 0;
    max-width: 86%;
    min-width: 0;
    font-size: 14px;
    line-height: 1.55;
    white-space: pre-wrap !important;
    overflow-wrap: break-word !important;
    word-break: normal !important;
    writing-mode: horizontal-tb !important;
}
.chat-user {
    background: #d0e8ff;
    border-radius: 12px 12px 2px 12px;
    margin-left: auto;
    color: #1a1a2e !important;
}
.chat-bot {
    background: #d4edda;
    border-radius: 12px 12px 12px 2px;
    margin-right: auto;
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

.role-tag {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.role-admin { background: rgba(255,193,7,0.25); border: 1px solid rgba(255,193,7,0.6); }
.role-guest { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); }

/* ── Model Performance page styling (added feature) ──────────── */
.perf-header {
    background: linear-gradient(135deg, #ffffff 0%, #f2fbf5 100%);
    border-radius: 18px;
    padding: 26px 30px;
    margin-bottom: 20px;
    box-shadow: 0 6px 24px rgba(20,90,50,0.09);
    border: 1px solid #e2f3e9;
}
.perf-header h1, .perf-header h2 {
    margin: 0;
    color: #123f24;
    font-weight: 800;
    letter-spacing: -0.4px;
}
.perf-header p {
    margin: 8px 0 0;
    color: #5c6f64;
    font-size: 14.5px;
}
.perf-divider {
    height: 4px;
    width: 70px;
    background: linear-gradient(90deg, #2ecc71, #17693b);
    border-radius: 6px;
    margin-top: 16px;
}
.section-sub {
    font-size: 13.5px;
    color: #6f8478;
    margin: -8px 0 16px;
}
.research-summary-box {
    background: linear-gradient(135deg, #f4fbf6 0%, #e4f8ec 100%);
    border: 1px solid #b9e8c8;
    border-left: 6px solid #2ecc71;
    border-radius: 16px;
    padding: 22px 26px;
    color: #123f24;
    font-size: 15.5px;
    line-height: 1.7;
    box-shadow: 0 4px 16px rgba(20,90,50,0.06);
}

/* ── Premium Smart Agriculture palette: styling only ─────────── */
:root {
    --sp-bg: #06130d;
    --sp-bg-2: #0a2117;
    --sp-card: #103323;
    --sp-card-2: #16452e;
    --sp-emerald: #28b66a;
    --sp-lime: #a8d95b;
    --sp-gold: #d8ad45;
    --sp-text: #f1f7f2;
    --sp-muted: #a9beb0;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 80% 0%, rgba(40,182,106,0.10), transparent 34%), var(--sp-bg) !important;
}
[data-testid="stHeader"] { background: rgba(6,19,13,0.82) !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(165deg, #06130d 0%, #0b2b1b 58%, #145235 100%) !important;
    border-right: 1px solid rgba(216,173,69,0.22);
}
[data-testid="stSidebar"] * { color: var(--sp-text) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] input {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(168,217,91,0.35) !important;
}
[data-testid="stAppViewContainer"] .stMarkdown,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {
    color: var(--sp-text);
}
.stat-card, .perf-header, .research-summary-box {
    background: linear-gradient(145deg, var(--sp-card-2), var(--sp-card)) !important;
    border-color: rgba(168,217,91,0.24) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.24) !important;
}
.stat-card h4, .perf-header p, .section-sub { color: var(--sp-muted) !important; }
.stat-card .val, .perf-header h1, .perf-header h2, .research-summary-box { color: var(--sp-text) !important; }
.section-header { color: var(--sp-lime) !important; border-bottom-color: var(--sp-gold) !important; }
.research-summary-box { border-left-color: var(--sp-gold) !important; }
.stButton > button {
    background: linear-gradient(135deg, #237c4b, #17613b) !important;
    border: 1px solid rgba(216,173,69,0.42) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.20);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2d9b5d, #1b7044) !important;
    box-shadow: 0 5px 16px rgba(40,182,106,0.24) !important;
}
[data-testid="stFileUploader"] {
    background: rgba(16,51,35,0.82) !important;
    border: 1px solid rgba(168,217,91,0.24) !important;
    border-radius: 12px;
}
    [data-testid="stMetric"] {
    background: rgba(16,51,35,0.78) !important;
    border: 1px solid rgba(168,217,91,0.20) !important;
    border-radius: 12px;
}
.stat-card, .perf-header, .research-summary-box,
[data-testid="stMetric"], [data-testid="stExpander"] {
    transition: box-shadow 180ms ease, border-color 180ms ease, filter 180ms ease;
}
.stat-card:hover, .perf-header:hover, .research-summary-box:hover,
[data-testid="stMetric"]:hover, [data-testid="stExpander"]:hover {
    border-color: rgba(216,173,69,0.38) !important;
    box-shadow: 0 10px 28px rgba(40,182,106,0.14) !important;
    filter: brightness(1.03);
}
[data-testid="stAlert"] { border-radius: 10px; }

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# INIT BACKENDS
# ═══════════════════════════════════════════════════════════════
init_db()
init_pred_log()
model, class_names = get_model()

# ═══════════════════════════════════════════════════════════════
# DOWNY MILDEW CONFIDENCE FIX  (threshold trick — no retraining)
# ═══════════════════════════════════════════════════════════════
DOWNY_MILDEW_BOOST = 1.30

@st.cache_data(show_spinner=False)
def _cached_prediction(image_bytes: bytes):
    """Run ML prediction once per image, including across language reruns."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    label, confidence, all_probs = predict_image(image)
    probs_array = np.array([all_probs.get(cn, 0.0) for cn in class_names])
    if "downy_mildew" in class_names:
        probs_array[class_names.index("downy_mildew")] *= DOWNY_MILDEW_BOOST
    total = float(probs_array.sum()) or 1.0
    probs_array = probs_array / total
    best_idx = int(np.argmax(probs_array))
    label = class_names[best_idx]
    confidence = float(probs_array[best_idx])
    all_probs_fixed = {cn: round(float(probs_array[i]) * 100, 2)
                       for i, cn in enumerate(class_names)}
    return label, confidence, all_probs_fixed


def predict_with_fix(image):
    """Backward-compatible wrapper used by the existing application flow."""
    buf = io.BytesIO()
    image.convert("RGB").save(buf, format="PNG")
    return _cached_prediction(buf.getvalue())


@st.cache_data(show_spinner=False)
def _cached_gradcam(image_bytes: bytes, class_index: int):
    """Reuse an existing Grad-CAM when only UI language changes."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return generate_gradcam(model, image, class_index)

# ═══════════════════════════════════════════════════════════════
# ADVISORY HELPER — renders one language's advisory block + TTS button
# ═══════════════════════════════════════════════════════════════
def render_advisory_block(col, adv: dict, lang_key: str, heading: str, L: dict):
    # BUGFIX: this used to receive the globally-selected-language `L`
    # for BOTH the selected-language column AND the English comparison
    # column, so the "English" column's own section headings (Treatment/
    # Prevention/Fertilizer/Irrigation/Listen) were shown in whatever
    # language was picked in the sidebar instead of English. Each column
    # must use labels for ITS OWN `lang_key`, not the caller's `L`.
    L_col = get_ui_labels(lang_key)
    with col:
        st.markdown(f"**{heading}**")
        st.info(adv["description"])
        st.markdown(f"**{L_col['treatment']}**")
        for item in adv["treatment"]:
            st.markdown(f"• {item}")
        st.markdown(f"**{L_col['prevention']}**")
        for item in adv["prevention"]:
            st.markdown(f"• {item}")
        col_f, col_i = st.columns(2)
        with col_f:
            st.success(f"🌱 **{L_col['fertilizer']}**\n\n{adv['fertilizer']}")
        with col_i:
            st.info(f"💧 **{L_col['irrigation']}**\n\n{adv['irrigation']}")
        if st.button(f"🔊 {L_col['listen']} ({native_name(lang_key)})", key=f"tts_{lang_key}"):
            speak(adv["description"] + " " + " ".join(adv["treatment"]), lang_key)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌾 Smart Paddy AI")
    st.markdown("---")

    # ── Language selector — all 11 languages from utils/i18n.py ──
    # (Deliberately resolved BEFORE anything else in the sidebar so every
    # label below — including the role identity badge — can be localized.)
    # PERSISTENCE FIX: the selectbox previously had no `key` and always
    # defaulted to DEFAULT_LANGUAGE on every browser reload (Streamlit's
    # widget state does not survive an actual page refresh / new session).
    # We now read/write the selection to st.query_params so the language
    # sticks across reloads (e.g. ?lang=tamil in the URL) while everything
    # else about the widget — its label, options, styling — is unchanged.
    _lang_from_url = resolve_lang(st.query_params.get("lang", DEFAULT_LANGUAGE))
    lang = st.selectbox(
        ui_text("language_selector", _lang_from_url),
        LANGUAGE_ORDER,
        index=LANGUAGE_ORDER.index(_lang_from_url),
        format_func=native_name,
        key="selected_lang",
    )
    lang = resolve_lang(lang)
    if st.query_params.get("lang") != lang:
        st.query_params["lang"] = lang
    L = get_ui_labels(lang)

    # Provider failures are handled invisibly by the chatbot provider chain;
    # the farmer receives a localized Groq or local Paddy response instead of
    # raw quota, authentication, traceback, or request details.

    st.markdown("---")

    # ── Role identity badge ────────────────────────────────────
    if st.session_state.is_admin:
        st.markdown(
            f"<div style='margin-bottom:8px'>{L['signed_in_as']} &nbsp;"
            f"<span class='role-tag role-admin'>👑 {L['admin_role']}</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='margin-bottom:8px'>{L['browsing_as']} &nbsp;"
            f"<span class='role-tag role-guest'>👤 {L['guest_role']}</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Navigation — list filtered by role ────────────────────
    # NOTE: page KEYS (emoji + English name) stay fixed and are used for
    # routing (`if "🔬 Diagnosis" in page:` etc. further down) — only the
    # DISPLAYED label is translated, via format_func. st.radio still
    # returns the original (untranslated) value from `allowed_pages`, so
    # routing logic is completely unaffected by the selected language.
    _PAGE_LABEL_KEYS = {
        "🔬 Diagnosis":         "title",
        "💬 Chatbot":           "chatbot",
        "📊 Model Performance": "model_performance_title",
        "📊 Analytics":         "analytics",
        "👑 Admin Dashboard":   "admin_dashboard_title",
        "📋 Full History":      "full_history_title",
        "📐 Research":          "research",
    }
    def _page_display(p: str) -> str:
        emoji, _, rest = p.partition(" ")
        key = _PAGE_LABEL_KEYS.get(p)
        label_text = L.get(key, rest) if key else rest
        return f"{emoji} {label_text}"

    allowed_pages = ADMIN_PAGES if st.session_state.is_admin else GUEST_PAGES

    # The floating Panda is a launcher for this existing Farming Assistant
    # page. Set the radio widget state before it is created, then let the
    # original page rendering below handle the chatbot exactly as before.
    if st.session_state.pop("pb_go_to_farming", False):
        st.session_state["main_page"] = "💬 Chatbot"

    selected_page = st.session_state.get("main_page", allowed_pages[0])
    if selected_page not in allowed_pages:
        selected_page = allowed_pages[0]

    page = st.radio(
        L["navigate_label"], allowed_pages,
        index=allowed_pages.index(selected_page),
        format_func=_page_display,
        label_visibility="collapsed",
        key="main_page",
    )

    st.markdown("---")

    # ── Optional farmer details (guest + admin) ────────────────
    st.markdown(f"**{L['optional_details']}**")
    farmer_name = st.text_input(L["farmer_name_label"], placeholder=L["farmer_name_ph"])
    location    = st.text_input(L["location_label"],    placeholder=L["location_ph"])

    st.markdown("---")

    # ── Admin login / logout ───────────────────────────────────
    if not st.session_state.is_admin:
        st.markdown(f"**{L['admin_login_heading']}**")
        a_user = st.text_input(L["username_label"], key="sb_admin_user")
        a_pass = st.text_input(L["password_label"], type="password", key="sb_admin_pass")
        if st.button(L["login_as_admin_btn"]):
            if a_user == ADMIN_USERNAME and a_pass == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.is_admin  = True
                st.session_state.username  = ADMIN_USERNAME
                st.success(L["login_success"])
                st.rerun()
            else:
                st.error(L["invalid_credentials"])
    else:
        if st.button(L["logout_btn"]):
            st.session_state.logged_in = False
            st.session_state.is_admin  = False
            st.session_state.username  = "Guest"
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: DIAGNOSIS  — Guest + Admin
# ═══════════════════════════════════════════════════════════════
if "🔬 Diagnosis" in page:

    st.markdown(f"<h1 style='color:#145a32'>🌾 {L['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#555;font-size:15px'>{L['subtitle']}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Keep the widget identity stable across language changes. The translated
    # label is rendered separately so changing language cannot clear the file.
    st.markdown(f"**{L['upload']}**")
    uploaded_file = st.file_uploader(
        "Paddy leaf image",
        type=["jpg", "png", "jpeg"],
        key="diagnosis_uploader",
        label_visibility="collapsed",
    )

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        st.session_state["diagnosis_image_bytes"] = image_bytes
    else:
        image_bytes = st.session_state.get("diagnosis_image_bytes")
        if image_bytes:
            uploaded_file = io.BytesIO(image_bytes)

    if uploaded_file:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # PaddyBuddy reaction: curious while a fresh leaf image just arrived
        st.session_state.pb_mood = "curious"

        with st.spinner(L["analysing_leaf"]):
            st.session_state.pb_mood = "thinking"
            label, confidence, all_probs = _cached_prediction(image_bytes)

        # ── Resolve final username for logging ─────────────────
        # Priority: typed Farmer Name > session username > "Guest"
        if farmer_name and farmer_name.strip():
            resolved_username = farmer_name.strip()
        elif st.session_state.username:
            resolved_username = st.session_state.username
        else:
            resolved_username = "Guest"

        # Log to both CSV and SQLite
        log_pred_csv(resolved_username, label)

        # advisory.py only ships English + Tamil copy today. get_advisory()
        # already falls back to English for any other language key, so this
        # never crashes — it just means non-Tamil/English readers currently
        # see English treatment/prevention text until those are translated.
        # advisory.py now translates on demand (via Gemini) for every one of
        # the 11 supported languages, not just English/Tamil — see
        # utils/advisory.py's _translate_advisory_dict().
        adv_selected = get_advisory(label, lang)
        adv_english  = get_advisory(label, "english")
        advisory     = adv_selected

        # ── Grad-CAM ───────────────────────────────────────────
        # NOTE: orig_img / cam_img / class_index are ONLY guaranteed
        # to exist if gradcam_available is True. Every downstream use
        # of these variables MUST be guarded by that flag — the crash
        # previously seen ("TypeError" on st.image(orig_img, ...))
        # happened because orig_img was referenced unconditionally
        # even when generate_gradcam() had raised and left it unset.
        gradcam_available = False
        orig_img = None
        cam_img = None
        class_index = None
        gradcam_error = None

        with st.spinner(L["generating_heatmap"]):
            try:
                class_index = class_names.index(label)
                orig_img, cam_img = _cached_gradcam(image_bytes, class_index)
                gradcam_available = True
            except Exception as e:
                gradcam_available = False
                orig_img = None
                cam_img = None
                gradcam_error = e

        if not gradcam_available and gradcam_error is not None:
            st.error(L["gradcam_failed"])
            st.exception(gradcam_error)

        # ── Severity + Health ──────────────────────────────────
        heatmap = None

        if gradcam_available:
            try:
                from utils.gradcam import compute_gradcam
                from utils.predict import preprocess

                heatmap = compute_gradcam(
                    model,
                    preprocess(image),
                    class_index
                )
            except Exception as e:
                st.error(L["heatmap_failed"])
                st.exception(e)
                heatmap = None

        severity = estimate_severity(label, confidence, heatmap)
        health   = crop_health_index(label, confidence, severity["percentage"])
        dashboard = advanced_health_dashboard(
            label, confidence, severity, health,
            lang=lang, disease_display=disease_display_name(label, lang),
        )
        explain   = generate_explainability_report(label, confidence, heatmap, severity["percentage"], lang=lang)
        # NOTE: get_treatment_effectiveness already accepted a `lang` param
        # in the original code. Whether it has translated content for all
        # 11 languages (vs. just English/Tamil) depends on that module,
        # which wasn't provided — verify there if non-EN/TA output matters.
        treatment_data = get_treatment_effectiveness(label, severity["percentage"], lang)

        # ── Feed this diagnosis to the Gemini chatbot as context ────
        # The Chatbot page (below) reads this dict so the AI assistant
        # can answer "what should I do now?"-style follow-ups without
        # the farmer re-explaining their situation.
        st.session_state.diagnosis_context = {
            "disease":            disease_display_name(label, lang),
            "confidence":         confidence * 100,
            "severity_label":     translate_enum(severity["label"], lang),
            "severity_pct":       severity["percentage"],
            "health_score":       health["score"],
            "health_category":    translate_enum(health["category"], lang),
            "recovery_potential": translate_enum(dashboard["recovery_potential"], lang),
            "treatment":          "; ".join(advisory.get("treatment", [])),
            "prevention":         "; ".join(advisory.get("prevention", [])),
        }

        # PaddyBuddy reaction: happy for a healthy leaf, concerned-but-
        # reassuring when a disease was detected — read-only reaction to
        # the EXISTING prediction result, never influences it.
        if label.lower() in ("healthy", "normal"):
            st.session_state.pb_mood = "happy"
        else:
            st.session_state.pb_mood = "concerned"

        log_prediction(
            disease=label,
            confidence=confidence,
            severity=severity["percentage"],
            health_idx=health["score"],
            location=location,
            farmer_name=resolved_username,
        )

        # ── Image + Result columns ─────────────────────────────
        col_img, col_res = st.columns([1, 1], gap="large")

        with col_img:
            st.markdown(
                f"<div class='section-header'>{L['gradcam']}</div>",
                unsafe_allow_html=True,
            )
            img_col1, img_col2 = st.columns(2)
            with img_col1:
                # Fall back to the raw uploaded image whenever Grad-CAM
                # failed, instead of touching the possibly-unset orig_img.
                display_orig = orig_img if gradcam_available else image
                st.image(display_orig, caption=L["orig"], use_container_width=True)
            with img_col2:
                if gradcam_available:
                    st.image(cam_img, caption=L["heatmap"], use_container_width=True)
                    st.download_button(
                        label=L["download_cam"],
                        data=pil_to_bytes(cam_img),
                        file_name="gradcam_heatmap.png",
                        mime="image/png",
                    )
                else:
                    st.info(L["gradcam_unavailable"])

        with col_res:
            st.markdown(
                f"<div class='section-header'>{L['detected']}</div>",
                unsafe_allow_html=True,
            )

            disease_color = {
                "blast":                     "#f39c12",
                "brown_spot":                "#e74c3c",
                "tungro":                    "#5c6bc0",
                "bacterial_panicle_blight":  "#8e44ad",
                "bacterial_leaf_blight":     "#d35400",
                "bacterial_leaf_streak":     "#c0392b",
                "dead_heart":                "#7f8c8d",
                "downy_mildew":              "#16a085",
                "hispa":                     "#2980b9",
                "normal":                    "#27ae60",
                "healthy":                   "#27ae60",
            }.get(label.lower(), "#555")

            display_name = disease_display_name(label, lang)

            st.markdown(
                f"<div style='font-size:30px;font-weight:800;color:{disease_color}'>"
                f"{'🌿' if label.lower() in ['healthy','normal'] else '⚠️'} "
                f"{display_name}</div>",
                unsafe_allow_html=True,
            )

            is_healthy = label.lower() in ("normal", "healthy")

            if is_healthy:
                action_level, risk_level, badge_cls = "healthy", "low", "badge-low"
            elif confidence > 0.8:
                action_level, risk_level, badge_cls = "high", "high", "badge-high"
            elif confidence > 0.5:
                action_level, risk_level, badge_cls = "medium", "medium", "badge-medium"
            else:
                action_level, risk_level, badge_cls = "low", "low", "badge-low"

            risk = risk_label(risk_level, lang)
            action_msg = action_text(action_level, lang)

            st.markdown(
                f"<span class='badge {badge_cls}'>{L['risk']}: {risk}</span>",
                unsafe_allow_html=True,
            )
            st.caption(f"⏱ {action_msg}")
            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f"<div class='stat-card'><h4>{L['confidence']}</h4>"
                    f"<div class='val'>{confidence * 100:.1f}%</div></div>",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"<div class='stat-card' style='border-color:{severity['color']}'>"
                    f"<h4>{L['severity']}</h4>"
                    f"<div class='val' style='color:{severity['color']}'>"
                    f"{translate_enum(severity['label'], lang)}<br>"
                    f"<span style='font-size:15px'>{severity['percentage']}%</span>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f"<div class='stat-card' style='border-color:{health['color']}'>"
                    f"<h4>{L['health']}</h4>"
                    f"<div class='val' style='color:{health['color']}'>"
                    f"{health['score']}/100<br>"
                    f"<span style='font-size:15px'>{translate_enum(health['category'], lang)}</span>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # ── All class probabilities ────────────────────────────
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
                    title={"text": disease_display_name(cls, lang), "font": {"size": 11}},
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

        st.markdown(f"#### {L['severity_health_overview_header']}")
        sev_fig = go.Figure()
        sev_fig.add_trace(go.Bar(
            x=[L["severity_pct_axis_label"], L["health_index_axis_label"]],
            y=[severity["percentage"], health["score"]],
            marker_color=[severity["color"], health["color"]],
            text=[f"{severity['percentage']}%", f"{health['score']}/100"],
            textposition="outside",
        ))
        sev_fig.update_layout(
            height=250, margin=dict(l=10, r=10, t=20, b=20),
            yaxis_range=[0, 110], showlegend=False,
        )
        st.plotly_chart(sev_fig, use_container_width=True)

        st.markdown("---")

        # ── Enhanced Crop Health Intelligence Dashboard ─────────
        st.markdown(
            f"<div class='section-header'>{L['enhanced_crop_health_header']}</div>",
            unsafe_allow_html=True,
        )
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.markdown(
                f"<div class='stat-card' style='border-color:{dashboard['risk_color']}'>"
                f"<h4>{L['disease_risk_label']}</h4>"
                f"<div class='val' style='color:{dashboard['risk_color']}'>{translate_enum(dashboard['risk_indicator'], lang)}</div>"
                f"</div>", unsafe_allow_html=True,
            )
        with d2:
            st.markdown(
                f"<div class='stat-card' style='border-color:{dashboard['recovery_color']}'>"
                f"<h4>{L['recovery_potential_label']}</h4>"
                f"<div class='val' style='color:{dashboard['recovery_color']}'>{translate_enum(dashboard['recovery_potential'], lang)}</div>"
                f"</div>", unsafe_allow_html=True,
            )
        with d3:
            st.markdown(
                f"<div class='stat-card'><h4>{L['ai_confidence_meter_label']}</h4>"
                f"<div class='val'>{dashboard['confidence_meter']}%</div></div>",
                unsafe_allow_html=True,
            )
        with d4:
            st.markdown(
                f"<div class='stat-card' style='border-color:{dashboard['leaf_quality_color']}'>"
                f"<h4>{L['leaf_quality_label']}</h4>"
                f"<div class='val' style='color:{dashboard['leaf_quality_color']}'>{translate_enum(dashboard['leaf_quality'], lang)}</div>"
                f"</div>", unsafe_allow_html=True,
            )
        st.info(f"🧾 {dashboard['ai_summary']}")

        st.markdown("---")

        # ── AI Explainability Report (Grad-CAM based) ───────────
        st.markdown(
            f"<div class='section-header'>🔍 {L['ai_explainability_report']}</div>",
            unsafe_allow_html=True,
        )
        if not explain["available"]:
            st.info(explain["explainability_summary"])
        else:
            e1, e2, e3 = st.columns(3)
            with e1:
                st.markdown(
                    f"<div class='stat-card'><h4>{L['disease_affected_area']}</h4>"
                    f"<div class='val'>{explain['disease_area_pct']}%</div></div>",
                    unsafe_allow_html=True,
                )
            with e2:
                st.markdown(
                    f"<div class='stat-card'><h4>{L['infection_location_label']}</h4>"
                    f"<div class='val' style='font-size:18px'>{explain['infection_location']}</div></div>",
                    unsafe_allow_html=True,
                )
            with e3:
                st.markdown(
                    f"<div class='stat-card'><h4>{L['attention_focus']}</h4>"
                    f"<div class='val' style='font-size:18px'>{explain['focus']['focus_label']}</div></div>",
                    unsafe_allow_html=True,
                )
            st.caption(f"{L['lesion_coverage_caption']}: {explain['lesion_coverage_label']}")
            st.markdown(f"**{L['why_predicted_label']}:** {explain['why_predicted']}")
            st.markdown(f"**{L['summary_label']}:** {explain['explainability_summary']}")
            st.markdown(f"**{L['confidence_interpretation_label']}:** {explain['confidence_interpretation']}")
            st.success(f"🌾 **{L['agricultural_interpretation_label']}:** {explain['agricultural_interpretation']}")

        st.markdown("---")

        # ── Advisory ───────────────────────────────────────────
        st.markdown(
            f"<div class='section-header'>🌱 {L['advisory']}</div>",
            unsafe_allow_html=True,
        )

        if lang == "english":
            # Single-column view — selected language IS English.
            (adv_col,) = st.columns(1)
            render_advisory_block(adv_col, adv_english, "english", "🇬🇧 English", L)
        else:
            # Two columns: the farmer's selected language, plus English
            # as a reliable reference (mirrors the original EN/TA layout,
            # generalised to any of the 11 supported languages).
            adv_col1, adv_col2 = st.columns([1, 1], gap="large")
            render_advisory_block(adv_col1, adv_selected, lang, f"🌐 {native_name(lang)}", L)
            render_advisory_block(adv_col2, adv_english, "english", "🇬🇧 English", L)

        st.markdown("---")

        # ── Treatment Effectiveness ──────────────────────────────
        st.markdown(
            f"<div class='section-header'>💊 {L['treatment_effectiveness_header']}</div>",
            unsafe_allow_html=True,
        )
        treat_rows = [{
            L["treatment_col_option"]:        translate_treatment_name(t["name"], lang),
            L["treatment_col_priority"]:      translate_enum(str(t["priority"]), lang),
            L["treatment_col_success_rate"]:  f"{t['success_rate']}%",
            L["treatment_col_recovery_time"]: t["recovery_days"],
            L["treatment_col_cost"]:          translate_enum(str(t["cost"]), lang),
            L["treatment_col_eco_friendly"]:  translate_enum(str(t["eco"]), lang),
            L["treatment_col_best_stage"]:    translate_treatment_stage(t["stage"], lang),
        } for t in treatment_data["treatments"]]
        st.dataframe(pd.DataFrame(treat_rows), use_container_width=True, hide_index=True)

        st.markdown("---")

        # ── PDF Report ─────────────────────────────────────────
        st.markdown(f"<div class='section-header'>📄 {L['report_section_title']}</div>", unsafe_allow_html=True)
        if st.button(f"📥 {L['download_pdf']}", type="primary"):
            with st.spinner(L["building_pdf"]):
                pdf_bytes = generate_pdf_report(
                    original_image=image,
                    gradcam_image=cam_img if gradcam_available else None,
                    disease=disease_display_name(label, lang),
                    confidence=confidence,
                    all_probs=all_probs,
                    severity=severity,
                    health_index=health,
                    advisory=adv_selected,
                    location=location,
                    farmer_name=farmer_name,
                    lang=lang,
                )
            st.download_button(
                label=L["pdf_click_save_btn"],
                data=pdf_bytes,
                file_name=f"paddy_report_{label.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )

    else:
        st.markdown(
            "<div style='text-align:center;padding:60px 20px;color:#888'>"
            "<div style='font-size:80px'>🌾</div>"
            f"<h3 style='color:#555'>{L['no_upload_title']}</h3>"
            f"<p>{L['supports_formats_caption']}</p>"
            "</div>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════
# PAGE: CHATBOT  — Guest + Admin
# ═══════════════════════════════════════════════════════════════
elif "💬 Chatbot" in page:

    st.markdown(f"<h2 style='color:#145a32'>💬 {L['chatbot']}</h2>", unsafe_allow_html=True)
    st.caption(L["chatbot_intro_caption"])

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append({"role": "bot", "text": chatbot_greeting(lang)})
        st.session_state.chat_greeting_lang = lang
    elif (
        len(st.session_state.chat_history) == 1
        and st.session_state.chat_history[0]["role"] == "bot"
        and st.session_state.get("chat_greeting_lang") != lang
    ):
        # Farmer switched language before sending their first message — the
        # only thing in the transcript so far is the auto-greeting, so
        # refresh it in place instead of leaving it stuck in the old
        # language. Real conversation turns are never rewritten.
        st.session_state.chat_history[0]["text"] = chatbot_greeting(lang)
        st.session_state.chat_greeting_lang = lang

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

    # Diagnosis context set by the Diagnosis page (blast, severity, etc.),
    # so the chatbot can answer "what should I do now?" without the farmer
    # repeating themselves. Empty until a scan has been run this session.
    diag_context = st.session_state.get("diagnosis_context")

    st.markdown(f"**{L['quick_questions_label']}**")
    quick = quick_questions(lang)
    qcols = st.columns(4 if len(quick) >= 4 else max(1, len(quick)))
    for i, q in enumerate(quick):
        with qcols[i % len(qcols)]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                with st.spinner(ui_text("chatbot_thinking", lang)):
                    response = smart_farming_bot(
                        q, lang=lang,
                        history=st.session_state.chat_history,
                        context=diag_context,
                    )
                st.session_state.chat_history.append({"role": "user", "text": q})
                st.session_state.chat_history.append({"role": "bot",  "text": response})
                st.rerun()

    user_query = st.text_input(
        L["ask"], key="chat_input",
        label_visibility="collapsed", placeholder=L["ask"],
    )
    send_col, clear_col = st.columns([4, 1])
    with send_col:
        if st.button(f"{L['send']} 📨", use_container_width=True) and user_query.strip():
            with st.spinner(ui_text("chatbot_thinking", lang)):
                response = smart_farming_bot(
                    user_query.strip(), lang=lang,
                    history=st.session_state.chat_history,
                    context=diag_context,
                )
            st.session_state.chat_history.append({"role": "user", "text": user_query.strip()})
            st.session_state.chat_history.append({"role": "bot",  "text": response})
            st.rerun()
    with clear_col:
        if st.button(f"{L['clear']} 🗑", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# PAGE: MODEL PERFORMANCE  — Guest + Admin (added feature)
# ═══════════════════════════════════════════════════════════════
elif "📊 Model Performance" in page:

    data = generate_research_data(lang)
    comparison_df = data["comparison_df"]
    col_existing, col_proposed, col_improve = data["col_existing"], data["col_proposed"], data["col_improve"]

    cap_data   = generate_model_capability_data(lang)
    dimensions = cap_data["dimensions"]
    cap_scores = cap_data["scores"]

    # ── Header ───────────────────────────────────────────────
    st.markdown(
        "<div class='perf-header'>"
        f"<h2>📊 {L['model_performance_title']}</h2>"
        f"<p>{L['model_performance_subtitle']}</p>"
        "<div class='perf-divider'></div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.caption(L["model_performance_caption"])

    # ═══════════════════════════════════════════════════════════
    # SECTION: CNN vs ResNet50 vs EfficientNetB0 (capability graph)
    # ═══════════════════════════════════════════════════════════
    st.markdown(f"<div class='section-header'>{L['cnn_resnet_effnet_header']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='section-sub'>{L['capability_comparison_subtitle']}</p>",
        unsafe_allow_html=True,
    )

    cap_fig = go.Figure()
    # Bold, saturated colour per model so CNN / ResNet50 / EfficientNetB0
    # are immediately separable, with EfficientNetB0 (Smart Paddy AI's
    # model) in the brightest, most eye-catching colour since it wins.
    # NOTE: model_name here is the DICT KEY from generate_model_capability_data
    # (stable "CNN (Baseline)" etc.) — NOT translated, since it's only used
    # internally for colour lookup and the trace legend name. Translating
    # legend names is a nice-to-have left for a future pass; the axis
    # categories (dimensions) — the part farmers actually read — are
    # already fully localized above.
    cap_colors = {
        "CNN (Baseline)":            "#ff9f43",   # warm orange
        "ResNet50 (Benchmark)":      "#8c7ae6",   # rich violet
        "EfficientNetB0 (Proposed)": "#05c46b",   # bright winning green
    }
    cap_line_colors = {
        "CNN (Baseline)":            "#c9700a",
        "ResNet50 (Benchmark)":      "#5b3fc9",
        "EfficientNetB0 (Proposed)": "#02853f",
    }
    for model_name, vals in cap_scores.items():
        cap_fig.add_trace(go.Bar(
            name=model_name,
            x=dimensions, y=vals,
            marker=dict(
                color=cap_colors[model_name],
                line=dict(color=cap_line_colors[model_name], width=1.8),
            ),
            text=[f"{v:.1f}" for v in vals],
            textposition="outside",
            textfont=dict(color=PALETTE["text"], size=13, family="Inter, sans-serif"),
        ))
    cap_fig.update_layout(
        # Explicitly keep this chart title empty. Without an explicit title
        # object, the renderer can display the literal word "undefined".
        title=dict(text=""),
        barmode="group",
        bargap=0.22,
        bargroupgap=0.1,
        yaxis_range=[0, 5.6],
        yaxis_title=L["capability_score_axis"],
    )
    style_fig(cap_fig, height=440)
    st.plotly_chart(cap_fig, use_container_width=True)
    st.caption(L["capability_chart_caption"])
    st.markdown(
        f"<div class='research-summary-box'>{L['verdict_box_html']}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════
    # SECTION: ACCURACY / PRECISION / RECALL / F1 COMPARISON TABLE
    # ═══════════════════════════════════════════════════════════
    st.markdown(f"<div class='section-header'>{L['accuracy_precision_recall_f1_header']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='section-sub'>{L['existing_vs_proposed_subtitle']}</p>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        comparison_df.style.format({
            col_existing: "{:.1f}",
            col_proposed: "{:.1f}",
            col_improve:  "+{:.1f}",
        }),
        use_container_width=True, hide_index=True,
    )

    # ── Conclusion ─────────────────────────────────────────────
    avg_existing = comparison_df[col_existing].mean()
    avg_proposed = comparison_df[col_proposed].mean()
    avg_gain     = avg_proposed - avg_existing
    st.markdown(
        "<div class='research-summary-box'>"
        + L["conclusion_box_template"].format(gain=avg_gain, proposed=avg_proposed, existing=avg_existing)
        + "</div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════
# PAGE: ANALYTICS  — Admin only
# ═══════════════════════════════════════════════════════════════
elif "📊 Analytics" in page:

    require_admin()

    st.markdown(f"<h2 style='color:#145a32'>📊 {L['analytics']}</h2>", unsafe_allow_html=True)

    preds = get_all_predictions()

    if not preds:
        st.info(L["upload_dashboard_info"])
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
            (s1, str(total),              L["total_scans_label"],         "#3498db"),
            (s2, most_common,             L["most_common_disease_label"], "#e74c3c"),
            (s3, f"{avg_conf:.1f}%",      L["avg_confidence_label"],      "#27ae60"),
            (s4, f"{avg_health:.0f}/100", L["avg_health_index_label"],    "#f39c12"),
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
            st.markdown(f"#### {L['disease_distribution_header']}")
            disease_counts         = df["disease"].value_counts().reset_index()
            disease_counts.columns = [L["col_disease"], L["col_count"]]
            fig_pie = px.pie(
                disease_counts, names=L["col_disease"], values=L["col_count"],
                color_discrete_sequence=["#27ae60","#e74c3c","#f39c12","#3498db","#9b59b6"],
                hole=0.35,
            )
            fig_pie.update_layout(height=320, margin=dict(l=0,r=0,t=20,b=0))
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.markdown(f"#### {L['scan_count_by_disease_header']}")
            fig_bar = px.bar(
                disease_counts, x=L["col_disease"], y=L["col_count"],
                color=L["col_disease"],
                color_discrete_sequence=["#27ae60","#e74c3c","#f39c12","#3498db"],
                text=L["col_count"],
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(height=320, margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown(f"#### {L['monthly_scan_trends_header']}")
        monthly = df.groupby("month").size().reset_index(name="count")
        fig_line = px.line(
            monthly, x="month", y="count",
            markers=True, line_shape="spline",
            color_discrete_sequence=["#27ae60"],
        )
        fig_line.update_layout(
            height=280, margin=dict(l=0,r=0,t=20,b=0),
            xaxis_title=L["month_axis_label"], yaxis_title=L["scans_axis_label"],
        )
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown(f"#### {L['severity_distribution_header']}")
        fig_hist = px.histogram(df, x="severity", nbins=20,
                                color_discrete_sequence=["#f39c12"])
        fig_hist.update_layout(height=250, margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown(f"#### {L['recent_predictions_header']}")
        disp               = df[["timestamp","disease","confidence","severity","health_idx"]].copy()
        disp["confidence"] = (disp["confidence"] * 100).round(1).astype(str) + "%"
        disp["severity"]   = disp["severity"].round(1).astype(str) + "%"
        disp["health_idx"] = disp["health_idx"].round(0).astype(int)
        disp.columns       = [
            L["col_timestamp"], L["col_disease"], L["col_confidence"],
            L["col_severity"], L["col_health_index"],
        ]
        st.dataframe(disp.head(20), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: RESEARCH METRICS  — Admin only
# ═══════════════════════════════════════════════════════════════
elif "📐 Research" in page:

    require_admin()

    st.markdown(f"<h2 style='color:#145a32'>📐 {L['research']}</h2>", unsafe_allow_html=True)
    st.caption(L["research_metrics_caption"])

    train_curves, saved_cm = load_training_plots()

    if train_curves:
        st.markdown(f"#### {L['training_curves_header']}")
        st.image(train_curves, use_container_width=True)

    if saved_cm:
        st.markdown(f"#### {L['confusion_matrix_header']}")
        st.image(saved_cm, use_container_width=True)

    st.markdown("---")
    st.markdown(f"#### {L['upload_eval_data_header']}")
    st.caption(L["csv_upload_caption"])

    eval_file = st.file_uploader(L["upload_eval_csv_label"], type=["csv"])

    if eval_file:
        eval_df = pd.read_csv(eval_file)
        if "true_label" not in eval_df.columns or "pred_label" not in eval_df.columns:
            st.error(L["csv_column_error"])
        else:
            all_cls = sorted(eval_df["true_label"].unique().tolist())
            cls_map = {c: i for i, c in enumerate(all_cls)}
            y_true  = eval_df["true_label"].map(cls_map).tolist()
            y_pred  = eval_df["pred_label"].map(cls_map).fillna(0).astype(int).tolist()

            cm_bytes = plot_confusion_matrix(y_true, y_pred, class_names=all_cls)
            st.image(cm_bytes, caption=L["eval_confusion_matrix_caption"], width=600)

            report = compute_classification_report(y_true, y_pred, class_names=all_cls)
            st.markdown(f"#### {L['overall_accuracy_label']}: **{report['accuracy']}%**")

            rep_rows = []
            for cls, m in report["per_class"].items():
                rep_rows.append({
                    L["eval_col_class"]:     cls,
                    L["eval_col_precision"]: f"{m['precision']}%",
                    L["eval_col_recall"]:    f"{m['recall']}%",
                    L["eval_col_f1"]:        f"{m['f1']}%",
                    L["eval_col_support"]:   m["support"],
                })
            st.dataframe(pd.DataFrame(rep_rows), use_container_width=True)

            mc, wc = st.columns(2)
            with mc:
                st.markdown(f"**{L['macro_average_label']}**")
                st.json(report["macro_avg"])
            with wc:
                st.markdown(f"**{L['weighted_average_label']}**")
                st.json(report["weighted_avg"])

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════
    # SECTION 1: CAPABILITY COMPARISON ACROSS THE THREE MODELS
    # ═══════════════════════════════════════════════════════════
    st.markdown(
        f"<div class='section-header'>{L['capability_comparison_full_title']}</div>",
        unsafe_allow_html=True,
    )

    cap_data   = generate_model_capability_data(lang)
    dimensions = cap_data["dimensions"]
    cap_scores = cap_data["scores"]

    cap_fig = go.Figure()
    # Bold, saturated colour per model so CNN / ResNet50 / EfficientNetB0
    # are immediately separable, with EfficientNetB0 (Smart Paddy AI's
    # model) in the brightest, most eye-catching colour since it wins.
    cap_colors = {
        "CNN (Baseline)":            "#ff9f43",   # warm orange
        "ResNet50 (Benchmark)":      "#8c7ae6",   # rich violet
        "EfficientNetB0 (Proposed)": "#05c46b",   # bright winning green
    }
    cap_line_colors = {
        "CNN (Baseline)":            "#c9700a",
        "ResNet50 (Benchmark)":      "#5b3fc9",
        "EfficientNetB0 (Proposed)": "#02853f",
    }
    for model_name, vals in cap_scores.items():
        cap_fig.add_trace(go.Bar(
            name=model_name,
            x=dimensions, y=vals,
            marker=dict(
                color=cap_colors[model_name],
                line=dict(color=cap_line_colors[model_name], width=1.8),
            ),
            text=[f"{v:.1f}" for v in vals],
            textposition="outside",
            textfont=dict(color=PALETTE["text"], size=13, family="Inter, sans-serif"),
        ))
    cap_fig.update_layout(
        title=dict(
            text=L["capability_comparison_full_title"],
            font=dict(family="Poppins, sans-serif", color=PALETTE["text"], size=16),
        ),
        barmode="group",
        bargap=0.22,
        bargroupgap=0.1,
        yaxis_range=[0, 5.6],
        yaxis_title=L["capability_score_axis_lower"],
    )
    style_fig(cap_fig, height=440)
    st.plotly_chart(cap_fig, use_container_width=True)

    st.caption(L["capability_models_caption"])

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════
    # SECTION 2: MODEL SELECTION RATIONALE
    # ═══════════════════════════════════════════════════════════
    st.markdown(
        "<div class='research-summary-box'>"
        f"<b>{L['why_effnet_selected_title']}</b><br><br>"
        f"{L['why_effnet_selected_body']}"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════
    # SECTION 3: ACCURACY, PRECISION, RECALL & F1 COMPARISON
    # ═══════════════════════════════════════════════════════════
    st.markdown(
        f"<div class='section-header'>{L['accuracy_precision_recall_f1_header']}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p class='section-sub'>{L['existing_vs_proposed_subtitle']}</p>",
        unsafe_allow_html=True,
    )

    perf_data     = generate_research_data(lang)   # same cached data source as the Model Performance page
    comparison_df = perf_data["comparison_df"]
    col_existing, col_proposed, col_improve = (
        perf_data["col_existing"], perf_data["col_proposed"], perf_data["col_improve"]
    )

    st.dataframe(
        comparison_df.style.format({
            col_existing: "{:.1f}",
            col_proposed: "{:.1f}",
            col_improve:  "+{:.1f}",
        }),
        use_container_width=True, hide_index=True,
    )

    avg_existing = comparison_df[col_existing].mean()
    avg_proposed = comparison_df[col_proposed].mean()
    avg_gain     = avg_proposed - avg_existing
    st.caption(
        ui_text("research_metrics_avg_gain_caption", lang,
                gain=avg_gain, proposed=avg_proposed, existing=avg_existing)
    )

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════
    # SECTION 4: FINAL PERFORMANCE CONCLUSION
    # ═══════════════════════════════════════════════════════════
    st.markdown(
        "<div class='research-summary-box'>"
        + ui_text("research_final_conclusion_template", lang,
                  gain=avg_gain, proposed=avg_proposed, existing=avg_existing)
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(f"#### {L['model_architecture_summary_header']}")
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
    info_rows = [{L["model_arch_param_col"]: k, L["model_arch_value_col"]: v} for k, v in model_info.items()]
    st.dataframe(pd.DataFrame(info_rows), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: ADMIN DASHBOARD  — Admin only
# ═══════════════════════════════════════════════════════════════
elif "👑 Admin Dashboard" in page:

    require_admin()

    st.markdown(f"<h2 style='color:#145a32'>{L['admin_dashboard_title']}</h2>", unsafe_allow_html=True)
    st.caption(L["admin_dashboard_caption"])
    st.markdown("---")

    log_df = load_pred_log()

    if log_df.empty:
        st.info(L["no_predictions_logged"])
    else:
        total       = len(log_df)
        unique_users = log_df["Username"].nunique()
        top_disease  = log_df["Predicted Disease"].value_counts().idxmax()

        a1, a2, a3 = st.columns(3)
        for col, val, label_text, color in [
            (a1, str(total),  L["admin_total_predictions_label"], "#3498db"),
            (a2, str(unique_users), L["admin_unique_users_label"],       "#27ae60"),
            (a3, top_disease,       L["admin_top_disease_label"],        "#e74c3c"),
        ]:
            with col:
                st.markdown(
                    f"<div class='stat-card' style='border-color:{color}'>"
                    f"<h4>{label_text}</h4><div class='val'>{val}</div></div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        ch1, ch2 = st.columns(2)

        with ch1:
            st.markdown(f"#### {L['predictions_by_disease_header']}")
            disease_counts         = log_df["Predicted Disease"].value_counts().reset_index()
            disease_counts.columns = [L["col_disease"], L["col_count"]]
            fig_bar = px.bar(
                disease_counts, x=L["col_disease"], y=L["col_count"],
                color=L["col_disease"],
                color_discrete_sequence=["#27ae60","#e74c3c","#f39c12","#3498db","#9b59b6"],
                text=L["col_count"],
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        with ch2:
            st.markdown(f"#### {L['scans_per_user_header']}")
            user_counts         = log_df["Username"].value_counts().reset_index()
            user_counts.columns = ["Username", "Scans"]
            fig_user = px.bar(
                user_counts, x="Username", y="Scans",
                color="Username",
                color_discrete_sequence=["#3498db","#27ae60","#f39c12","#e74c3c"],
                text="Scans",
            )
            fig_user.update_traces(textposition="outside")
            fig_user.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
            st.plotly_chart(fig_user, use_container_width=True)

        st.markdown(f"#### {L['recent_activity_header']}")
        st.dataframe(
            log_df.tail(10).iloc[::-1].reset_index(drop=True),
            use_container_width=True,
        )

        st.markdown("---")
        st.markdown(f"#### {ui_text('full_prediction_history_count', lang, total=total)}")
        st.dataframe(
            log_df.iloc[::-1].reset_index(drop=True),
            use_container_width=True,
        )
        csv_bytes_admin = log_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=L["download_full_log_btn"],
            data=csv_bytes_admin,
            file_name="paddy_predictions_log.csv",
            mime="text/csv",
            key="admin_dashboard_full_log_download",
        )


# ═══════════════════════════════════════════════════════════════
# PAGE: FULL HISTORY  — Admin only
# ═══════════════════════════════════════════════════════════════
elif "📋 Full History" in page:

    require_admin()

    st.markdown(f"<h2 style='color:#145a32'>{L['full_history_title']}</h2>", unsafe_allow_html=True)
    st.caption(L["full_history_caption"])
    st.markdown("---")

    log_df = load_pred_log()

    if log_df.empty:
        st.info(L["no_prediction_records"])
    else:
        all_users_label    = L["all_users_option"]
        all_diseases_label = L["all_diseases_option"]

        fc1, fc2 = st.columns(2)
        with fc1:
            all_users     = [all_users_label] + sorted(log_df["Username"].unique().tolist())
            selected_user = st.selectbox(L["filter_by_user"], all_users)
        with fc2:
            all_diseases     = [all_diseases_label] + sorted(log_df["Predicted Disease"].unique().tolist())
            selected_disease = st.selectbox(L["filter_by_disease"], all_diseases)

        filtered = log_df.copy()
        if selected_user != all_users_label:
            filtered = filtered[filtered["Username"] == selected_user]
        if selected_disease != all_diseases_label:
            filtered = filtered[filtered["Predicted Disease"] == selected_disease]

        st.markdown(ui_text("showing_records_of", lang, shown=len(filtered), total=len(log_df)))
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)

        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=L["download_filtered_log_btn"],
            data=csv_bytes,
            file_name="paddy_predictions_log.csv",
            mime="text/csv",
        )


# ═══════════════════════════════════════════════════════════════
# PADDYBUDDY — FLOATING MULTILINGUAL AI ASSISTANT  (added feature)
# ═══════════════════════════════════════════════════════════════
# Isolated, modular, and safe to remove: deleting this block plus the
# `from utils.paddy_buddy import ...` line near the top, and the three
# `st.session_state.pb_mood = "..."` lines in the Diagnosis page above,
# fully removes the feature without touching prediction, Grad-CAM,
# severity, advisory, logging, or any existing page.
#
# Rendered LAST and OUTSIDE the page routing if/elif chain so the
# character floats on top of every page (Diagnosis, Chatbot, Model
# Performance, and — for admins — Analytics/Research/Admin/History
# too), always reflecting the currently selected sidebar language.
render_paddy_buddy(lang, mood=st.session_state.get("pb_mood", "idle"))
# PaddyBuddy is intentionally launcher-only. The existing Farming
# Assistant page above is the single chatbot interface, so no duplicate
# floating chat panel is rendered here.
