"""Five-topic Tavily research, capped at five basic requests per explicit run."""
from datetime import datetime, timezone
from tavily_search import search_once, _key
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

TOPICS = (
    ("Company & products", "official website company products portfolio"),
    ("Competitors", "competing brands alternative products"),
    ("Market & industry", "industry category consumer trends news"),
    ("Digital presence", "official website social media online channels"),
    ("Brand positioning", "brand positioning target customers differentiation messaging"),
)


def run_research(company: str, market: str, category: str) -> dict:
    values = [str(v).strip() for v in (company, market, category)]
    if any(not v or len(v) > 100 for v in values):
        raise ValueError("Enter company, market and category (up to 100 characters each).")
    key = _key()
    if not key:
        raise RuntimeError("TAVILY_API_KEY is missing from Streamlit Secrets.")
    company, market, category = values
    sections, seen, errors = [], set(), []
    attempted = 0
    for title, suffix in TOPICS:
        query = f"{company} {category} {market} {suffix}"
        payload = json.dumps({
            "query": query, "search_depth": "basic", "max_results": 5,
            "include_answer": False, "include_raw_content": False,
            "include_images": False,
        }).encode("utf-8")
        request = Request(
            "https://api.tavily.com/search", data=payload, method="POST",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        attempted += 1
        try:
            with urlopen(request, timeout=25) as response:
                data = json.load(response)
            if not isinstance(data, dict) or not isinstance(data.get("results"), list):
                raise ValueError("Unexpected response format")
        except HTTPError as exc:
            errors.append(f"{title}: Tavily HTTP {exc.code}.")
            if exc.code in (401, 403, 429):
                errors.append("Stopped remaining searches due to access or quota restriction.")
                break
            continue
        except (URLError, TimeoutError, ValueError, TypeError):
            errors.append(f"{title}: request failed or response invalid.")
            continue
        sources = []
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
        sections.append({"topic": title, "query": query, "sources": sources})
    return {
        "status": "AUTOMATED SOURCE DISCOVERY — NOT VERIFIED",
        "scope": {"company": company, "market": market, "category": category},
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "requests_attempted": attempted,
        "maximum_requests": len(TOPICS),
        "unique_sources": len(seen),
        "sections": sections,
        "errors": errors,
        "note": "Results are unverified search snippets. Gemini was not called. This report is stored only in the current Streamlit session until downloaded.",
    }
