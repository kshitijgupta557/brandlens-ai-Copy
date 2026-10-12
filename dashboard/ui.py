"""Responsive presentation helpers; user text is escaped before HTML."""
from html import escape
import streamlit as st


def apply_styles():
    st.markdown("""<style>
    :root {--ink:#24343a;--teal:#157663;--gold:#a47727;--violet:#8064b0;--coral:#c86d58;}
    .stApp {background:#f7f8fa;color:var(--ink);}
    /* Streamlit's fixed toolbar needs clearance at every breakpoint. Never collapse
       this to the old 1.2rem mobile inset or clip the header to a fixed height. */
    [data-testid="stMainBlockContainer"], .main .block-container {
      max-width:1440px;padding:5.25rem 2.4rem 2.5rem;box-sizing:border-box;}
    .brand-header {position:relative;height:auto;min-height:0;overflow:visible;
      padding:4px 0 10px;margin:0;white-space:normal;overflow-wrap:anywhere;}
    .eyebrow {display:block;font-size:.69rem;letter-spacing:.13em;color:#586c70;
      font-weight:700;line-height:1.8;padding:2px 0;margin:0 0 10px;overflow:visible;}
    .brand-header h1 {font-size:clamp(1.8rem,3vw,2.55rem);font-weight:700;line-height:1.22;
      padding:0;margin:0 0 12px;letter-spacing:-.045em;color:var(--ink);}
    .header-meta {display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;color:#647378;font-size:.83rem;line-height:1.7;}
    .demo-pill {display:inline-flex;align-items:center;gap:7px;background:#e7f3ee;color:#17604f;
      border:1px solid #cce5d9;border-radius:999px;padding:3px 10px;font-size:.7rem;font-weight:650;}
    h2,h3 {letter-spacing:-.025em;color:var(--ink);line-height:1.4 !important;}
    h3 {font-size:1.16rem !important;}
    [data-testid="stSidebar"] {background:#fff;border-right:1px solid #e4e9e8;}
    [data-testid="stSidebarUserContent"] {padding-top:1.5rem;}
    .wordmark {display:flex;align-items:center;gap:10px;line-height:1.5;padding:8px 0 6px;
      margin:0;font-size:1.5rem;font-weight:750;letter-spacing:-.05em;white-space:normal;}
    .brand-symbol {display:inline-flex;align-items:center;justify-content:center;width:35px;height:35px;
      flex-shrink:0;border-radius:11px;background:#157663;color:#fff;font-size:1.35rem;box-shadow:0 4px 10px #15766320;}
    .ai-badge {color:#715595;background:#f0eaf8;padding:2px 6px;border-radius:5px;font-size:.65rem;letter-spacing:.03em;}
    .sidebar-label {font-size:.66rem;font-weight:700;letter-spacing:.12em;color:#708085;margin:12px 0 8px;}
    [data-testid="stSidebar"] [role="radiogroup"] {gap:5px;}
    [data-testid="stSidebar"] [role="radiogroup"] label {
      padding:10px 9px;border:1px solid transparent;border-radius:9px;min-height:44px;transition:background .15s;}
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {background:#f5f7f6;}
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
      background:#e9f4ee;border-color:#d3e7dd;box-shadow:inset 3px 0 0 #157663;}
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:focus-visible) {outline:2px solid #157663;outline-offset:2px;}
    [data-testid="stSidebar"] hr {margin:1rem 0;}
    .demo-notice {border:1px solid #eadfca;background:#fffaf0;color:#725924;padding:12px 16px;
      border-radius:10px;font-size:.8rem;margin:2px 0 16px;line-height:1.65;}
    .demo-notice b {display:inline-block;font-size:.67rem;letter-spacing:.09em;margin-right:12px;}
    .kpi-grid {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:0 0 24px;}
    .kpi {--accent:#157663;--tint:#edf7f2;--icon-bg:#dceee4;background:linear-gradient(140deg,#fff 50%,var(--tint));
      border:1px solid #e3e9e6;border-top:3px solid var(--accent);border-radius:15px;padding:19px 20px;
      min-width:0;box-shadow:0 4px 16px #263f3510;}
    .kpi-violet {--accent:#8064b0;--tint:#f5f0fb;--icon-bg:#eee5f9;}
    .kpi-gold {--accent:#a47727;--tint:#fcf6e9;--icon-bg:#f5eacb;}
    .kpi-coral {--accent:#b96350;--tint:#fcf0ec;--icon-bg:#f7e2db;}
    .kpi-top {display:flex;gap:10px;align-items:center;min-height:38px;}
    .kpi-icon {display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;width:34px;height:34px;
      border-radius:10px;background:var(--icon-bg);color:var(--accent);}
    .kpi-icon svg {width:19px;height:19px;}
    .kpi-label {color:#53676d;font-size:.79rem;line-height:1.5;font-weight:550;overflow-wrap:anywhere;}
    .kpi-value {font-size:clamp(1.7rem,2.5vw,2.2rem);font-weight:700;line-height:1.3;letter-spacing:-.045em;margin:14px 0 8px;color:var(--ink);overflow-wrap:anywhere;}
    .kpi-note {color:#617278;font-size:.75rem;line-height:1.6;}
    .feature {border-left:3px solid #b99955;padding:3px 0 3px 15px;margin:12px 0 18px;}
    .feature p {color:#5e7278;font-size:.88rem;line-height:1.75;margin:8px 0 0;}
    [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stForm"] {
      background:#fff;border-radius:15px;border-color:#e2e8e5;box-shadow:0 3px 14px #243d3510;}
    .audit-hero {background:linear-gradient(115deg,#ecf6f0 0%,#f7f4ec 58%,#f1edf8 100%);
      border:1px solid #dde9df;border-radius:18px;padding:30px;margin:0 0 22px;}
    .audit-hero h2 {font-size:clamp(1.5rem,2.4vw,2rem);line-height:1.3;margin:8px 0 12px;padding:0;max-width:700px;}
    .audit-hero p {max-width:690px;color:#536c69;font-size:.95rem;line-height:1.8;margin:0;}
    .hero-tags {display:flex;gap:8px;flex-wrap:wrap;margin-top:18px;}
    .hero-tags span {background:#ffffffc9;border:1px solid #dde5df;padding:5px 10px;border-radius:7px;font-size:.72rem;color:#4b6560;}
    @media(max-width:1100px) {.kpi-grid {grid-template-columns:repeat(2,minmax(0,1fr));}}
    @media(max-width:850px) {
      [data-testid="stHorizontalBlock"] {flex-wrap:wrap;}
      [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {width:100% !important;flex:1 1 100% !important;min-width:0 !important;}}
    @media(max-width:600px) {
      [data-testid="stMainBlockContainer"], .main .block-container {padding:5rem 1rem 2rem;}
      .kpi-grid {grid-template-columns:1fr;gap:12px;}.kpi {padding:17px;}
      .eyebrow {font-size:.63rem;letter-spacing:.07em;line-height:1.9;}
      .audit-hero {padding:20px;}.header-meta {gap:6px 10px;}}
    </style>""", unsafe_allow_html=True)


def page_header(page, company, research_loaded=False):
    status = ('<span class="demo-pill">Research draft</span><span>Unverified source material</span>'
              if research_loaded else
              '<span class="demo-pill">Demo workspace</span><span>Synthetic data</span>')
    st.markdown(f'<header class="brand-header"><div class="eyebrow">BRANDLENS AI / INTELLIGENCE WORKSPACE</div>'
                f'<h1>{escape(page)}</h1><div class="header-meta"><span>Workspace: {escape(company)}</span>'
                f'{status}</div></header>', unsafe_allow_html=True)


def kpis(items):
    # Decorative inline SVGs avoid external assets, fonts and platform-dependent emoji.
    paths = [
        '<path d="M3 17l5-5 4 3 8-10M15 5h5v5"/>',
        '<path d="M20 11a8 8 0 01-8 8H4l2-4a8 8 0 1114-4z"/><path d="M8 10h8M8 14h5"/>',
        '<path d="M4 20h16M6 16v-4M12 16V5M18 16V9"/>',
        '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    ]
    tones = ["teal", "violet", "gold", "coral"]
    cards = []
    for i, (label, value, note) in enumerate(items):
        icon = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[i % 4]}</svg>'
        cards.append(f'<div class="kpi kpi-{tones[i % 4]}"><div class="kpi-top"><span class="kpi-icon">{icon}</span>'
                     f'<div class="kpi-label">{escape(label)}</div></div><div class="kpi-value">{escape(str(value))}</div>'
                     f'<div class="kpi-note">{escape(note)}</div></div>')
    st.markdown('<div class="kpi-grid">' + ''.join(cards) + '</div>', unsafe_allow_html=True)


def feature(title, body):
    st.markdown(f'<div class="feature"><b>{escape(title)}</b><p>{escape(body)}</p></div>', unsafe_allow_html=True)


def audit_hero():
    st.markdown('<section class="audit-hero"><div class="eyebrow">YOUR NEXT STRATEGIC PERSPECTIVE</div>'
                '<h2>See the brand.<br>Find the opportunity.</h2>'
                '<p>Explore a structured view of positioning, consumer perception and digital presence — '
                'with a clear path from evidence to action.</p><div class="hero-tags">'
                '<span>Research pipeline available</span><span>7 analysis pages</span>'
                '<span>12-section report blueprint</span></div></section>', unsafe_allow_html=True)
