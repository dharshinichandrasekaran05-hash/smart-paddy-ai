"""
utils/ai_expert.py — Smart Paddy AI: Gemini-Powered Conversational Assistant
Place at: smart_paddy_ai/utils/ai_expert.py

Replaces the old rule-based keyword matcher with a real conversational AI
(Gemini) that:
  - Understands natural language, not just fixed keywords.
  - Maintains full conversation history (passed in from Streamlit
    session_state by the caller — this module stays state-free).
  - Answers follow-up questions using that history as context.
  - Automatically answers ONLY in the currently selected language, and
    never mixes languages.
  - Is automatically given the current diagnosis context (disease,
    confidence, severity, crop health index, recovery potential,
    treatment, prevention) so its answers are personalised, without the
    user having to repeat themselves.

utils/chatbot.py (the old, separate 4-disease rule-based bot) has been
removed — this module is now the single chatbot implementation.
"""

from __future__ import annotations
from utils.gemini_client import chat_reply, is_configured
from utils.i18n import native_name, resolve_lang, ui_text
from utils.advisory import get_advisory

_LANGUAGE_ENGLISH_NAMES = {
    "tamil": "Tamil", "telugu": "Telugu", "kannada": "Kannada",
    "malayalam": "Malayalam", "hindi": "Hindi", "bengali": "Bengali",
    "marathi": "Marathi", "gujarati": "Gujarati", "punjabi": "Punjabi",
    "odia": "Odia", "english": "English",
}


def _build_system_instruction(context: dict | None, lang: str) -> str:
    """
    Build the full system prompt sent to Gemini for every turn:
    persona + hard language rule + the farmer's current diagnosis context.
    """
    lang_name = _LANGUAGE_ENGLISH_NAMES.get(lang, lang.title())

    instruction = (
        "You are the Smart Paddy AI Assistant, a friendly and knowledgeable "
        "agricultural expert helping rice/paddy farmers in India. You give "
        "practical, safe, and specific advice on paddy cultivation, paddy and "
        "leaf diseases, symptoms, prevention, treatment, fertilizers, irrigation, "
        "water management, pests, soil, weather risks, disease spread, harvesting, "
        "crop protection, AI disease detection, confidence, severity, Grad-CAM, "
        "and the diagnosis context supplied by the application.\n\n"
        f"The user's currently selected application language is: {lang_name} ({lang}).\n"
        f"CRITICAL LANGUAGE RULE: You must answer ONLY in {lang_name}. "
        f"Do not mix in English or any other language, even for a single "
        f"word, unless the term is a widely-used technical acronym like "
        f"CNN, AI, PDF, NPK, or a scientific/chemical name that has no "
        f"native translation. Never switch languages mid-response.\n\n"
        "Understand natural wording, spelling variations, regional-language "
        "questions, and follow-up references such as 'it', 'this disease', or "
        "'that result' by using the conversation history and diagnosis context. "
        "Keep answers concise, well-structured (use short paragraphs or bullet "
        "points), and actionable. If a question is completely unrelated to "
        "paddy or agriculture, politely explain in the selected language that "
        "you are specialized in paddy farming and invite a crop-related question."
    )

    if context:
        ctx_lines = ["\nCURRENT DIAGNOSIS CONTEXT for this farmer's crop:"]
        if context.get("disease"):
            ctx_lines.append(f"- Detected Disease: {context['disease']}")
        if context.get("confidence") is not None:
            ctx_lines.append(f"- Prediction Confidence: {context['confidence']:.1f}%")
        if context.get("severity_label"):
            ctx_lines.append(
                f"- Severity: {context['severity_label']} "
                f"({context.get('severity_pct', '?')}%)"
            )
        if context.get("health_score") is not None:
            ctx_lines.append(
                f"- Crop Health Index: {context['health_score']}/100 "
                f"({context.get('health_category', '')})"
            )
        if context.get("recovery_potential"):
            ctx_lines.append(f"- Recovery Potential: {context['recovery_potential']}")
        if context.get("treatment"):
            ctx_lines.append(f"- Recommended Treatment: {context['treatment']}")
        if context.get("prevention"):
            ctx_lines.append(f"- Prevention Advice: {context['prevention']}")
        ctx_lines.append(
            "\nUse this context to personalise your answers whenever relevant "
            "(e.g. if the farmer asks 'what should I do now', refer back to "
            "this specific disease and severity instead of giving generic advice)."
        )
        instruction += "\n" + "\n".join(ctx_lines)

    return instruction


def smart_farming_bot(
    query: str,
    disease: str | None = None,
    lang: str = "english",
    history: list[dict] | None = None,
    context: dict | None = None,
) -> str:
    """
    Main chatbot entry point — now backed by Gemini instead of keyword rules.

    Parameters
    ----------
    query    : the farmer's new question
    disease  : predicted disease name from the model (kept for backward
               compatibility with old call sites; folded into `context`
               automatically if `context` isn't supplied separately)
    lang     : one of the 11 supported language keys from utils/i18n.py
    history  : prior turns as [{"role": "user"|"bot", "text": str}, ...]
               (pass st.session_state.chat_history straight in)
    context  : optional richer diagnosis context dict — see
               _build_system_instruction() for supported keys. If omitted
               but `disease` is given, a minimal context is built from it.

    Returns
    -------
    The assistant's reply as a plain string, already in the requested
    language.
    """
    lang = resolve_lang(lang)

    if context is None and disease:
        context = {"disease": disease}

    system_instruction = _build_system_instruction(context, lang)

    # Convert the Streamlit-style {"role": "user"/"bot", "text": ...} log
    # into Gemini's {"role": "user"/"model", "text": ...} shape, and drop
    # the initial greeting turn (it isn't a real exchange).
    gemini_history = []
    if history:
        for turn in history:
            role = "user" if turn.get("role") == "user" else "model"
            gemini_history.append({"role": role, "text": turn.get("text", "")})

    reply = chat_reply(system_instruction, gemini_history, query, lang=lang)
    if reply:
        return reply
    return _local_paddy_fallback(query, lang, context)


_DISEASE_TERMS = {
    "blast": "blast", "பிளாஸ்ட்": "blast", "ब्लास्ट": "blast", "బ్లాస్ట్": "blast",
    "brown spot": "brown spot", "பழுப்பு": "brown spot", "भूरा": "brown spot",
    "tungro": "tungro", "டங்க்ரோ": "tungro", "टुंग्रो": "tungro",
    "bacterial leaf blight": "bacterial leaf blight", "இலை அழுகல்": "bacterial leaf blight",
}


def _local_paddy_fallback(query: str, lang: str, context: dict | None) -> str:
    """Answer common Paddy questions locally when both remote providers fail."""
    text = (query or "").lower()
    disease = (context or {}).get("disease")
    disease_key = None
    for term, key in _DISEASE_TERMS.items():
        if term in text:
            disease_key = key
            break
    if not disease_key and disease:
        disease_key = str(disease).lower()
    if disease_key:
        try:
            advice = get_advisory(disease_key, lang)
            parts = [advice.get("description", "")]
            if any(word in text for word in ("treat", "சிகிச்சை", "उपचार", "చికిత్స", "treatment")):
                parts.append("\n".join(advice.get("treatment", [])))
            elif any(word in text for word in ("prevent", "தடுப்பு", "रोक", "నివారణ", "prevention")):
                parts.append("\n".join(advice.get("prevention", [])))
            else:
                parts.extend([advice.get("fertilizer", ""), advice.get("irrigation", "")])
            return "🌾 " + "\n".join(p for p in parts if p)
        except Exception:
            pass
    crop_terms = ("paddy", "rice", "crop", "disease", "leaf", "धान", "நெல்", "వరి", "ಭತ್ತ", "നെല്ല്", "ধান", "भात", "ડાંગર", "ਝੋਨਾ", "ଧାନ")
    if any(term in text for term in crop_terms) or (context and context.get("disease")):
        return ui_text("chatbot_service_unavailable", lang)
    return ui_text("chatbot_offtopic", lang)


def _not_configured_message(lang: str) -> str:
    return ui_text("chatbot_service_unavailable", lang)
