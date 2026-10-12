"""Single-request Tavily connectivity test. No Gemini calls or automatic retries."""
import json
import os
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


def _key():
    key = os.environ.get("TAVILY_API_KEY", "").strip()
    if key:
        return key
    try:
        value = st.secrets.get("TAVILY_API_KEY", "")
    except (StreamlitSecretNotFoundError, FileNotFoundError):
        return None
    return value.strip() if isinstance(value, str) and value.strip() else None


def search_once(company: str, market: str, category: str) -> dict:
    """Execute exactly one basic search; return unverified source leads."""
    values = [str(v).strip() for v in (company, market, category)]
    if any(not value or len(value) > 100 for value in values):
        raise ValueError("Enter company, market and category (maximum 100 characters each).")
    key = _key()
    if not key:
        raise RuntimeError("TAVILY_API_KEY is missing from Streamlit Secrets.")
    company, market, category = values
    query = f"{company} {category} {market} official products company overview"
    payload = json.dumps({
        "query": query,
        "search_depth": "basic",
        "max_results": 5,
        "include_answer": False,
        "include_raw_content": False,
        "include_images": False,
    }).encode("utf-8")
    request = Request(
        "https://api.tavily.com/search",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=25) as response:
            data = json.load(response)
    except HTTPError as exc:
        if exc.code in (401, 403):
            message = "Tavily authentication or permission failed. Check the secret in Streamlit."
        elif exc.code == 429:
            message = "Tavily request limit reached. Check your Tavily dashboard; no automatic retry was made."
        else:
            message = f"Tavily returned HTTP {exc.code}. No results saved."
        raise RuntimeError(message) from None
    except (URLError, TimeoutError):
        raise RuntimeError("Tavily connection timed out or failed. No automatic retry was made.") from None
    except (ValueError, TypeError):
        raise RuntimeError("Tavily returned an invalid response.") from None

    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise RuntimeError("Tavily response had no usable results list.")
    sources = []
    seen = set()
    for item in data["results"][:5]:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url") or "")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc or url in seen:
            continue
        seen.add(url)
        sources.append({
            "title": str(item.get("title") or "Untitled source")[:200],
            "url": url,
            "snippet": str(item.get("content") or "")[:1500],
        })
    return {
        "status": "TAVILY SOURCE DISCOVERY — NOT VERIFIED",
        "query": query,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
        "note": "Search snippets and links are unverified leads, not verified findings. Gemini was not called.",
    }
