"""Export an evidence-traceable Markdown brand intelligence report without API calls."""
from datetime import datetime, timezone
from urllib.parse import urlparse
from intelligence_dashboard import SECTIONS, split_report, citations_for, coverage

TOPICS = ("Company & products", "Competitors", "Market & industry", "Digital presence", "Brand positioning")


def build_intelligence_report(analysis):
    if not isinstance(analysis, dict) or not analysis.get("report_markdown"):
        raise ValueError("Generate a Gemini evidence analysis before exporting a report.")
    scope = analysis.get("scope") or {}
    company = str(scope.get("company") or "Unspecified brand")
    market = str(scope.get("market") or "Not specified")
    category = str(scope.get("category") or "Not specified")
    sources = analysis.get("sources") or []
    sections = split_report(analysis["report_markdown"])
    counts = coverage(analysis)
    generated = str(analysis.get("generated_at_utc") or "Unknown")
    exported = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = [
        f"# Brand Intelligence Report — {company}",
        "",
        "**Status:** AI interpretation of unverified public search snippets; not independently fact-checked.",
        f"**Scope:** {company} | {market} | {category}",
        f"**AI analysis generated:** {generated}",
        f"**Report exported:** {exported}",
        "",
        "## Executive summary",
        "",
        "This report organizes previously generated Gemini analysis of Tavily search snippets. "
        "It does not establish factual accuracy, market share, sentiment, or numerical brand performance.",
        "",
    ]
    for name in ("Brand overview", "Competitor landscape", "Market insights", "Strategic recommendations"):
        body = sections.get(name, "").strip()
        first = body.split("\n\n")[0].strip() if body else "Insufficient evidence."
        out.extend([f"### {name}", "", first, ""])
    out.extend(["## Evidence coverage", "", "| Research topic | Collected snippets | Assessment |",
                "|---|---:|---|"])
    for topic in TOPICS:
        n = counts.get(topic, 0)
        out.append(f"| {topic} | {n} | {'Unverified source material' if n else 'Evidence gap'} |")
    out.extend(["", f"**Total indexed snippets:** {len(sources)}. Counts are not verified findings.", "",
                "## Detailed research findings", ""])
    for name, _ in SECTIONS:
        body = sections.get(name, "").strip() or "Insufficient evidence in the generated analysis."
        refs = citations_for(body, sources)
        out.extend([f"### {name}", "", body, "",
                    "**Cited source IDs:** " + (", ".join(f"[{ref}]" for ref in refs) if refs else "None identified"), ""])
    if sections.get("Other analysis"):
        out.extend(["### Additional analysis", "", sections["Other analysis"], ""])
    out.extend(["## Source register", "",
                "Source IDs map to retrieved snippets. URLs are leads for manual verification, not proof of claims.", ""])
    for source in sources:
        sid = str(source.get("id", "?"))
        title = str(source.get("title", "Untitled")).replace("\n", " ")
        url = str(source.get("url", ""))
        topic = str(source.get("topic", "Unknown"))
        safe_url = url if urlparse(url).scheme == "https" else "(invalid URL)"
        out.extend([f"### [{sid}] {title}", "", f"- Topic: {topic}",
                    f"- URL: {safe_url}", "- Verification: Not independently verified"])
        flags = source.get("flags") or []
        if flags:
            out.append("- Review flags: " + "; ".join(map(str, flags)))
        out.append("")
    out.extend(["## Methodology and limitations", "",
                "1. Tavily was used to discover publicly accessible search-result snippets.",
                "2. Deterministic keyword filters and text cleaning were applied; relevance does not establish reliability.",
                "3. Gemini generated interpretations from the selected snippets. Citations are model-generated and require checking.",
                "4. No original webpages were independently checked in this pipeline; numerical claims may be outdated.",
                "5. Missing topics must be treated as evidence gaps, not as proof of absence.",
                "6. Demo charts, mock scores, synthetic sentiment and rankings are deliberately excluded from this report.",
                "7. Strategic actions are hypotheses until independently validated and tested.", "",
                "**Required next step:** Review source URLs, confirm important facts and dates, and validate recommendations before external use.", ""])
    return "\n".join(out)
