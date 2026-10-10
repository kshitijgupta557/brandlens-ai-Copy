"""Altair charts using inline synthetic data; no network fetches."""
import altair as alt
import streamlit as st
from dashboard import demo
TEAL = "#397f70"
GOLD = "#b59a62"

def show(chart):
    chart = chart.properties(height=260).configure_view(strokeWidth=0).configure_axis(
        gridColor="#edf0f2", domain=False, tickSize=0, labelColor="#67757d",
        titleColor="#67757d", labelPadding=10, titlePadding=14,
    ).configure_legend(title=None, orient="bottom", labelColor="#67757d")
    st.altair_chart(chart, width="stretch", theme=None)

def trend():
    chart = alt.Chart(alt.Data(values=demo.TREND)).encode(
        x=alt.X("Period:O", title=None, sort=[r["Period"] for r in demo.TREND], axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Score:Q", title="Illustrative score / 100", scale=alt.Scale(domain=[0, 100])),
        tooltip=["Period:O", "Score:Q"],
    )
    show(chart.mark_area(color=TEAL, opacity=.09) + chart.mark_line(color=TEAL, strokeWidth=3, point=True))

def bars(rows, label, value, title, color=TEAL):
    show(alt.Chart(alt.Data(values=rows)).mark_bar(color=color, cornerRadiusEnd=4, size=22).encode(
        y=alt.Y(f"{label}:N", sort=None, title=None),
        x=alt.X(f"{value}:Q", title=title, scale=alt.Scale(domain=[0, 100])),
        tooltip=[f"{label}:N", f"{value}:Q"],
    ))

def sentiment():
    show(alt.Chart(alt.Data(values=demo.SENTIMENT)).mark_arc(innerRadius=75, outerRadius=112).encode(
        theta=alt.Theta("Percent:Q"),
        color=alt.Color("Sentiment:N", scale=alt.Scale(domain=["Positive", "Neutral", "Negative"],
                       range=[TEAL, "#c5cdd1", "#bc806d"])),
        tooltip=["Sentiment:N", alt.Tooltip("Percent:Q", title="Percent (demo)")],
    ))
