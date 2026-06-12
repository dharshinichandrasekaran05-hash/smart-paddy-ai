"""
utils/voice.py — Smart Paddy AI: Text-to-Speech
Place at: smart_paddy_ai/utils/voice.py

Uses gTTS to generate Tamil audio and plays it in Streamlit.
Strips markdown symbols before synthesis.
"""

import re
import io
import streamlit as st
from gtts import gTTS


def _clean_text(text: str) -> str:
    """Remove markdown symbols so TTS sounds natural."""
    text = re.sub(r"[*#_`~•→]", "", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def speak_tamil(text: str) -> None:
    """Generate Tamil TTS and play inline in Streamlit."""
    clean = _clean_text(text)
    if not clean:
        st.warning("No text to speak.")
        return

    tts = gTTS(text=clean, lang="ta", slow=False)

    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)

    st.audio(buf.read(), format="audio/mp3")


def speak_english(text: str) -> None:
    """Generate English TTS and play inline in Streamlit."""
    clean = _clean_text(text)
    if not clean:
        return

    tts = gTTS(text=clean, lang="en", tld="co.in", slow=False)

    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)

    st.audio(buf.read(), format="audio/mp3")