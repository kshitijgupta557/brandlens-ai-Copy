"""Minimal, manually triggered Gemini connectivity test for BrandLens AI."""
import os
import streamlit as st
from google import genai
from streamlit.errors import StreamlitSecretNotFoundError

MODEL_ID = "gemini-3.5-flash-lite"
API_REQUESTS_ENABLED = True  # Only the explicit test button invokes the API.


def get_api_key() -> str | None:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except (StreamlitSecretNotFoundError, FileNotFoundError):
        return None
    return key.strip() or None if isinstance(key, str) else None


def create_client() -> genai.Client:
    if not API_REQUESTS_ENABLED:
        raise RuntimeError("Gemini requests are disabled.")
    key = get_api_key()
    if not key:
        raise ValueError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=key, vertexai=False)


def test_connection() -> str:
    """Exactly one generate_content request; never return raw exception details."""
    if not API_REQUESTS_ENABLED:
        return "Gemini requests are disabled."
    if not get_api_key():
        return "No Gemini API key found in Streamlit Secrets."
    try:
        with create_client() as client:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents="Reply with exactly: BrandLens connection successful",
            )
        if "BrandLens connection successful" in (response.text or ""):
            return "Connection successful. Gemini returned the expected response."
        return "Gemini responded, but the response did not match the expected test phrase."
    except Exception:
        return "Connection failed. Check your model availability, free-tier quota, API key and Streamlit logs. Details are hidden to protect credentials."
