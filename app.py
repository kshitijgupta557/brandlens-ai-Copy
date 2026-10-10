"""BrandLens AI: first development milestone, with no model requests."""

import streamlit as st

from gemini import MODEL_ID, get_api_key

st.set_page_config(page_title="BrandLens AI", page_icon="🔎")
st.title("BrandLens AI")
st.caption("An evidence-based brand auditing application — foundation milestone.")

company_name = st.text_input("Company name", placeholder="Enter a company name")
if company_name.strip():
    st.write("Company selected:", company_name.strip())

st.info("Scaffold only. Brand audits and Gemini API requests are not enabled.")
st.caption(f"Provisional model: {MODEL_ID}")
if get_api_key():
    st.success("API key detected locally. It has not been validated or used.")
else:
    st.warning("No API key configured. You can still use this screen.")
