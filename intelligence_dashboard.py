"""Read-only presentation helpers for the existing Gemini report; no API calls."""
import re

SECTIONS = (
    ("Brand overview", "Brand overview"),
    ("Competitor landscape", "Competitor landscape"),
    ("Market insights", "Market insights"),
    ("Digital presence", "Digital presence"),
    ("Strategic recommendations", "Strategic recommendations"),
    ("Evidence gaps", "Evidence gaps"),
)


def split_report(markdown):
    """Split on expected Markdown headings; preserve all text if format varies."""
    lines = str(markdown or "").splitlines()
    output = {name: [] for name, _ in SECTIONS}
    output["Other analysis"] = []
    current = "Other analysis"
    for line in lines:
        candidate = re.sub(r"^\s*#{1,6}\s*", "", line).strip().rstrip(":")
        candidate = re.sub(r"\*\*", "", candidate).strip().lower()
        match = next((name for name, _ in SECTIONS if candidate == name.lower()), None)
        if match and (line.lstrip().startswith("#") or line.strip().startswith("**")):
            current = match
        else:
            output[current].append(line)
    return {key: "\n".join(value).strip() for key, value in output.items()}


def citations_for(text, sources):
    valid = {str(source.get("id")) for source in sources}
    used = re.findall(r"\[S\d+\]", text or "")
    return sorted({ref[1:-1] for ref in used if ref[1:-1] in valid}, key=lambda ref: int(ref[1:]))


def coverage(analysis):
    sections = analysis.get("sources", [])
    by_topic = {}
    for source in sections:
        topic = str(source.get("topic", "Unknown"))
        by_topic[topic] = by_topic.get(topic, 0) + 1
    return by_topic
