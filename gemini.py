"""Gemini configuration only: API access is disabled for milestone one."""

import os

import streamlit as st
from google import genai
from streamlit.errors import StreamlitSecretNotFoundError

MODEL_ID = "gemini-3.5-flash-lite"
# Verified in Google's model documentation on 2026-10-10.
# https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite
API_REQUESTS_ENABLED = False


def get_api_key() -> str | None:
    """Read a key without printing it; environment takes precedence.

    No .env loader is installed. Missing or invalid Streamlit secrets are
    treated as unconfigured so the scaffold remains usable without a key.
    """
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except (StreamlitSecretNotFoundError, FileNotFoundError):
        return None
    if not isinstance(key, str):
        return None
    return key.strip() or None


def create_client() -> genai.Client:
    """Reserved for a later milestone; refuse client creation for now."""
    if not API_REQUESTS_ENABLED:
        raise RuntimeError("Gemini API access is disabled for this milestone.")
    key = get_api_key()
    if not key:
        raise ValueError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=key, vertexai=False)
