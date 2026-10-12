"""Offline regression tests. Never call Gemini or Tavily."""
import unittest
from unittest.mock import patch
from intelligence_export import build_intelligence_report
from intelligence_dashboard import split_report, citations_for, coverage
from evidence_processing import process_evidence
from pdf_export import build_pdf_report
from audit_pipeline import run_complete_audit

SAMPLE = {
    "scope": {"company": "Example Snacks", "market": "India", "category": "Snacks"},
    "generated_at_utc": "2026-10-13T00:00:00+00:00",
    "report_markdown": "## Brand overview\nExample Snacks offers snacks [S1].\n\n"
                       "## Competitor landscape\nInsufficient evidence.\n\n"
                       "## Market insights\nInsufficient evidence.\n\n"
                       "## Digital presence\nInsufficient evidence.\n\n"
                       "## Strategic recommendations\nTest product messaging [S1].\n\n"
                       "## Evidence gaps\nCompetitors are unresearched.",
    "sources": [{"id": "S1", "topic": "Company & products", "title": "Company site",
                 "url": "https://example.com", "snippet": "Example Snacks offers snacks",
                 "flags": []}],
}


class OfflineReportTests(unittest.TestCase):
    def test_section_and_citations(self):
        sections = split_report(SAMPLE["report_markdown"])
        self.assertIn("offers snacks", sections["Brand overview"])
        self.assertEqual(citations_for(sections["Brand overview"], SAMPLE["sources"]), ["S1"])
        self.assertEqual(coverage(SAMPLE)["Company & products"], 1)

    def test_markdown_report(self):
        report = build_intelligence_report(SAMPLE)
        self.assertIn("Example Snacks", report)
        self.assertIn("https://example.com", report)
        self.assertIn("not independently", report.lower())

    def test_pdf_signature(self):
        data = build_pdf_report(SAMPLE)
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertGreater(len(data), 2000)

    def test_cleaning(self):
        raw = {"scope": SAMPLE["scope"], "sections": [
            {"topic": "Company & products", "sources": [
                {"url": "https://example.com", "title": "Company",
                 "snippet": "Example Snacks has 410 products. Shop now!"}]}]}
        cleaned = process_evidence(raw)
        self.assertEqual(cleaned["source_count"], 1)
        self.assertTrue(cleaned["sections"][0]["sources"][0]["review_flags"])

    @patch("audit_pipeline.analyze_evidence")
    @patch("audit_pipeline.process_evidence")
    @patch("audit_pipeline.run_research")
    def test_full_pipeline(self, search, process, analyze):
        search.return_value = {"sections": [], "scope": SAMPLE["scope"]}
        process.return_value = {"source_count": 1}
        analyze.return_value = SAMPLE
        result = run_complete_audit("Example Snacks", "India", "Snacks")
        self.assertEqual(result["analysis"]["scope"]["company"], "Example Snacks")
        search.assert_called_once()
        analyze.assert_called_once()

    @patch("audit_pipeline.analyze_evidence")
    @patch("audit_pipeline.process_evidence")
    @patch("audit_pipeline.run_research")
    def test_skip_gemini_when_no_sources(self, search, process, analyze):
        search.return_value = {"sections": []}
        process.return_value = {"source_count": 0}
        result = run_complete_audit("Example Snacks", "India", "Snacks")
        self.assertIsNone(result["analysis"])
        analyze.assert_not_called()


if __name__ == "__main__":
    unittest.main()
