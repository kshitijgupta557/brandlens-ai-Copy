"""PPT-ready report blueprint, deliberately without synthetic findings."""
import json

SECTIONS = [
    ("Executive summary", "Decision context, three supported findings, strategic implications and priorities.", "1–2", "Executive narrative and priority table"),
    ("Scope and methodology", "Company identity, category, market, time window, research questions, sampling and exclusions.", "3", "Scope table and research process"),
    ("Evidence register", "Source ID, exact URL, publisher, publication/access dates, extracted claim, limitations and verification status.", "Appendix", "Traceable claim-to-source register"),
    ("Brand identity and positioning", "Promise, target audience, benefits, tone, distinctive assets and positioning consistency.", "4–5", "Positioning statement and identity matrix"),
    ("Category and competitor landscape", "Competitor selection rationale, comparable offers, pricing dates and differentiators.", "6–7", "Comparison table and positioning map"),
    ("Consumer perception", "Feedback themes, sample size, platform mix, sentiment method and representative cited quotations.", "8–9", "Sentiment chart and theme-evidence table"),
    ("Digital presence", "Website, search and social review, consistent measurement periods and platform-specific limitations.", "10–11", "Channel scorecard and journey friction map"),
    ("Brand gaps and opportunities", "Observed gap, supporting evidence, business implication, uncertainty and counter-evidence.", "12–13", "Gap-to-opportunity matrix"),
    ("Strategic recommendations", "Action, rationale, evidence IDs, owner, dependencies, effort and expected mechanism of impact.", "14–15", "Impact-effort matrix; no invented ROI"),
    ("30 / 60 / 90-day roadmap", "Sequenced work, owners, milestones, dependencies and decision checkpoints.", "16", "Action roadmap"),
    ("Measurement plan", "KPI definitions, formulas, baselines, proposed targets, data owners and reporting cadence.", "17", "Measurement dashboard specification"),
    ("Limitations and appendix", "Missing evidence, unresolved questions, scoring rubric, calculation notes and full references.", "18 + appendix", "Caveats, source bibliography and calculations"),
]

def blueprint(workspace):
    lines = ["# BrandLens AI — Report blueprint", "",
             "**PLANNED STRUCTURE ONLY — NOT A COMPLETED BRAND AUDIT.**", "",
             "No evidence collected. No real findings, verified scores or recommendations are included.",
             "Dashboard mock data is intentionally excluded from this document.", "",
             "## Requested workspace (user-provided, unverified)", "",
             "    " + json.dumps(workspace, ensure_ascii=True), "",
             "## Suggested presentation structure", "",
             "Approximately 18 slides plus an evidence appendix; final length depends on the evidence.", ""]
    for title, detail, slides, visual in SECTIONS:
        lines.extend([f"### {title}", f"- Planned content: {detail}",
                      f"- Suggested slides: {slides}", f"- Suggested visual: {visual}",
                      "- Status: Awaiting evidence / not researched.", ""])
    lines.extend(["## Required standard for the future completed report", "",
                  "Separate verified facts, analyst interpretations, hypotheses and missing data.",
                  "Every factual claim and quantitative chart must link to dated evidence IDs.",
                  "Document comparable periods, formulas, denominators and sampling bias.",
                  "Label proposed targets as proposals, and validate recommendations before action."])
    return "\n".join(lines) + "\n"
