"""Local, deterministic evidence processing; makes no network or AI requests."""
import re
from urllib.parse import urlparse

PROMO = re.compile(r"(?i)\b(?:buy now|shop now|subscribe|click here|limited time offer|sign up today)\b")
NUMERIC = re.compile(r"(?i)(?:\b\d[\d,.]*\s*(?:%|percent|crore|million|billion|products|stores|followers|years)\b|₹\s*\d[\d,.]*)")


def _clean(text):
    value = re.sub(r"\s+", " ", str(text or "")).strip()
    value = re.sub(r"(?i)\b(?:image\s*\d+|see more|read more)\b", " ", value)
    return re.sub(r"\s+", " ", value).strip()[:450]


def process_evidence(report):
    """Add transparent source heuristics and claim flags to saved Tavily results."""
    if not isinstance(report, dict) or not isinstance(report.get("sections"), list):
        raise ValueError("Run the five-topic research before processing evidence.")
    output = []
    for section in report["sections"]:
        entries = []
        for source in section.get("sources", []):
            url = str(source.get("url", ""))
            host = (urlparse(url).hostname or "").lower()
            title = _clean(source.get("title"))[:180]
            snippet = _clean(source.get("snippet"))
            if not host or not snippet:
                continue
            if host.endswith((".gov.in", ".gov", ".edu", ".ac.in")):
                source_type = "Government / academic domain"
            elif "linkedin.com" in host:
                source_type = "Professional / social platform"
            elif any(host.endswith(s) for s in (".youtube.com", "youtube.com", "instagram.com", "facebook.com")):
                source_type = "Social / video platform"
            else:
                source_type = "Website / publisher (unclassified)"
            flags = []
            if NUMERIC.search(snippet):
                flags.append("Contains numerical claim — verify against original")
            if PROMO.search(snippet):
                flags.append("Promotional wording — review")
            entries.append({
                "title": title,
                "url": url,
                "domain": host,
                "source_type": source_type,
                "clean_snippet": snippet,
                "review_flags": flags,
                "review_status": "NOT VERIFIED",
            })
        output.append({"topic": section.get("topic", "Unknown"), "sources": entries})
    return {
        "status": "PROCESSED EVIDENCE — NOT FACT-CHECKED",
        "scope": report.get("scope", {}),
        "retrieved_at_utc": report.get("retrieved_at_utc"),
        "sections": output,
        "source_count": sum(len(x["sources"]) for x in output),
        "method": "Whitespace/artifact cleanup, domain categorization, numeric/promotional flags. Domain categories do not establish credibility.",
    }
