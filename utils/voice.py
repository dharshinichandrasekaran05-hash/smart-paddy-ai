"""
utils/voice.py — Smart Paddy AI: Text-to-Speech
Place at: smart_paddy_ai/utils/voice.py

Uses gTTS to generate audio and plays it in Streamlit.
Strips markdown symbols before synthesis.

Supports all 11 languages registered in utils/i18n.py via speak(text, lang).
speak_tamil() / speak_english() are kept as thin wrappers around speak()
for backward compatibility with existing call sites.
"""

import re
import io
import streamlit as st
from gtts import gTTS
from gtts.lang import tts_langs

from utils.i18n import tts_code, resolve_lang, native_name

# gTTS accepts a "tld" for some accent variants; only English benefits from
# the .co.in accent used previously, so we special-case it and default to
# the plain "com" domain for every other language.
_TLD_OVERRIDES = {
    "english": "co.in",
}

# gTTS (Google Translate TTS) does not cover every language in our 11-language
# i18n list — as of this writing it has no Odia voice at all, regardless of
# language code used. Checked once at import time so speak() can give a
# clear, friendly message instead of a raw exception when that happens.
try:
    _GTTS_SUPPORTED_CODES = set(tts_langs().keys())
except Exception:
    # If the language list can't be fetched (e.g. no network), fall back to
    # attempting synthesis anyway and let the try/except in speak() handle it.
    _GTTS_SUPPORTED_CODES = None


def _clean_text(text: str) -> str:
    """Remove markdown symbols so TTS sounds natural."""
    text = re.sub(r"[*#_`~•→]", "", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def speak(text: str, lang: str = "english") -> None:
    """
    Generate TTS audio for any of the 11 supported languages and play it
    inline in Streamlit. Falls back to English gTTS code if the language
    key isn't recognised (resolve_lang / tts_code already handle that).
    """
    clean = _clean_text(text)
    if not clean:
        st.warning("No text to speak.")
        return

    lang = resolve_lang(lang)
    code = tts_code(lang)
    tld = _TLD_OVERRIDES.get(lang, "com")

    if _GTTS_SUPPORTED_CODES is not None and code not in _GTTS_SUPPORTED_CODES:
        st.warning(
            f"🔇 Voice playback isn't available in {native_name(lang)} yet — "
            f"Google's TTS engine doesn't support it. Showing English audio instead."
        )
        code = "en"
        tld = "co.in"

    try:
        tts = gTTS(text=clean, lang=code, tld=tld, slow=False)
    except Exception:
        # Some gTTS versions reject unknown tld/lang combos for certain
        # languages — retry with default tld before giving up.
        try:
            tts = gTTS(text=clean, lang=code, slow=False)
        except Exception as e:
            st.error(f"Could not generate audio for {native_name(lang)}.")
            st.exception(e)
            return

    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)

    st.audio(buf.read(), format="audio/mp3")


# ─── Backward-compatible wrappers (existing call sites keep working) ──────
def speak_tamil(text: str) -> None:
    """Generate Tamil TTS and play inline in Streamlit."""
    speak(text, "tamil")


def speak_english(text: str) -> None:
    """Generate English TTS and play inline in Streamlit."""
    speak(text, "english")
