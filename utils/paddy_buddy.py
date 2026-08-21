"""
utils/paddy_buddy.py — Smart Paddy AI: PaddyBuddy Floating Assistant
Place at: smart_paddy_ai/utils/paddy_buddy.py

A self-contained, MODULAR add-on feature. Nothing in this file touches
the disease-detection model, prediction pipeline, Grad-CAM, severity
math, advisory content, database/logging, or any existing page layout.
It can be deleted (and its two call sites removed from app.py) without
affecting any other part of the application.

What this module provides
--------------------------
1. render_paddy_buddy(lang, mood, speech)
   A small floating cartoon paddy-farmer character (original design —
   an SVG built from scratch, not a photo, not a copyrighted mascot)
   pinned to the bottom-right corner of the viewport. It gently bobs,
   blinks, and waves on load. A speech bubble greets the farmer in the
   currently selected language. Clicking the character toggles the
   PaddyBuddy chat panel.

2. render_paddy_chat_panel(lang, diag_context, chat_fn)
   A compact floating chat panel (separate from the existing full
   "💬 Chatbot" page — this is only the quick-access popup version).
   It reuses the SAME Gemini-backed backend (utils/ai_expert.py ->
   smart_farming_bot) that the main Chatbot page already uses, and the
   SAME diagnosis-result context (st.session_state["diagnosis_context"])
   set by the Diagnosis page — it never predicts anything itself, it
   only reads the existing prediction the model already produced.

State used (all namespaced with a "pb_" prefix so it can never collide
with, or overwrite, any of the app's existing session_state keys):
    st.session_state.pb_open          : bool  — chat panel open/closed
    st.session_state.pb_history       : list  — this widget's own chat
                                                  log (kept separate from
                                                  the main Chatbot page's
                                                  st.session_state.chat_history
                                                  so the two never mix)
    st.session_state.pb_mood          : str   — current character mood
    st.session_state.pb_speech        : str   — current speech-bubble text
    st.session_state.pb_greeted_open  : bool  — whether the "chat opened"
                                                  greeting line has already
                                                  been appended this session

Requires Streamlit >= 1.31 for `st.container(key=...)` (used to get a
stable CSS hook for the floating position). If an older Streamlit is
detected, the character still renders — it just falls back to floating
in normal flow at the point it's called instead of a fixed corner
overlay (still isolated, still safe, just less polished positioning).
"""

from __future__ import annotations
import streamlit as st

from utils.i18n import ui_text, resolve_lang, quick_questions


# ═══════════════════════════════════════════════════════════════
# ONE-TIME CSS (animations + floating layout)
# ═══════════════════════════════════════════════════════════════
_CSS = """
<style>
@keyframes pb-float {
    0%, 100% { transform: translateY(0px); }
    50%      { transform: translateY(-6px); }
}
@keyframes pb-blink {
    0%, 92%, 100% { transform: scaleY(1); }
    96%           { transform: scaleY(0.1); }
}
@keyframes pb-wave {
    0%, 100% { transform: rotate(0deg); }
    25%      { transform: rotate(-18deg); }
    50%      { transform: rotate(4deg); }
    75%      { transform: rotate(-10deg); }
}
@keyframes pb-pop-in {
    0%   { opacity: 0; transform: translateY(8px) scale(0.95); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

/* Floating character dock — bottom-right, above everything, but small
   enough to never cover primary buttons/content. */
.st-key-paddybuddy_dock {
    position: fixed !important;
    right: 18px;
    bottom: 18px;
    z-index: 9999;
    width: 92px !important;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}
.pb-avatar-wrap {
    animation: pb-float 3.2s ease-in-out infinite;
    cursor: pointer;
    filter: drop-shadow(0 4px 10px rgba(20,90,50,0.28));
}
.pb-eye {
    animation: pb-blink 4.6s ease-in-out infinite;
    transform-origin: center;
}
.pb-wave-group {
    animation: pb-wave 1.6s ease-in-out 2;
    transform-origin: 70% 70%;
}
.pb-bubble {
    animation: pb-pop-in 0.35s ease-out;
    background: #ffffff;
    border: 1px solid #cdeccb;
    border-radius: 14px;
    padding: 8px 12px;
    font-size: 12.5px;
    line-height: 1.35;
    color: #1a3c1a !important;
    box-shadow: 0 6px 16px rgba(20,90,50,0.18);
    max-width: 190px;
    margin-bottom: 6px;
    text-align: right;
}

/* Floating chat panel */
.st-key-paddybuddy_panel {
    position: fixed !important;
    right: 18px;
    bottom: 118px;
    z-index: 9998;
    width: min(470px, calc(100vw - 36px)) !important;
    min-width: 360px !important;
    height: min(680px, calc(100vh - 150px)) !important;
    max-width: calc(100vw - 36px) !important;
    overflow: hidden;
    background: #fbfdf8;
    border: 1px solid #cdeccb;
    border-radius: 18px;
    box-shadow: 0 16px 42px rgba(20,90,50,0.32);
    padding: 16px 18px !important;
    animation: pb-pop-in 0.25s ease-out;
    color: #1a3c1a !important;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}
.st-key-pb_messages {
    flex: 1 1 auto;
    min-height: 0;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 2px 4px 8px 2px;
    scrollbar-width: thin;
    scrollbar-color: #b7d8bd transparent;
}
/* Everything text-based inside the panel defaults to a dark, readable
   colour — the panel itself is intentionally light so it stays legible
   and "cute" even though the rest of the app uses a dark theme. Without
   this, plain text (like the input label / paragraph text Streamlit
   renders inside markdown blocks) inherits the app's light/white text
   colour and becomes invisible on this light panel. */
.st-key-paddybuddy_panel, .st-key-paddybuddy_panel p,
.st-key-paddybuddy_panel span, .st-key-paddybuddy_panel label,
.st-key-paddybuddy_panel div {
    color: #1a3c1a;
}
.pb-panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 700;
    color: #145a32 !important;
    font-size: 14px;
    margin-bottom: 6px;
}
.pb-msg-user, .pb-msg-bot {
    display: block;
    box-sizing: border-box;
    padding: 10px 12px;
    border-radius: 12px;
    margin: 7px 0;
    font-size: 14px;
    line-height: 1.55;
    max-width: 92%;
    min-width: 0;
    white-space: pre-wrap !important;
    overflow-wrap: break-word !important;
    word-break: normal !important;
    writing-mode: horizontal-tb !important;
    overflow: visible;
}
.pb-msg-user {
    background: #e8f5e9;
    color: #1a3c1a !important;
    margin-left: auto;
    text-align: right;
}
.pb-msg-bot {
    background: #f1f1f1;
    color: #202020 !important;
    margin-right: auto;
}
/* Error replies (gemini_client._fallback_message strings all start with
   the ⚠️ glyph) get a distinct, still-readable amber treatment instead
   of blending in as a normal bot message. */
.pb-msg-error {
    background: #fff3e0;
    color: #7a3b00 !important;
    border: 1px solid #f3c98a;
    margin-right: auto;
}
.pb-suggestions-title {
    color: #145a32 !important;
    font-size: 13px;
    font-weight: 700;
    margin: 14px 0 7px;
}
.st-key-paddybuddy_panel button {
    white-space: normal !important;
    height: auto !important;
    min-height: 38px !important;
    line-height: 1.25 !important;
    overflow-wrap: break-word !important;
}

/* ── Streamlit widgets embedded in the panel (text input + buttons) ──
   These are real Streamlit widgets, not our own markdown/HTML, so they
   keep using the app's global (dark) theme colours unless scoped and
   overridden here. Scoped strictly to the PaddyBuddy panel/dock via the
   st-key-* container hooks Streamlit gives st.container(key=...) and
   keyed widgets — this does NOT touch the app's overall theme. */
.st-key-paddybuddy_panel input[type="text"],
.st-key-pb_input input[type="text"] {
    background: #ffffff !important;
    color: #1a3c1a !important;
    border: 1px solid #cdeccb !important;
    caret-color: #1a3c1a !important;
}
.st-key-paddybuddy_panel input[type="text"]::placeholder,
.st-key-pb_input input[type="text"]::placeholder {
    color: #6b8f6b !important;
    opacity: 1 !important;
}
.st-key-pb_send_btn button {
    background: #2d7a2d !important;
    color: #ffffff !important;
    border: 1px solid #2d7a2d !important;
    font-weight: 600;
}
.st-key-pb_send_btn button p { color: #ffffff !important; }
.st-key-pb_close_btn button {
    background: #ffffff !important;
    color: #1a3c1a !important;
    border: 1px solid #cdeccb !important;
}
.st-key-pb_close_btn button p { color: #1a3c1a !important; }
.st-key-paddybuddy_toggle_btn button {
    background: transparent !important;
    border: none !important;
}

@media (max-width: 520px) {
    .st-key-paddybuddy_dock  { width: 72px !important; right: 10px; bottom: 10px; }
    .st-key-paddybuddy_panel {
        width: calc(100vw - 20px) !important;
        min-width: 0 !important;
        max-width: calc(100vw - 20px) !important;
        height: calc(100vh - 118px) !important;
        right: 10px;
        bottom: 96px;
        padding: 12px !important;
    }
    .pb-msg-user, .pb-msg-bot { max-width: 96%; font-size: 14px; }
}
</style>
"""


def _character_svg(mood: str, waving: bool) -> str:
    """
    Build the PaddyBuddy SVG for a given mood. Original cartoon design —
    a round-faced little agricultural worker with a conical farmer hat,
    holding a paddy (rice) stalk. Facial expression changes per mood;
    everything else (hat, body, stalk) stays constant so the character
    reads as the same consistent mascot across states.
    """
    # Eyes / mouth per mood (all coordinates hand-tuned for the 120x120 canvas)
    if mood == "happy":
        eyes = (
            '<ellipse class="pb-eye" cx="46" cy="60" rx="4.2" ry="5.5" fill="#2d3436"/>'
            '<ellipse class="pb-eye" cx="74" cy="60" rx="4.2" ry="5.5" fill="#2d3436"/>'
        )
        mouth = '<path d="M45 72 Q60 86 75 72" stroke="#2d3436" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
    elif mood == "concerned":
        eyes = (
            '<ellipse class="pb-eye" cx="46" cy="61" rx="4" ry="5" fill="#2d3436"/>'
            '<ellipse class="pb-eye" cx="74" cy="61" rx="4" ry="5" fill="#2d3436"/>'
            '<path d="M40 53 Q46 49 52 53" stroke="#2d3436" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
            '<path d="M68 53 Q74 49 80 53" stroke="#2d3436" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
        )
        mouth = '<path d="M48 76 Q60 70 72 76" stroke="#2d3436" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
    elif mood == "curious":
        eyes = (
            '<ellipse class="pb-eye" cx="46" cy="59" rx="5" ry="6.4" fill="#2d3436"/>'
            '<ellipse class="pb-eye" cx="74" cy="59" rx="5" ry="6.4" fill="#2d3436"/>'
        )
        mouth = '<ellipse cx="60" cy="76" rx="6" ry="5" fill="#2d3436"/>'
    elif mood == "thinking":
        eyes = (
            '<path d="M41 60 L51 60" stroke="#2d3436" stroke-width="3.2" stroke-linecap="round"/>'
            '<ellipse class="pb-eye" cx="74" cy="59" rx="4.2" ry="5.5" fill="#2d3436"/>'
        )
        mouth = '<circle cx="60" cy="77" r="3.4" fill="#2d3436"/>'
    else:  # idle / default friendly face
        eyes = (
            '<ellipse class="pb-eye" cx="46" cy="60" rx="4.2" ry="5.5" fill="#2d3436"/>'
            '<ellipse class="pb-eye" cx="74" cy="60" rx="4.2" ry="5.5" fill="#2d3436"/>'
        )
        mouth = '<path d="M47 73 Q60 83 73 73" stroke="#2d3436" stroke-width="3.2" fill="none" stroke-linecap="round"/>'

    stalk_class = "pb-wave-group" if waving else ""

    return f'''
<svg viewBox="0 0 120 130" width="76" height="82" xmlns="http://www.w3.org/2000/svg">
  <!-- body -->
  <ellipse cx="60" cy="104" rx="34" ry="22" fill="#5fae5f"/>
  <ellipse cx="60" cy="100" rx="27" ry="16" fill="#79c479"/>
  <!-- head -->
  <circle cx="60" cy="62" r="38" fill="#f6c98a"/>
  <circle cx="42" cy="70" r="6.5" fill="#f2a86f" opacity="0.55"/>
  <circle cx="78" cy="70" r="6.5" fill="#f2a86f" opacity="0.55"/>
  <!-- conical farmer hat -->
  <path d="M18 40 Q60 -6 102 40 Q60 30 18 40 Z" fill="#d9a441"/>
  <path d="M14 42 Q60 26 106 42 L100 48 Q60 34 20 48 Z" fill="#c68f30"/>
  <!-- face -->
  {eyes}
  {mouth}
  <!-- little paddy (rice) stalk held to the side -->
  <g class="{stalk_class}">
    <line x1="94" y1="96" x2="106" y2="66" stroke="#3f8f4f" stroke-width="3.4" stroke-linecap="round"/>
    <ellipse cx="107" cy="60" rx="4.2" ry="7" fill="#e8d27a" transform="rotate(18 107 60)"/>
    <ellipse cx="112" cy="67" rx="4.2" ry="7" fill="#e8d27a" transform="rotate(35 112 67)"/>
    <ellipse cx="101" cy="66" rx="4.2" ry="7" fill="#f2df9a" transform="rotate(-5 101 66)"/>
  </g>
</svg>
'''


_DEFAULT_SPEECH_KEYS = {
    "idle":       "paddybuddy_greeting",
    "curious":    "paddybuddy_on_upload",
    "thinking":   "paddybuddy_analysing",
    "happy":      "paddybuddy_healthy",
    "concerned":  "paddybuddy_disease_found",
}


def render_paddy_buddy(lang: str = "english", mood: str | None = None, speech: str | None = None) -> None:
    """
    Render the floating PaddyBuddy character. Call this once per script
    run, anywhere in app.py (it positions itself via fixed CSS regardless
    of where in the page flow it's called from).

    Parameters
    ----------
    lang   : currently selected app language (utils.i18n key) — the
             speech bubble always follows this, never a separate
             in-widget language choice.
    mood   : one of "idle" | "curious" | "thinking" | "happy" | "concerned".
             Defaults to st.session_state.pb_mood (or "idle" the first
             time). Set by app.py at key moments (upload, analysing,
             healthy result, disease result) — see PART 7 of the spec.
    speech : optional explicit speech-bubble text (already localized).
             If omitted, a sensible default for the mood is looked up
             via utils.i18n (ui_text), so it always matches `lang`.
    """
    lang = resolve_lang(lang)
    mood = mood or st.session_state.get("pb_mood", "idle")
    st.session_state.pb_mood = mood

    if speech is None:
        key = _DEFAULT_SPEECH_KEYS.get(mood, "paddybuddy_greeting")
        speech = ui_text(key, lang)
    st.session_state.pb_speech = speech

    st.markdown(_CSS, unsafe_allow_html=True)

    is_open = st.session_state.get("pb_open", False)

    try:
        dock = st.container(key="paddybuddy_dock")
    except TypeError:
        # Older Streamlit without container(key=...) — degrade gracefully,
        # character still works, just isn't pinned to a fixed corner.
        dock = st.container()

    with dock:
        st.markdown(
            f'<div class="pb-bubble">{speech}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="pb-avatar-wrap">{_character_svg(mood, waving=not is_open)}</div>',
            unsafe_allow_html=True,
        )
        if st.button("🌾", key="paddybuddy_toggle_btn", help=ui_text("paddybuddy_panel_title", lang)):
            st.session_state.pb_open = not is_open
            if not is_open:
                # panel is being opened right now
                st.session_state.pb_mood = "idle"
                st.session_state.pb_greeted_open = False
            st.rerun()


def render_paddy_chat_panel(lang: str, diag_context: dict | None, chat_fn) -> None:
    """Render the responsive floating PaddyBuddy dialog using the existing chat backend."""
    if not st.session_state.get("pb_open", False):
        return

    lang = resolve_lang(lang)
    if "pb_history" not in st.session_state:
        st.session_state.pb_history = []

    if not st.session_state.get("pb_greeted_open", False):
        st.session_state.pb_history.append({"role": "bot", "text": ui_text("paddybuddy_chat_open", lang)})
        st.session_state.pb_greeted_open = True
        st.session_state.pb_greeting_lang = lang
    elif (
        len(st.session_state.pb_history) == 1
        and st.session_state.pb_history[0]["role"] == "bot"
        and st.session_state.get("pb_greeting_lang") != lang
    ):
        st.session_state.pb_history[0]["text"] = ui_text("paddybuddy_chat_open", lang)
        st.session_state.pb_greeting_lang = lang

    try:
        panel = st.container(key="paddybuddy_panel")
    except TypeError:
        panel = st.container()

    with panel:
        st.markdown(
            f'<div class="pb-panel-header">🌾 {ui_text("paddybuddy_panel_title", lang)}</div>',
            unsafe_allow_html=True,
        )

        try:
            messages_area = st.container(key="pb_messages")
        except TypeError:
            messages_area = st.container()
        with messages_area:
            for msg in st.session_state.pb_history[-20:]:
                text = msg.get("text", "")
                if msg.get("role") == "user":
                    cls, icon = "pb-msg-user", "👤"
                elif text.strip().startswith("⚠️"):
                    cls, icon = "pb-msg-error", "🌾"
                else:
                    cls, icon = "pb-msg-bot", "🌾"
                st.markdown(f'<div class="{cls}">{icon} {text}</div>', unsafe_allow_html=True)

            # Starter questions are suggestions only; arbitrary free-text remains
        # available through the input below and is sent to the same Gemini chat
        # backend with the full conversation context.
        if len(st.session_state.pb_history) == 1:
            st.markdown(
                f'<div class="pb-suggestions-title">{ui_text("quick_questions_label", lang)}</div>',
                unsafe_allow_html=True,
            )
            suggestions = quick_questions(lang)
            suggestion_cols = st.columns(2)
            for i, question in enumerate(suggestions[:8]):
                with suggestion_cols[i % 2]:
                    if st.button(question, key=f"pb_suggest_{i}", use_container_width=True):
                        with st.spinner(ui_text("chatbot_thinking", lang)):
                            reply = chat_fn(question, lang=lang, history=st.session_state.pb_history, context=diag_context)
                        st.session_state.pb_history.extend([
                            {"role": "user", "text": question},
                            {"role": "bot", "text": reply},
                        ])
                        st.rerun()

        query = st.text_input(
            ui_text("ask", lang),
            key="pb_input",
            label_visibility="collapsed",
            placeholder=ui_text("ask", lang),
        )
        send_col, close_col = st.columns([3, 1])
        with send_col:
            send = st.button(ui_text("send", lang), key="pb_send_btn", use_container_width=True)
        with close_col:
            close = st.button(ui_text("paddybuddy_close_btn", lang), key="pb_close_btn", use_container_width=True)

        if send and query.strip():
            with st.spinner(ui_text("chatbot_thinking", lang)):
                reply = chat_fn(query.strip(), lang=lang, history=st.session_state.pb_history, context=diag_context)
            st.session_state.pb_history.extend([
                {"role": "user", "text": query.strip()},
                {"role": "bot", "text": reply},
            ])
            st.rerun()

        if close:
            st.session_state.pb_open = False
            st.rerun()