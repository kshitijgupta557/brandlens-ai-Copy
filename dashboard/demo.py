"""Synthetic fixtures only; never observations about a real brand."""
DIMENSIONS = [
    {"Dimension": "Brand clarity", "Score": 82},
    {"Dimension": "Digital presence", "Score": 74},
    {"Dimension": "Consumer trust", "Score": 78},
    {"Dimension": "Differentiation", "Score": 61},
    {"Dimension": "Content consistency", "Score": 67},
]
HEALTH = round(sum(row["Score"] for row in DIMENSIONS) / len(DIMENSIONS))
TREND = [{"Period": f"Month {i + 1}", "Score": n} for i, n in enumerate([58, 61, 60, 66, 69, HEALTH])]
COMPETITORS = [
    {"Brand": "Sample Brand", "Health score": HEALTH, "Voice share": 28},
    {"Brand": "Peer A", "Health score": 81, "Voice share": 35},
    {"Brand": "Peer B", "Health score": 68, "Voice share": 22},
    {"Brand": "Peer C", "Health score": 63, "Voice share": 15},
]
SENTIMENT = [{"Sentiment": label, "Percent": value} for label, value in [("Positive", 64), ("Neutral", 24), ("Negative", 12)]]
CHANNELS = [{"Channel": label, "Score": value} for label, value in [("Website", 82), ("Search", 74), ("Social", 66)]]
THEMES = [
    {"Theme": "Product experience", "Sample mentions": 420, "Hypothetical signal": "Positive"},
    {"Theme": "Value for money", "Sample mentions": 310, "Hypothetical signal": "Mixed"},
    {"Theme": "Packaging", "Sample mentions": 270, "Hypothetical signal": "Positive"},
    {"Theme": "Availability", "Sample mentions": 200, "Hypothetical signal": "Mixed"},
]
PRIORITIES = [
    {"title": "Sharpen the reason to choose", "area": "Positioning", "priority": "P1",
     "hypothesis": "A clearer benefit statement could help a brand stand apart.",
     "action": "Test two benefit statements with the target audience before changing messaging.",
     "evidence": "Competitor message inventory, interviews and a controlled message test.",
     "owner": "Brand marketing", "window": "Days 1–30", "metric": "Message comprehension and preference"},
    {"title": "Connect discovery to the product", "area": "Digital experience", "priority": "P2",
     "hypothesis": "Consistent product information could reduce uncertainty before purchase.",
     "action": "Review landing pages and test a clearer product explanation.",
     "evidence": "Page inventory, consented analytics and usability interviews.",
     "owner": "Digital marketing", "window": "Days 31–60", "metric": "Qualified product-page engagement"},
    {"title": "Close the listening loop", "area": "Consumer experience", "priority": "P3",
     "hypothesis": "Repeated service questions could reveal a useful content opportunity.",
     "action": "Validate recurring themes, then test a concise customer FAQ.",
     "evidence": "Dated feedback with a documented sampling method and appropriate permissions.",
     "owner": "Customer experience", "window": "Days 61–90", "metric": "Repeat contact rate and CSAT"},
]
