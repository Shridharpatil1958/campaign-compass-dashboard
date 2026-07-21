import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 6, 30)
dates = pd.date_range(START_DATE, END_DATE, freq="D")

# ── helpers ──────────────────────────────────────────────────────────────────
def seasonal(dates, base, amplitude=0.25):
    """Add a gentle weekly seasonality (weekends dip) + slow upward trend."""
    trend  = np.linspace(1.0, 1.3, len(dates))
    weekly = 1 - amplitude * (dates.dayofweek >= 5).astype(float)
    noise  = np.random.normal(1.0, 0.05, len(dates))
    return np.maximum(0, base * trend * weekly * noise).astype(int)

# ─────────────────────────────────────────────────────────────────────────────
# 1. GA4 TRAFFIC DATA
# ─────────────────────────────────────────────────────────────────────────────
channels = ["Organic Search", "Paid Search", "Social Media", "Direct", "Referral", "Email"]
base_sessions = {"Organic Search": 180, "Paid Search": 90, "Social Media": 60,
                 "Direct": 70, "Referral": 30, "Email": 25}
conv_rates    = {"Organic Search": 0.032, "Paid Search": 0.048, "Social Media": 0.018,
                 "Direct": 0.041, "Referral": 0.027, "Email": 0.055}
avg_session_dur = {"Organic Search": 185, "Paid Search": 142, "Social Media": 98,
                   "Direct": 210, "Referral": 155, "Email": 170}  # seconds
bounce_rates    = {"Organic Search": 0.42, "Paid Search": 0.51, "Social Media": 0.67,
                   "Direct": 0.38, "Referral": 0.48, "Email": 0.35}

ga4_rows = []
for ch in channels:
    sessions = seasonal(dates, base_sessions[ch])
    for i, d in enumerate(dates):
        s = max(1, sessions[i])
        c = max(0, np.random.binomial(s, conv_rates[ch]))
        ga4_rows.append({
            "date": d.strftime("%Y-%m-%d"),
            "channel": ch,
            "sessions": s,
            "users": max(1, int(s * np.random.uniform(0.78, 0.92))),
            "new_users": max(0, int(s * np.random.uniform(0.55, 0.72))),
            "conversions": c,
            "bounce_rate": round(bounce_rates[ch] + np.random.normal(0, 0.03), 3),
            "avg_session_duration_sec": max(30, int(avg_session_dur[ch] + np.random.normal(0, 20))),
            "pageviews": max(s, int(s * np.random.uniform(1.8, 3.5))),
        })

ga4_df = pd.DataFrame(ga4_rows)
ga4_df.to_csv("data/raw/ga4_traffic.csv", index=False)
print(f"GA4 rows: {len(ga4_df):,}  |  total sessions: {ga4_df['sessions'].sum():,}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. GOOGLE SEARCH CONSOLE DATA  (top keywords, weekly)
# ─────────────────────────────────────────────────────────────────────────────
keywords = [
    ("IT staffing company Nagpur", 4.2),
    ("manpower solutions India",   6.1),
    ("contract staffing services", 5.8),
    ("web development company Nagpur", 7.3),
    ("payroll management services", 4.9),
    ("digital marketing agency Nagpur", 8.1),
    ("ecommerce website development", 9.4),
    ("IT recruitment agency", 5.5),
    ("graphic design services Nagpur", 6.7),
    ("on-site manpower support", 3.8),
    ("permanent staffing solutions", 4.4),
    ("product management consulting", 11.2),
]

weeks = pd.date_range(START_DATE, END_DATE, freq="W-MON")
sc_rows = []
for kw, avg_pos in keywords:
    base_imp = int(500 / avg_pos * np.random.uniform(0.7, 1.3))
    for w in weeks:
        imp  = max(10, int(base_imp * np.random.uniform(0.8, 1.2)))
        ctr  = max(0.01, min(0.35, (1 / avg_pos) * np.random.uniform(0.8, 1.2)))
        clicks = max(0, int(imp * ctr))
        sc_rows.append({
            "week_start": w.strftime("%Y-%m-%d"),
            "keyword": kw,
            "impressions": imp,
            "clicks": clicks,
            "ctr": round(ctr, 4),
            "avg_position": round(avg_pos + np.random.normal(0, 0.5), 1),
        })

sc_df = pd.DataFrame(sc_rows)
sc_df.to_csv("data/raw/search_console.csv", index=False)
print(f"Search Console rows: {len(sc_df):,}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. ADS SPEND DATA  (Google Ads + Meta Ads, campaign level, monthly)
# ─────────────────────────────────────────────────────────────────────────────
campaigns = [
    # (name, platform, monthly_budget_INR, avg_cpc, quality)
    ("Brand Awareness – Google",    "Google Ads", 8000,  12.5, "good"),
    ("Lead Gen – IT Staffing",      "Google Ads", 15000, 18.2, "good"),
    ("Retargeting – Web Dev",       "Google Ads", 6000,  9.8,  "average"),
    ("Nagpur Local – Staffing",     "Meta Ads",   10000, 7.4,  "good"),
    ("Awareness – Digital Mktg",    "Meta Ads",   7500,  5.1,  "poor"),
    ("Lead Gen – Payroll Services", "Meta Ads",   9000,  8.9,  "average"),
]

conv_val_INR = 2500  # avg value of one conversion

months = pd.date_range(START_DATE, END_DATE, freq="MS")
ads_rows = []
for name, platform, budget, cpc, quality in campaigns:
    conv_rate_map = {"good": 0.055, "average": 0.031, "poor": 0.014}
    for m in months:
        spend = budget * np.random.uniform(0.88, 1.05)
        clicks = max(1, int(spend / cpc * np.random.uniform(0.9, 1.1)))
        cr     = conv_rate_map[quality] * np.random.uniform(0.85, 1.15)
        convs  = max(0, int(clicks * cr))
        revenue = convs * conv_val_INR * np.random.uniform(0.9, 1.1)
        ads_rows.append({
            "month": m.strftime("%Y-%m"),
            "campaign": name,
            "platform": platform,
            "spend_inr": round(spend, 2),
            "impressions": max(clicks, int(clicks * np.random.uniform(8, 25))),
            "clicks": clicks,
            "conversions": convs,
            "revenue_inr": round(revenue, 2),
            "cpc": round(spend / clicks, 2),
            "cpa": round(spend / max(1, convs), 2),
            "roas": round(revenue / max(1, spend), 3),
            "quality_score": quality,
        })

ads_df = pd.DataFrame(ads_rows)
ads_df.to_csv("data/raw/ads_spend.csv", index=False)
print(f"Ads rows: {len(ads_df):,}  |  total spend: ₹{ads_df['spend_inr'].sum():,.0f}")
print("\nAll raw files saved to data/raw/")
