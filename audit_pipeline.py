"""Orchestrate one explicitly authorized research run, with no retries."""
from automated_research import run_research
from evidence_processing import process_evidence
from evidence_analysis import analyze_evidence


def run_complete_audit(company, market, category):
    """Up to five basic Tavily searches and one Gemini call."""
    research = run_research(company, market, category)
    processed = process_evidence(research)
    if not processed.get("source_count"):
        return {"research": research, "processed": processed, "analysis": None,
                "message": "No usable evidence; Gemini not called."}
    analysis = analyze_evidence(processed)
    return {"research": research, "processed": processed, "analysis": analysis,
            "message": "Audit analysis generated from collected evidence."}
