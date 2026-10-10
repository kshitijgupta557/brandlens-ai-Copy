"""Responsive presentation helpers; user text is escaped before HTML."""
from html import escape
import streamlit as st

def apply_styles():
    st.markdown("""<style>
    .stApp {background:#f7f8fa;color:#202d36;}
    .block-container {max-width:1440px;padding-top:2.2rem;padding-bottom:2rem;}
    [data-testid="stSidebar"] {background:#fff;border-right:1px solid #e4e8eb;}
    h1,h2,h3 {letter-spacing:-.035em;color:#202d36;}
    h1 {font-weight:650 !important;font-size:2.2rem !important;}
    h3 {font-size:1.18rem !important;}
    .wordmark {font-size:1.55rem;font-weight:750;letter-spacing:-.055em;margin:8px 0 4px;}
    .wordmark span {color:#267568;margin-left:5px;font-size:.85rem;letter-spacing:0;}
    [data-testid="stSidebar"] [role="radiogroup"] {gap:7px;}
    [data-testid="stSidebar"] [role="radiogroup"] label {padding:8px 5px;border-radius:8px;}
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:#edf5f1;}
    .eyebrow {font-size:.7rem;letter-spacing:.16em;color:#66757d;font-weight:650;margin-bottom:8px;}
    .demo-notice {border:1px solid #e6dfcc;background:#fcf9f0;color:#675836;padding:12px 16px;
      border-radius:9px;font-size:.82rem;margin:12px 0 24px;line-height:1.55;}
    .demo-notice b {font-size:.68rem;letter-spacing:.09em;margin-right:12px;}
    .kpi-grid {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:8px 0 24px;}
    .kpi {background:#fff;border:1px solid #e4e8eb;border-radius:12px;padding:21px;min-width:0;}
    .kpi-label {color:#66757d;font-size:.82rem;}
    .kpi-value {font-size:2.05rem;font-weight:650;letter-spacing:-.05em;margin:8px 0;color:#213c36;}
    .kpi-note {color:#66757d;font-size:.74rem;line-height:1.5;}
    .feature {border-left:3px solid #b49b65;padding:4px 0 4px 16px;margin:12px 0 20px;}
    .feature p {color:#61717a;font-size:.9rem;line-height:1.6;margin:8px 0 0;}
    [data-testid="stVerticalBlockBorderWrapper"] {background:#fff;border-radius:12px;}
    @media(max-width:1000px) {.kpi-grid {grid-template-columns:repeat(2,minmax(0,1fr));}}
    @media(max-width:600px) {.block-container {padding:1.2rem 1rem;}.kpi-grid {grid-template-columns:1fr;gap:10px;}
      h1 {font-size:1.8rem !important;}.kpi {padding:16px;}}
    </style>""", unsafe_allow_html=True)

def page_header(page, company):
    st.markdown('<div class="eyebrow">BRANDLENS AI / INTELLIGENCE WORKSPACE</div>', unsafe_allow_html=True)
    st.title(page)
    st.caption(f"Workspace: {company} · Local demonstration · No live data")

def kpis(items):
    cards = "".join(f'<div class="kpi"><div class="kpi-label">{escape(label)}</div>'
        f'<div class="kpi-value">{escape(str(value))}</div><div class="kpi-note">{escape(note)}</div></div>'
        for label, value, note in items)
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)

def feature(title, body):
    st.markdown(f'<div class="feature"><b>{escape(title)}</b><p>{escape(body)}</p></div>', unsafe_allow_html=True)
