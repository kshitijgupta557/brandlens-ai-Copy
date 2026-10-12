"""BrandLens AI: a local demonstration, with no external research requests."""
import streamlit as st
from dashboard import views
from dashboard.ui import apply_styles, page_header
from gemini import get_api_key

st.set_page_config(page_title="BrandLens AI", page_icon="◈", layout="wide")
apply_styles()
if "workspace" not in st.session_state:
    st.session_state.workspace = {"company": "Sample Brand", "market": "India", "category": "Healthy snacks"}
PAGES = {
    "Brand Audit": views.brand_audit, "Overview": views.overview,
    "Competitor Analysis": views.competitors, "Consumer Sentiment": views.sentiment,
    "Digital Presence": views.digital, "Strategic Recommendations": views.recommendations,
    "Reports": views.reports,
}
with st.sidebar:
    st.markdown('<div class="wordmark"><span class="brand-symbol">◈</span>BrandLens<span class="ai-badge">AI</span></div>', unsafe_allow_html=True)
    st.caption("BRAND INTELLIGENCE WORKSPACE")
    st.divider()
    st.markdown('<div class="sidebar-label">EXPLORE YOUR BRAND</div>', unsafe_allow_html=True)
    page = st.radio("Workspace navigation", list(PAGES), index=1, key="navigation", label_visibility="collapsed",
                    format_func=lambda name: f"{list(PAGES).index(name) + 1:02d}  {name}")
    st.divider()
    st.caption("CURRENT WORKSPACE")
    st.text(st.session_state.workspace["company"])
    st.caption("Demo mode · No external research")
    with st.expander("Connection status"):
        st.write("Gemini requests: disabled")
        st.caption("Key detected (not validated)." if get_api_key() else "No API key needed for this demo.")
    st.caption("MILESTONE 02.1 / PRODUCT PREVIEW")
page_header(page, st.session_state.workspace["company"])
st.markdown('<div class="demo-notice"><b>DEMO DATA</b> All scores, charts and examples are synthetic. '
            'They do not describe the entered company. No sources have been collected.</div>', unsafe_allow_html=True)
PAGES[page]()
st.divider()
st.caption("BrandLens AI · Demo workspace · Evidence collection and live audits are planned, not active.")
