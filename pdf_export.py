"""Generate a clean PDF report from an existing Gemini analysis, without network calls."""
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, HRFlowable
from intelligence_dashboard import SECTIONS, split_report, coverage, citations_for

INK = colors.HexColor("#24343A")
TEAL = colors.HexColor("#157663")
MUTED = colors.HexColor("#617278")


def _p(text, style):
    return Paragraph(escape(str(text or "")).replace("\n", "<br/>"), style)


def build_pdf_report(analysis):
    """Return a downloadable PDF byte string; no Tavily or Gemini requests."""
    if not isinstance(analysis, dict) or not analysis.get("report_markdown"):
        raise ValueError("Generate Gemini evidence analysis before exporting PDF.")
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=(595.28, 841.89),
                            leftMargin=48, rightMargin=48, topMargin=56, bottomMargin=55,
                            title="BrandLens Brand Intelligence Report", author="BrandLens AI")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BLTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=22, leading=28, textColor=INK, spaceAfter=16, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name="BLSection", parent=styles["Heading2"], fontSize=13, leading=18,
                              textColor=TEAL, spaceBefore=18, spaceAfter=9))
    styles.add(ParagraphStyle(name="BLBody", parent=styles["BodyText"], fontSize=9.5, leading=15,
                              textColor=INK, spaceAfter=9, wordWrap="CJK"))
    styles.add(ParagraphStyle(name="BLMeta", parent=styles["BodyText"], fontSize=8.5, leading=13,
                              textColor=MUTED, spaceAfter=8, wordWrap="CJK"))
    story = []
    scope = analysis.get("scope") or {}
    company = str(scope.get("company") or "Unspecified brand")
    story.append(_p("Brand Intelligence Report", styles["BLTitle"]))
    story.append(_p(company + "  |  " + str(scope.get("market", "")) + "  |  " +
                    str(scope.get("category", "")), styles["BLBody"]))
    story.append(_p("AI interpretation of unverified search snippets. Not independently fact-checked.",
                    styles["BLMeta"]))
    story.append(_p("Generated: " + str(analysis.get("generated_at_utc", "Unknown")), styles["BLMeta"]))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=16))
    sections = split_report(analysis["report_markdown"])
    counts = coverage(analysis)
    story.append(_p("Executive brief", styles["BLSection"]))
    story.append(_p("This audit evaluates the available brand evidence across company, competition, market, digital presence and strategic options. Findings below are AI interpretations of unverified snippets; evidence gaps are explicitly marked.", styles["BLBody"]))
    story.append(_p("Evidence coverage", styles["BLSection"]))
    for topic in ("Company & products", "Competitors", "Market & industry", "Digital presence", "Brand positioning"):
        count = counts.get(topic, 0)
        story.append(_p(f"{topic}: {count} collected snippet(s)" +
                        (" — evidence gap" if not count else " — unverified"), styles["BLBody"]))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#D7E6DF"), spaceBefore=12, spaceAfter=8))
    story.append(_p("Brand audit findings", styles["BLSection"]))
    for heading, _ in SECTIONS:
        story.append(_p(heading, styles["BLSection"]))
        body = sections.get(heading, "").strip()
        if not body:
            story.append(_p("Insufficient evidence in the generated analysis.", styles["BLBody"]))
        else:
            # Keep generated citations as text and preserve paragraph breaks.
            for paragraph in body.split("\n\n"):
                if paragraph.strip():
                    story.append(_p(paragraph[:9000], styles["BLBody"]))
        refs = citations_for(body, analysis.get("sources") or [])
        story.append(_p("Cited IDs: " + (", ".join(refs) if refs else "None"), styles["BLMeta"]))
    story.append(_p("Source register", styles["BLSection"]))
    for source in analysis.get("sources") or []:
        title = str(source.get("title") or "Untitled")
        url = str(source.get("url") or "")
        topic = str(source.get("topic") or "Unknown")
        story.append(KeepTogether([
            _p(f"[{source.get('id', '?')}] {title}", styles["BLBody"]),
            _p(f"{topic} | {url}", styles["BLMeta"]),
            _p("Verification: Not independently verified", styles["BLMeta"]),
        ]))
    story.append(_p("Methodology and limitations", styles["BLSection"]))
    for line in (
        "Tavily discovered public search snippets; filtering was based on keywords and text cleanup.",
        "Gemini interpreted those snippets. Model-generated citations require manual review.",
        "Original webpages, numeric claims, market sizes, competitors and recommendations have not been independently verified.",
        "Missing topics indicate evidence gaps, not the absence of business activity.",
        "All synthetic demonstration charts, sentiment scores and rankings are excluded.",
        "Validate important claims against original sources before sharing or making business decisions.",
    ):
        story.append(_p("– " + line, styles["BLBody"]))
    def footer(canvas, document):
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(48, 32, "BrandLens AI | Research draft — not fact-checked")
        canvas.drawRightString(547, 32, f"Page {document.page}")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()
