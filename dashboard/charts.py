"""Accessible categorical colours and inline synthetic data; no network fetches."""
import altair as alt
import streamlit as st
from dashboard import demo

TEAL = "#23836e"
GOLD = "#b28a3a"
VIOLET = "#8c70ba"
CORAL = "#cb7967"
PALETTE = [TEAL, VIOLET, GOLD, CORAL, "#789a96"]


def show(chart):
    chart = chart.properties(height=270).configure_view(strokeWidth=0).configure_axis(
        gridColor="#edf0f2", domain=False, tickSize=0, labelColor="#52676c",
        titleColor="#52676c", labelPadding=9, titlePadding=14,
        labelFontSize=11, titleFontSize=11,
    ).configure_legend(title=None, orient="bottom", columns=1, labelColor="#52676c", labelFontSize=12, symbolSize=100)
    st.altair_chart(chart, width="stretch", theme=None)


def trend():
    chart = alt.Chart(alt.Data(values=demo.TREND)).encode(
        x=alt.X("Period:O", title=None, sort=[r["Period"] for r in demo.TREND], axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        y=alt.Y("Score:Q", title="Illustrative score / 100", scale=alt.Scale(domain=[0, 100])),
        tooltip=[alt.Tooltip("Period:O", title="Demo period"), alt.Tooltip("Score:Q", title="Mock score / 100")],
    )
    show(chart.mark_area(color=TEAL, opacity=.1)
         + chart.mark_line(color=TEAL, strokeWidth=3, point=alt.OverlayMarkDef(filled=True, size=60))
         + chart.mark_text(dy=-14, color="#28594f", fontSize=11).encode(text="Score:Q"))


def bars(rows, label, value, title, color=TEAL):
    # The same category colour is reused across competitor charts. Axis labels
    # and values keep the chart interpretable without relying on colour alone.
    names = [row[label] for row in rows]
    colors = PALETTE if color == TEAL else [GOLD, VIOLET, TEAL, CORAL, "#789a96"]
    if label == "Brand":
        colors = PALETTE
    base = alt.Chart(alt.Data(values=rows)).encode(
        y=alt.Y(f"{label}:N", sort=names, title=None, axis=alt.Axis(labelLimit=150)),
        x=alt.X(f"{value}:Q", title=title, scale=alt.Scale(domain=[0, 110]), axis=alt.Axis(values=[0, 25, 50, 75, 100])),
        tooltip=[alt.Tooltip(f"{label}:N"), alt.Tooltip(f"{value}:Q", title=title + " (demo)")],
    )
    bars = base.mark_bar(cornerRadiusEnd=5, size=23).encode(
        color=alt.Color(f"{label}:N", scale=alt.Scale(domain=names, range=colors[:len(names)]), legend=None))
    labels = base.mark_text(align="left", dx=6, fontSize=12, color="#415b61").encode(text=alt.Text(f"{value}:Q", format=".0f"))
    show(bars + labels)


def sentiment():
    rows = [{**row, "Label": f"{row['Percent']}%"} for row in demo.SENTIMENT]
    chart = alt.Chart(alt.Data(values=rows)).encode(
        theta=alt.Theta("Percent:Q", stack=True),
        order=alt.Order("Sentiment:N", sort="ascending"),
        color=alt.Color("Sentiment:N", scale=alt.Scale(
            domain=["Positive", "Neutral", "Negative"], range=[TEAL, VIOLET, CORAL])),
        tooltip=["Sentiment:N", alt.Tooltip("Percent:Q", title="Percent (demo)")],
    )
    arc = chart.mark_arc(innerRadius=60, outerRadius=95, stroke="#fff", strokeWidth=3)
    labels = chart.mark_text(radius=112, fontSize=12, fontWeight=600).encode(text="Label:N", color=alt.value("#415b61"))
    show(arc + labels)
