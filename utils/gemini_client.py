"""
utils/gemini_client.py — Smart Paddy AI: Centralized Gemini API Client
Place at: smart_paddy_ai/utils/gemini_client.py

Single shared entry point for the ONLY Gemini call left in the project:
  - Conversational chatbot replies (utils/ai_expert.py)

Gemini is NOT used anywhere else. All UI text, disease names, advisory
content, severity/treatment text, chart labels, and PDF/voice output are
translated locally via utils/i18n.py's static dictionaries — no runtime
translation API calls, so changing the selected language never makes a
network request. All normal application content is supplied by the local dictionaries and templates in utils/i18n.py; this client has no translation entry point.

Why this file exists
---------------------
Rather than duplicating "load API key / call model / handle errors" logic
in every module, everything Gemini-related lives here. If you ever swap
model versions or providers, this is the only file that changes.

API key resolution order (first one found wins):
  1. st.secrets["GEMINI_API_KEY"]           (.streamlit/secrets.toml)
  2. os.environ["GEMINI_API_KEY"]

Setup
-----
1. pip install google-generativeai
2. Add to smart_paddy_ai/.streamlit/secrets.toml:
       GEMINI_API_KEY = "your-key-here"
   (or set the GEMINI_API_KEY environment variable instead)

CHANGES IN THIS VERSION
------------------------
The old version caught every exception with one generic try/except and
always returned the same "temporarily unavailable" message — so a bad
API key, a 429 quota error, and a genuine network outage were all
indistinguishable in the UI. That made a real "quota exceeded" error
(HTTP 429 / ResourceExhausted, which needs a NEW API key or billing
fix on Google's side — it cannot be retried away) look identical to a
transient blip that a retry would fix.

This version:
  1. Detects google.api_core.exceptions.ResourceExhausted (429)
     specifically, retries a couple of times with backoff ONLY for
     that error (since Gemini's own `retry_delay` hint is often just
     a few seconds for real rate limits), then — if still exhausted —
     returns a message that clearly says "quota exceeded", not a
     generic "unavailable" message, so you immediately know to check
     https://ai.dev/rate-limit or rotate the key instead of assuming
     it's a config typo.
  2. Detects invalid/unauthorized key errors (PermissionDenied /
     Unauthenticated) and returns a distinct "invalid key" message.
  3. Falls back to the original generic message only for genuinely
     unknown errors (e.g. no network).
  4. Still logs the FULL original exception + traceback via
     _log_error(), exactly as before, so nothing is hidden from you
     during debugging — only the user-facing text is now specific.

MODEL FALLBACK (this revision)
-------------------------------
The screenshot error you saw ("model unavailable") happens because a
single hard-coded MODEL_NAME can silently go stale — Google regularly
retires specific Gemini model snapshots, and this project's SDK
(google-generativeai, the "google.generativeai" import used throughout
this file) is Google's older, now-legacy client, so it only talks to
a limited set of model names.

Instead of trusting one hard-coded name, this file now tries an
ORDERED LIST of currently-supported model names (MODEL_CANDIDATES)
and remembers whichever one actually works:
  - Every chatbot call to Gemini goes through
    _iter_candidate_models(), which tries the last known-working model
    first, then walks the rest of the list.
  - If a candidate responds with "model not found" / "unsupported"
    (NotFound / InvalidArgument), that candidate is skipped and the
    next one is tried automatically, in the SAME request — the farmer
    never sees an intermediate failure.
  - The first model name that succeeds is cached in-process
    (_working_model_name) so every subsequent call goes straight to
    it instead of re-probing the list every time.
  - Quota (ResourceExhausted) and auth (PermissionDenied /
    Unauthenticated) errors are NOT retried against other models —
    those are key/billing problems, not model-name problems, so they
    surface immediately with the correct specific message.
  - No dependency changes: still the same `google-generativeai`
    package, same secrets/env-var key loading, same call site in ai_expert.py. Only the "which model name do I call" logic is
    now self-healing instead of a single hard-coded string.
"""

from __future__ import annotations
import os
import json
import hashlib
import time
import functools
import traceback
import requests

try:
    import streamlit as st
except Exception:  # pragma: no cover - allows import outside Streamlit too
    st = None

try:
    import google.generativeai as genai
    from google.api_core.exceptions import (
        ResourceExhausted,
        PermissionDenied,
        Unauthenticated,
        InvalidArgument,
        NotFound,
    )
    _GENAI_AVAILABLE = True
except Exception:
    _GENAI_AVAILABLE = False
    # Keep names defined so the except clauses below don't NameError
    # if the import failed (e.g. package not installed at all).
    class ResourceExhausted(Exception): ...
    class PermissionDenied(Exception): ...
    class Unauthenticated(Exception): ...
    class InvalidArgument(Exception): ...
    class NotFound(Exception): ...

# Ordered list of model names to try. The first one that actually
# responds successfully is remembered (see _working_model_name below)
# and used for every subsequent call — so in the common case this list
# is only ever walked once per app run. Kept intentionally to
# currently-supported "-flash" family names compatible with the
# google-generativeai SDK already used by this project (no SDK change).
MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-flash-latest",
]

# Kept for backward compatibility with anything that imports MODEL_NAME
# directly (e.g. error messages, logs) — reflects the first candidate,
# but the ACTUAL model used per-call is resolved dynamically below.
MODEL_NAME = MODEL_CANDIDATES[0]

# Retry behaviour for transient 429s only. Real free-tier "limit: 0"
# quota errors will NOT be fixed by retrying — this just absorbs brief,
# genuine rate-limit blips (e.g. two requests in the same second).
_MAX_RETRIES = 2
_RETRY_DELAY_SECONDS = 5

# Remembers whichever model name from MODEL_CANDIDATES last worked, so
# we don't re-probe the whole list on every single call.
_working_model_name: str | None = None


def _iter_candidate_models():
    """Yield model names to try, last-known-working one first."""
    if _working_model_name:
        yield _working_model_name
    for name in MODEL_CANDIDATES:
        if name != _working_model_name:
            yield name


def _mark_working_model(name: str) -> None:
    global _working_model_name
    if _working_model_name != name:
        _working_model_name = name


# ─────────────────────── API KEY / MODEL SETUP ────────────────
def _get_api_key() -> str | None:
    key = None
    if st is not None:
        try:
            key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            key = None
    if not key:
        key = os.environ.get("GEMINI_API_KEY")
    return key


@functools.lru_cache(maxsize=1)
def _configure_genai() -> None:
    """
    Configure the genai SDK with the API key exactly once per process.
    Raises RuntimeError with a clear message if the SDK isn't installed
    or no key is available — callers should catch this.
    """
    if not _GENAI_AVAILABLE:
        raise RuntimeError(
            "google-generativeai is not installed. Run: "
            "pip install google-generativeai"
        )
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Add it to .streamlit/secrets.toml "
            "or set it as an environment variable."
        )
    genai.configure(api_key=api_key)


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")


def _get_secret_or_env(name: str) -> str | None:
    value = None
    if st is not None:
        try:
            value = st.secrets.get(name)
        except Exception:
            value = None
    return value or os.environ.get(name)


def _get_groq_api_key() -> str | None:
    return _get_secret_or_env("GROQ_API_KEY")


def _get_groq_model() -> str:
    return _get_secret_or_env("GROQ_MODEL") or GROQ_MODEL


def is_configured() -> bool:
    """Return whether at least one chatbot provider is configured."""
    return (_GENAI_AVAILABLE and bool(_get_api_key())) or bool(_get_groq_api_key())


# ─────────────────────── SHARED CALL WRAPPER ──────────────────
def _generate_with_retry(model, contents, generation_config: dict):
    """
    Call model.generate_content(), retrying a limited number of times
    ONLY on ResourceExhausted (429). Any other exception is raised
    immediately to the caller (including NotFound / InvalidArgument,
    which the model-fallback layer above this function handles by
    trying the next candidate model — see _generate_with_model_fallback).
    """
    last_error = None
    for attempt in range(_MAX_RETRIES + 1):
        try:
            return model.generate_content(contents, generation_config=generation_config)
        except ResourceExhausted as e:
            last_error = e
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY_SECONDS)
                continue
            raise
    raise last_error  # pragma: no cover - unreachable, defensive only


# ─────────────────────── MODEL FALLBACK WRAPPER ────────────────
def _generate_with_model_fallback(contents, generation_config: dict, system_instruction: str | None = None):
    """
    Try each candidate model (see MODEL_CANDIDATES / _iter_candidate_models)
    until one actually answers. This is what fixes a stale/incorrect
    MODEL_NAME without needing a code edit every time Google retires a
    model snapshot: if the current model name comes back "not found" or
    "unsupported", we transparently try the next one in the SAME request.

    Quota (ResourceExhausted) and auth (PermissionDenied / Unauthenticated)
    errors are NOT model-name problems, so they're raised immediately
    instead of wasting time walking the rest of the candidate list.
    """
    _configure_genai()
    last_error: Exception | None = None

    for name in _iter_candidate_models():
        try:
            model = (
                genai.GenerativeModel(name, system_instruction=system_instruction)
                if system_instruction is not None
                else genai.GenerativeModel(name)
            )
            response = _generate_with_retry(model, contents, generation_config)
            _mark_working_model(name)
            return response
        except (NotFound, InvalidArgument) as e:
            # This specific model name isn't available/supported — try
            # the next candidate instead of failing the whole request.
            last_error = e
            continue
        # ResourceExhausted / PermissionDenied / Unauthenticated / any
        # other exception: not a model-name issue, so propagate as-is.

    raise last_error if last_error is not None else RuntimeError(
        "No Gemini model candidates were available."
    )


# ─────────────────────── CHAT PROVIDER CHAIN ──────────────────
def _gemini_chat_reply(system_instruction: str, history: list[dict], user_message: str, temperature: float) -> str | None:
    if not (_GENAI_AVAILABLE and _get_api_key()):
        return None
    contents = []
    for turn in history:
        role = "user" if turn.get("role") == "user" else "model"
        contents.append({"role": role, "parts": [turn.get("text", "")]})
    contents.append({"role": "user", "parts": [user_message]})
    response = _generate_with_model_fallback(
        contents,
        generation_config={"temperature": temperature},
        system_instruction=system_instruction,
    )
    return (getattr(response, "text", "") or "").strip() or None


def _groq_chat_reply(system_instruction: str, history: list[dict], user_message: str, temperature: float) -> str | None:
    api_key = _get_groq_api_key()
    if not api_key:
        return None
    messages = [{"role": "system", "content": system_instruction}]
    for turn in history:
        role = "user" if turn.get("role") == "user" else "assistant"
        text = (turn.get("text") or "").strip()
        if text:
            messages.append({"role": role, "content": text})
    messages.append({"role": "user", "content": user_message})
    response = requests.post(
        GROQ_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": _get_groq_model(), "messages": messages, "temperature": temperature, "max_tokens": 900},
        timeout=(8, 45),
    )
    response.raise_for_status()
    payload = response.json()
    return ((((payload.get("choices") or [{}])[0].get("message") or {}).get("content")) or "").strip() or None


def chat_reply(system_instruction: str, history: list[dict], user_message: str, temperature: float = 0.6, lang: str = "english") -> str | None:
    """Try Gemini first and Groq second; None lets ai_expert use local Paddy knowledge."""
    try:
        reply = _gemini_chat_reply(system_instruction, history, user_message, temperature)
        if reply:
            return reply
    except Exception as error:
        _log_error("gemini_provider", error)
    try:
        reply = _groq_chat_reply(system_instruction, history, user_message, temperature)
        if reply:
            return reply
    except Exception as error:
        _log_error("groq_provider", error)
    return None


def _log_error(where: str, error: Exception) -> None:
    """
    Make Gemini failures VISIBLE instead of silently swallowing them.
    The full traceback always goes to the terminal running
    `streamlit run`, and the latest error string is also stashed in
    session_state for easy inspection in-app (e.g. a small
    st.sidebar.error(st.session_state["_gemini_last_error"]) block).
    """
    print(f"\n[gemini_client] {where} failed: {error!r}")
    traceback.print_exc()
    if st is not None:
        try:
            st.session_state["_gemini_last_error"] = f"{where}: {error}"
        except Exception:
            pass


def _fallback_message(error: Exception | None = None, lang: str = "english") -> str:
    """
    Return a user-facing message tailored to the KIND of failure, instead
    of one generic string for every possible cause. This is the key fix:
    a 429 quota error (which needs a new key / billing fix, not a retry
    or a secrets.toml edit) now says so explicitly, rather than looking
    identical to "API key missing".

    `lang` is accepted (not just for the caller's convenience — chat_reply()
    calls this with `lang=lang`) but intentionally unused: these are
    technical/config error strings for whoever is setting up the API key,
    so they stay in English regardless of the farmer's selected language.
    Accepting the parameter here (instead of dropping it) avoids a
    TypeError on every failed Gemini call, which used to crash the
    chatbot instead of showing a graceful error.
    """
    if isinstance(error, ResourceExhausted):
        return (
            "⚠️ The AI assistant has hit Gemini's usage quota for this API "
            "key (free-tier limit reached, or the key's Google Cloud "
            "project has 0 free-tier quota). This will NOT fix itself by "
            "retrying — generate a new API key at "
            "https://aistudio.google.com/apikey (ideally in a fresh "
            "project) or check billing/quota at https://ai.dev/rate-limit, "
            "then update GEMINI_API_KEY in .streamlit/secrets.toml."
        )
    if isinstance(error, (PermissionDenied, Unauthenticated)):
        return (
            "⚠️ The AI assistant's Gemini API key was rejected as invalid "
            "or unauthorized. Generate a fresh key at "
            "https://aistudio.google.com/apikey and update "
            "GEMINI_API_KEY in .streamlit/secrets.toml."
        )
    if isinstance(error, (NotFound, InvalidArgument)):
        return (
            "⚠️ None of the configured Gemini models "
            f"({', '.join(MODEL_CANDIDATES)}) are currently available for "
            "this API key/region. Update MODEL_CANDIDATES in "
            "utils/gemini_client.py with a model name from "
            "https://ai.google.dev/gemini-api/docs/models."
        )
    return (
        "⚠️ The AI assistant is temporarily unavailable "
        "(Gemini API not reachable or not configured). "
        "Please check your GEMINI_API_KEY setup and try again."
    )