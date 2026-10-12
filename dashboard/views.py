"""Seven dashboard screens, powered entirely by local fixtures."""
from datetime import datetime, timezone
import streamlit as st
from dashboard import charts, demo
from brand_research import generate_preliminary_audit
from tavily_search import search_once
from automated_research import run_research
from evidence_processing import process_evidence
import json
from dashboard.report import SECTIONS, blueprint
from dashboard.ui import audit_hero, feature, kpis

def brand_audit():
    audit_hero()
    left, right = st.columns([1.4, 1], gap="large")
    with left, st.container(border=True):
        st.subheader("Set up your brand workspace")
        st.caption("01 / DEFINE THE SCOPE · About a minute to explore the demo")
        with st.form("audit_setup"):
            current = st.session_state.workspace
            company = st.text_input("Company name", value=current["company"], max_chars=100)
            market = st.text_input("Market", value=current["market"], max_chars=80)
            category = st.text_input("Category", value=current["category"], max_chars=100)
            acknowledged = st.checkbox("I understand this loads synthetic examples, not research about this company.")
            submitted = st.form_submit_button("Run demo audit", type="primary", width="stretch")
        if submitted:
            if not company.strip():
                st.error("Enter a company name to label the workspace.")
            elif not acknowledged:
                st.warning("Confirm that you understand the demo uses synthetic data.")
            else:
                st.session_state.workspace = {"company": company.strip(), "market": market.strip(), "category": category.strip()}
                st.session_state.demo_loaded = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
                st.rerun()
        if "demo_loaded" in st.session_state:
            st.success("Demo workspace ready. Open Overview or any analysis page in the sidebar.")
            st.caption(f"Demo loaded: {st.session_state.demo_loaded}. This is not a research timestamp.")
    with right:
        feature("01 / Define the scope", "Your company, category and market label the workspace. Inputs stay in the current server session.")
        feature("02 / Load the demonstration", "The same fictional dataset is used for every company. No sites are searched and no model is called.")
        feature("03 / Explore the report structure", "Review the dashboard and download a report blueprint with evidence requirements and suggested slides.")
    st.divider()
    st.subheader("AI Brand Research · preliminary draft")
    st.caption("One manual Gemini request per click. No web search or verified sources. This is not a completed audit.")
    with st.form("ai_research_form"):
        scope = st.session_state.workspace
        ai_company = st.text_input("Research company", value=scope["company"], max_chars=100)
        ai_market = st.text_input("Research market", value=scope["market"], max_chars=80)
        ai_category = st.text_input("Research category", value=scope["category"], max_chars=100)
        consent = st.checkbox("I understand this sends the three inputs to Gemini and returns unverified AI hypotheses.")
        run_ai = st.form_submit_button("Generate preliminary AI analysis", type="primary")
    if run_ai:
        if not consent:
            st.warning("Please acknowledge the AI-generated and unverified nature of this draft.")
        elif not all(x.strip() for x in (ai_company, ai_market, ai_category)):
            st.warning("Complete all three fields.")
        else:
            st.session_state.pop("ai_draft", None)
            with st.spinner("Generating one preliminary AI draft..."):
                try:
                    draft = generate_preliminary_audit(ai_company, ai_market, ai_category)
                    st.session_state.ai_draft = {
                        "scope": (ai_company.strip(), ai_market.strip(), ai_category.strip()),
                        "result": draft,
                    }
                except (RuntimeError, ValueError) as exc:
                    st.error(str(exc))
    if "ai_draft" in st.session_state:
        saved = st.session_state.ai_draft
        draft = saved["result"]
        st.warning("UNVERIFIED AI DRAFT · No sources checked. Do not use as established facts or business decisions.")
        st.caption("Scope: " + " · ".join(saved["scope"]))
        for field, label in [
            ("overview", "Brand overview"), ("products", "Potential product categories"),
            ("target_customers", "Possible target customers"), ("positioning", "Positioning hypothesis"),
            ("competitors", "Potential competitors — verify identities"),
            ("strengths", "SWOT · strengths (hypotheses)"),
            ("weaknesses", "SWOT · weaknesses (hypotheses)"),
            ("opportunities", "SWOT · opportunities (hypotheses)"),
            ("threats", "SWOT · threats (hypotheses)"),
            ("verification_priorities", "What to verify next"),
        ]:
            with st.expander(label, expanded=field in ("overview", "verification_priorities")):
                value = draft[field]
                if isinstance(value, list):
                    for item in value:
                        st.write("• " + item)
                else:
                    st.write(value)
        st.download_button(
            "Download unverified draft (.json)",
            data=json.dumps({"status": "UNVERIFIED AI DRAFT", **saved}, indent=2),
            file_name="brandlens-preliminary-ai-draft.json",
            mime="application/json",
        )
    st.divider()
    st.subheader("Tavily source discovery · connection test")
    st.caption("One manually initiated BASIC Tavily search (typically one search credit). No Gemini request, scraping, or automatic retries.")
    with st.form("tavily_search_form"):
        base = st.session_state.workspace
        src_company = st.text_input("Company for Tavily search", value=base["company"], max_chars=100)
        src_market = st.text_input("Market for Tavily search", value=base["market"], max_chars=80)
        src_category = st.text_input("Category for Tavily search", value=base["category"], max_chars=100)
        src_ack = st.checkbox("I understand this uses Tavily search credits and results are unverified.")
        src_run = st.form_submit_button("Test Tavily search")
    if src_run:
        if not src_ack:
            st.warning("Please acknowledge the Tavily usage and evidence limitations.")
        elif not all(x.strip() for x in (src_company, src_market, src_category)):
            st.warning("Complete all three fields.")
        else:
            st.session_state.pop("tavily_test_result", None)
            with st.spinner("Running one Tavily basic search..."):
                try:
                    st.session_state.tavily_test_result = search_once(src_company, src_market, src_category)
                except (RuntimeError, ValueError) as exc:
                    st.error(str(exc))
    if "tavily_test_result" in st.session_state:
        result = st.session_state.tavily_test_result
        st.success("Tavily connection successful — search response received.")
        st.warning(result["status"])
        st.caption("Query: " + result["query"])
        st.caption("Retrieved: " + result["retrieved_at_utc"])
        if result["sources"]:
            for source in result["sources"]:
                with st.container(border=True):
                    st.markdown(f"**[{source['title']}]({source['url']})**")
                    st.write(source["snippet"] or "No snippet supplied.")
        else:
            st.info("Tavily returned no usable HTTPS source links.")
        st.caption(result["note"])
        st.download_button("Download unverified source leads (.json)",
                           json.dumps(result, indent=2),
                           file_name="brandlens-tavily-test.json",
                           mime="application/json")
    st.divider()
    st.subheader("Automated brand research · five topics")
    st.caption("One click runs up to five BASIC Tavily searches. Estimated maximum: five basic-search credits. No Gemini calls or automatic retries.")
    with st.form("automated_tavily_form"):
        base = st.session_state.workspace
        auto_company = st.text_input("Brand to research", value=base["company"], max_chars=100)
        auto_market = st.text_input("Target market", value=base["market"], max_chars=80)
        auto_category = st.text_input("Product category", value=base["category"], max_chars=100)
        auto_ack = st.checkbox("I approve up to five Tavily basic searches for this run and understand the results are unverified.")
        auto_run = st.form_submit_button("Run five-topic research", type="primary")
    if auto_run:
        if not auto_ack:
            st.warning("Please acknowledge the research credit budget.")
        elif not all(v.strip() for v in (auto_company, auto_market, auto_category)):
            st.warning("Complete all three fields.")
        else:
            st.session_state.pop("automated_tavily_result", None)
            st.session_state.pop("processed_evidence", None)
            with st.spinner("Collecting public search results across five topics..."):
                try:
                    st.session_state.automated_tavily_result = run_research(auto_company, auto_market, auto_category)
                except (RuntimeError, ValueError) as exc:
                    st.error(str(exc))
    if "automated_tavily_result" in st.session_state:
        report = st.session_state.automated_tavily_result
        st.warning(report["status"])
        st.caption(f"Requests attempted: {report['requests_attempted']} / {report['maximum_requests']} · Unique source URLs: {report['unique_sources']}")
        st.caption("Retrieved: " + report["retrieved_at_utc"])
        for issue in report["errors"]:
            st.error(issue)
        for section in report["sections"]:
            with st.expander(f"{section['topic']} · {len(section['sources'])} accepted · {section.get('rejected_irrelevant', 0)} rejected", expanded=False):
                st.caption("Search query: " + section["query"])
                if not section["sources"]:
                    st.info("No new usable HTTPS source links for this topic.")
                for source in section["sources"]:
                    st.markdown(f"**[{source['title']}]({source['url']})**")
                    st.write(source["snippet"] or "No snippet provided.")
        st.caption(report["note"])
        st.download_button("Download research evidence (.json)", data=json.dumps(report, indent=2),
                           file_name="brandlens-five-topic-research.json", mime="application/json")
    if "automated_tavily_result" in st.session_state:
        st.subheader("Evidence processing · no API credits")
        if st.button("Clean and review collected evidence"):
            try:
                st.session_state.processed_evidence = process_evidence(st.session_state.automated_tavily_result)
            except ValueError as exc:
                st.error(str(exc))
        if "processed_evidence" in st.session_state:
            processed = st.session_state.processed_evidence
            st.warning(processed["status"])
            st.caption(f"Processed sources: {processed['source_count']} · {processed['method']}")
            for section in processed["sections"]:
                with st.expander(f"{section['topic']} · {len(section['sources'])} processed", expanded=False):
                    for source in section["sources"]:
                        st.markdown(f"**[{source['title']}]({source['url']})**")
                        st.caption(source["domain"] + " · " + source["source_type"])
                        st.write(source["clean_snippet"])
                        for flag in source["review_flags"]:
                            st.caption("Review: " + flag)
            st.download_button("Download processed evidence (.json)",
                               json.dumps(processed, indent=2),
                               file_name="brandlens-processed-evidence.json",
                               mime="application/json")
    st.divider()
    st.subheader("The planned audit team")
    st.caption("Architecture preview only. These agents are not running.")
    st.dataframe([
        {"Planned role": "Research", "Responsibility": "Collect and date public evidence", "Status": "Not implemented"},
        {"Planned role": "Brand & competitors", "Responsibility": "Compare positioning using traceable sources", "Status": "Not implemented"},
        {"Planned role": "Consumer & digital", "Responsibility": "Review signals and sampling limitations", "Status": "Not implemented"},
        {"Planned role": "Strategy & verification", "Responsibility": "Challenge claims and prioritize supported actions", "Status": "Not implemented"},
    ], hide_index=True, width="stretch")

def overview():
    kpis([("Brand health · demo", f"{demo.HEALTH}/100", "Equal-weight average of 5 synthetic dimensions"),
          ("Positive sentiment · demo", "64%", "Illustrative sentiment distribution"),
          ("Share of voice · demo", "28%", "Fictional four-brand comparison"),
          ("Verified sources", "0", "Evidence collection has not started")])
    left, right = st.columns([1.5, 1], gap="large")
    with left, st.container(border=True):
        st.subheader("Brand momentum")
        st.caption("MOCK SERIES · Six illustrative periods, not calendar observations")
        charts.trend()
    with right, st.container(border=True):
        st.subheader("The brand at a glance")
        st.caption("MOCK SCORECARD · Illustrative scores out of 100")
        charts.bars(demo.DIMENSIONS, "Dimension", "Score", "Score / 100")
    st.subheader("Executive perspective")
    st.caption("Example interpretations of the fictional dataset — not findings about your company.")
    cols = st.columns(3, gap="medium")
    for col, title, body in zip(cols,
            ["A clear foundation", "Room to stand apart", "Evidence comes first"],
            ["In this example, brand clarity is the strongest dimension at 82/100.",
             "Differentiation is the lowest sample dimension at 61/100; it would be a research priority.",
             "Zero sources are verified. No business decision should rely on these illustrative scores."]):
        with col, st.container(border=True):
            feature(title, body)
    with st.expander("Demo methodology and underlying values"):
        st.write("Health = the rounded arithmetic mean of five mock scores. Other values are fixed fixtures, not estimates. No confidence level is claimed.")
        st.dataframe(demo.DIMENSIONS, hide_index=True, width="stretch")

def competitors():
    kpis([("Brands in demo", "4", "One fictional brand and three fictional peers"),
          ("Sample brand rank", "2 of 4", "Ranked only by mock health score"),
          ("Gap to sample leader", "9 pts", "81 minus 72; not a real benchmark"),
          ("Competitors verified", "0", "No competitor identities researched")])
    left, right = st.columns(2, gap="large")
    with left, st.container(border=True):
        st.subheader("Relative brand health · demo")
        charts.bars(demo.COMPETITORS, "Brand", "Health score", "Illustrative score / 100")
    with right, st.container(border=True):
        st.subheader("Share of voice · demo")
        charts.bars(demo.COMPETITORS, "Brand", "Voice share", "Illustrative share (%)", charts.GOLD)
    st.dataframe(demo.COMPETITORS, hide_index=True, width="stretch")
    st.caption("Share values total 100%. No mention corpus, market-share data or actual competitors were collected.")
    feature("What a real comparison will need", "A defined competitor set, dated sources, comparable geography and measurement periods, and an explicit scoring rubric.")

def sentiment():
    kpis([("Positive · demo", "64%", "Synthetic distribution"), ("Neutral · demo", "24%", "Synthetic distribution"),
          ("Negative · demo", "12%", "Synthetic distribution"), ("Real reviews collected", "0", "No consumer research performed")])
    left, right = st.columns([1, 1.3], gap="large")
    with left, st.container(border=True):
        st.subheader("How the conversation could look")
        st.caption("DEMO · No real consumer statements")
        charts.sentiment()
    with right, st.container(border=True):
        st.subheader("Illustrative conversation themes")
        st.dataframe(demo.THEMES, hide_index=True, width="stretch")
        st.caption("1,200 synthetic mentions, assigned to mutually exclusive themes. Counts are invented for layout demonstration.")
        feature("Read the context, not just the percentage", "A future audit must explain platform coverage, language, sample selection and uncertainty before interpreting sentiment.")

def digital():
    kpis([("Digital index · demo", "74/100", "Mean of 3 fictional channel scores"),
          ("Website · demo", "82/100", "Illustrative score"), ("Search · demo", "74/100", "Illustrative score"),
          ("Social · demo", "66/100", "Illustrative score")])
    left, right = st.columns([1.2, 1], gap="large")
    with left, st.container(border=True):
        st.subheader("Channel performance · demo")
        charts.bars(demo.CHANNELS, "Channel", "Score", "Illustrative score / 100")
    with right, st.container(border=True):
        st.subheader("Future assessment checklist")
        for title, body in [("Website", "Message clarity, product information, accessibility and conversion journey."),
                            ("Search", "Discoverability, branded queries and comparable organic visibility."),
                            ("Social", "Content consistency, meaningful engagement and response practices.")]:
            feature(title, body)
    st.caption("No website crawl, search query, analytics connection or social platform request has been performed.")

def recommendations():
    st.write("An example action agenda. Every item below is a hypothesis for demonstration, not advice based on company evidence.")
    stage = st.selectbox("Planning horizon", ["All stages", "Days 1–30", "Days 31–60", "Days 61–90"])
    for item in demo.PRIORITIES:
        if stage != "All stages" and item["window"] != stage:
            continue
        with st.container(border=True):
            st.caption(f"{item['priority']} · {item['area'].upper()} · {item['window']} · DEMO HYPOTHESIS")
            st.subheader(item["title"])
            st.write(item["hypothesis"])
            st.write("**Proposed test:** " + item["action"])
            st.write("**Evidence required:** " + item["evidence"])
            st.caption(f"Suggested owner: {item['owner']} · Measure: {item['metric']}")
    st.info("Priorities and timing are illustrative. Impact, cost and confidence remain unassessed until evidence is available.")

def reports():
    kpis([("Planned sections", str(len(SECTIONS)), "Detailed audit structure"),
          ("Suggested presentation", "~18 slides", "Plus evidence appendix"),
          ("Verified findings", "0", "No completed audit yet"),
          ("Available download", "Blueprint", "Markdown outline, not a findings report")])
    st.subheader("From evidence to an executive presentation")
    st.write("The planned report will connect each finding to sources, explain its business meaning, and translate it into a testable action. The outline below is ready to guide a future presentation.")
    st.download_button("Download report blueprint (.md)", blueprint(st.session_state.workspace),
                       file_name="brandlens-report-blueprint.md", mime="text/markdown", type="primary")
    st.caption("Structure only. Includes no mock findings. PDF, Word and PowerPoint exports are not implemented in this milestone.")
    for index, (title, detail, slides, visual) in enumerate(SECTIONS, 1):
        with st.expander(f"{index:02d} / {title}", expanded=index == 1):
            st.write(detail)
            st.write("**Suggested visual:** " + visual)
            st.caption(f"Suggested slides: {slides} · Status: Awaiting evidence / not researched")
    feature("The evidence standard", "Future reports must separate verified facts, interpretations and hypotheses. Every quantitative claim needs a source, date, method and limitation.")
