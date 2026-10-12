"""BrandLens AI — company in, research-backed brand audit out."""
import streamlit as st
from dashboard.ui import apply_styles
from audit_pipeline import run_complete_audit
from intelligence_dashboard import split_report, citations_for, coverage
from intelligence_export import build_intelligence_report
from pdf_export import build_pdf_report

st.set_page_config(page_title="BrandLens AI | Brand Audit", page_icon="◈", layout="wide")
apply_styles()

if "audit_history" not in st.session_state:
    st.session_state.audit_history = []

with st.sidebar:
    st.markdown('<div class="wordmark"><span class="brand-symbol">◈</span>BrandLens<span class="ai-badge">AI</span></div>', unsafe_allow_html=True)
    st.caption("AUTOMATED BRAND INTELLIGENCE")
    st.divider()
    st.caption("HOW IT WORKS")
    st.write("1. Enter a company name")
    st.write("2. Run automated research")
    st.write("3. Review the AI brand audit")
    st.write("4. Download your report")
    st.divider()
    if st.session_state.audit_history:
        st.caption("AUDITS IN THIS SESSION")
        for idx, item in enumerate(reversed(st.session_state.audit_history)):
            if st.button(item["scope"]["company"], key=f"past_{idx}", use_container_width=True):
                st.session_state.evidence_ai_report = item
                st.rerun()
    st.caption("Research is based on public search snippets, not independent fact-checking.")

st.markdown("## BrandLens AI")
st.markdown("### Automated Brand Audit")
st.write("Enter a company name to research its products, competitors, market, online presence, positioning and strategic opportunities.")

with st.form("run_audit"):
    company = st.text_input("Company name", placeholder="e.g. Haldiram's", max_chars=100)
    with st.expander("Optional research settings"):
        market = st.text_input("Market", value="India", max_chars=100)
        category = st.text_input("Industry or product category", value="General business", max_chars=100,
                                 help="Providing the specific category improves search relevance.")
    consent = st.checkbox("I authorize up to five Tavily searches and one Gemini request. I understand findings require source verification.")
    submitted = st.form_submit_button("Generate Brand Audit Report", type="primary", use_container_width=True)

if submitted:
    if not company.strip():
        st.error("Enter a company name.")
    elif not market.strip() or not category.strip():
        st.error("Market and category cannot be empty.")
    elif not consent:
        st.warning("Please authorize the research requests before generating a report.")
    else:
        st.session_state.pop("evidence_ai_report", None)
        try:
            with st.spinner("Researching sources and generating your brand audit. This may take a minute..."):
                result = run_complete_audit(company.strip(), market.strip(), category.strip())
            if result.get("analysis"):
                analysis = result["analysis"]
                st.session_state.evidence_ai_report = analysis
                st.session_state.audit_history.append(analysis)
                st.session_state.audit_history = st.session_state.audit_history[-10:]
                st.success("Research draft generated. Review evidence coverage and gaps before using the report.")
            else:
                st.warning(result.get("message", "No usable evidence found."))
            if result.get("research", {}).get("errors"):
                st.warning("Some searches failed: " + "; ".join(result["research"]["errors"]))
        except (ValueError, RuntimeError) as exc:
            st.error("The audit could not be completed: " + str(exc))
            st.info("No automatic retry was made. Check your API quota or try again later.")

analysis = st.session_state.get("evidence_ai_report")
if analysis:
    scope = analysis.get("scope", {})
    st.divider()
    st.subheader(f"Brand Audit — {scope.get('company', 'Company')}")
    st.caption(f"Market: {scope.get('market', 'Not specified')} · Category: {scope.get('category', 'Not specified')}")
    st.warning("AI analysis of search snippets — not independently fact-checked. Verify important claims against the source links.")
    counts = coverage(analysis)
    a, b, c = st.columns(3)
    a.metric("Collected sources", analysis.get("source_count", 0))
    b.metric("Research topics covered", sum(1 for v in counts.values() if v))
    c.metric("Topics with no sources", sum(1 for v in counts.values() if not v))
    st.caption("Coverage counts reflect collected snippets, not source credibility or verified findings.")
    critical = [name for name in ("Competitors", "Digital presence", "Brand positioning") if counts.get(name, 0) == 0]
    if critical:
        st.error("Incomplete audit: no evidence collected for " + ", ".join(critical) +
                 ". The report is a partial research draft, not a comprehensive brand audit.")

    report = split_report(analysis.get("report_markdown", ""))
    names = ["Brand overview", "Competitor landscape", "Market insights", "Digital presence", "Strategic recommendations", "Evidence gaps"]
    tabs = st.tabs(["Overview", "Competitors", "Market", "Digital", "Strategy", "Evidence gaps"])
    source_map = {s.get("id"): s for s in analysis.get("sources", [])}
    for tab, name in zip(tabs, names):
        with tab:
            st.markdown("#### " + name)
            body = report.get(name, "").strip()
            if body:
                st.markdown(body)
                refs = citations_for(body, analysis.get("sources", []))
                if refs:
                    with st.expander("View cited sources"):
                        for ref in refs:
                            src = source_map[ref]
                            st.markdown(f"**[{ref}]** [{src.get('title', 'Source')}]({src.get('url', '')})")
            else:
                st.info("Insufficient evidence in the generated report.")
    st.markdown("### Download your report")
    left, right = st.columns(2)
    with left:
        st.download_button("Download PDF Report", build_pdf_report(analysis),
                           file_name="brandlens-brand-audit.pdf", mime="application/pdf",
                           use_container_width=True, type="primary")
    with right:
        st.download_button("Download Markdown Report", build_intelligence_report(analysis),
                           file_name="brandlens-brand-audit.md", mime="text/markdown",
                           use_container_width=True)
    with st.expander("Full source register"):
        for source in analysis.get("sources", []):
            st.markdown(f"**{source.get('id')}** [{source.get('title', 'Source')}]({source.get('url', '')}) — {source.get('topic', '')}")
    st.caption("Audits are retained only during this browser session; download reports to keep them.")
else:
    st.info("Your generated report will appear here after the research completes. No sample brand scores or synthetic charts are shown.")
