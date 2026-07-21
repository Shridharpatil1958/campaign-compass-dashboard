"""
Marketing ROI Analysis Pipeline
Prime Pulse Solutions – Intern Project
=======================================
Run this script after generate_data.py.
Outputs 5 clean CSV files ready to load into Power BI.
"""

import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings("ignore")

RAW  = "data/raw"
CLEAN = "data/cleaned"
OUT   = "powerbi_export"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 – Load raw files
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 55)
print("STEP 1: Loading raw data")
print("=" * 55)

ga4 = pd.read_csv(f"{RAW}/ga4_traffic.csv", parse_dates=["date"])
sc  = pd.read_csv(f"{RAW}/search_console.csv", parse_dates=["week_start"])
ads = pd.read_csv(f"{RAW}/ads_spend.csv")

print(f"  GA4 traffic  : {len(ga4):>5,} rows")
print(f"  Search Console: {len(sc):>4,} rows")
print(f"  Ads spend    : {len(ads):>5,} rows")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 – Clean GA4
# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 2: Cleaning GA4 traffic data")

# Clamp bounce_rate between 0 and 1
ga4["bounce_rate"] = ga4["bounce_rate"].clip(0, 1)

# Derived columns
ga4["conversion_rate"] = (ga4["conversions"] / ga4["sessions"]).round(4)
ga4["month"]           = ga4["date"].dt.to_period("M").astype(str)
ga4["week"]            = ga4["date"].dt.to_period("W").apply(lambda r: str(r.start_time.date()))
ga4["day_of_week"]     = ga4["date"].dt.day_name()
ga4["avg_session_duration_min"] = (ga4["avg_session_duration_sec"] / 60).round(2)

# Nulls check
nulls = ga4.isnull().sum().sum()
print(f"  Null values after cleaning : {nulls}")
print(f"  Date range : {ga4['date'].min().date()} → {ga4['date'].max().date()}")
print(f"  Channels   : {sorted(ga4['channel'].unique())}")

ga4.to_csv(f"{CLEAN}/ga4_clean.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 – Clean Search Console
# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 3: Cleaning Search Console data")

sc["ctr_pct"] = (sc["ctr"] * 100).round(2)
sc.to_csv(f"{CLEAN}/search_console_clean.csv", index=False)
print(f"  Keywords tracked : {sc['keyword'].nunique()}")
print(f"  Total impressions: {sc['impressions'].sum():,}")
print(f"  Total clicks     : {sc['clicks'].sum():,}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 – Clean & enrich Ads data
# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 4: Cleaning Ads spend data")

ads["month_dt"]  = pd.to_datetime(ads["month"])
ads["profit_inr"] = (ads["revenue_inr"] - ads["spend_inr"]).round(2)
ads["roi_pct"]    = ((ads["profit_inr"] / ads["spend_inr"]) * 100).round(1)
ads["ctr"]        = (ads["clicks"] / ads["impressions"]).round(4)

ads.to_csv(f"{CLEAN}/ads_clean.csv", index=False)
print(f"  Platforms  : {list(ads['platform'].unique())}")
print(f"  Campaigns  : {ads['campaign'].nunique()}")
print(f"  Total spend: ₹{ads['spend_inr'].sum():,.0f}")
print(f"  Total ROAS : {(ads['revenue_inr'].sum()/ads['spend_inr'].sum()):.2f}x")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 – Monthly summary (master table for Power BI)
# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 5: Building monthly channel summary")

# GA4 monthly aggregation
ga4_monthly = (
    ga4.groupby(["month", "channel"])
    .agg(
        sessions=("sessions", "sum"),
        users=("users", "sum"),
        new_users=("new_users", "sum"),
        pageviews=("pageviews", "sum"),
        conversions=("conversions", "sum"),
        avg_bounce_rate=("bounce_rate", "mean"),
        avg_session_dur_min=("avg_session_duration_min", "mean"),
    )
    .reset_index()
)
ga4_monthly["conversion_rate"] = (
    ga4_monthly["conversions"] / ga4_monthly["sessions"]
).round(4)
ga4_monthly["avg_bounce_rate"]    = ga4_monthly["avg_bounce_rate"].round(3)
ga4_monthly["avg_session_dur_min"] = ga4_monthly["avg_session_dur_min"].round(2)

# Ads monthly aggregation (by channel label to match GA4)
ads_monthly = (
    ads.groupby(["month", "platform"])
    .agg(spend_inr=("spend_inr","sum"),
         ad_clicks=("clicks","sum"),
         ad_conversions=("conversions","sum"),
         revenue_inr=("revenue_inr","sum"))
    .reset_index()
    .rename(columns={"platform":"ad_platform"})
)

print(f"  GA4 monthly rows : {len(ga4_monthly)}")
print(f"  Ads monthly rows : {len(ads_monthly)}")

ga4_monthly.to_csv(f"{OUT}/01_ga4_monthly_by_channel.csv", index=False)
ads_monthly.to_csv(f"{OUT}/02_ads_monthly_by_platform.csv", index=False)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 – Channel ROI summary table
# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 6: Computing channel ROI summary")

# Total GA4 per channel (all months)
ch_summary = (
    ga4.groupby("channel")
    .agg(total_sessions=("sessions","sum"),
         total_conversions=("conversions","sum"),
         avg_bounce=("bounce_rate","mean"),
         avg_duration_min=("avg_session_duration_min","mean"))
    .reset_index()
)
ch_summary["conversion_rate_pct"] = (
    ch_summary["total_conversions"] / ch_summary["total_sessions"] * 100
).round(2)
ch_summary["avg_bounce"] = (ch_summary["avg_bounce"] * 100).round(1)
ch_summary["avg_duration_min"] = ch_summary["avg_duration_min"].round(2)

# Merge paid channel spend
paid_totals = (
    ads.groupby("platform")
    .agg(total_spend=("spend_inr","sum"),
         total_revenue=("revenue_inr","sum"),
         total_ad_convs=("conversions","sum"))
    .reset_index()
)
# Map platform names to GA4 channel names
platform_map = {"Google Ads": "Paid Search", "Meta Ads": "Social Media"}
paid_totals["channel"] = paid_totals["platform"].map(platform_map)

ch_summary = ch_summary.merge(paid_totals[["channel","total_spend","total_revenue","total_ad_convs"]],
                               on="channel", how="left")
ch_summary["total_spend"]   = ch_summary["total_spend"].fillna(0)
ch_summary["total_revenue"] = ch_summary["total_revenue"].fillna(0)
ch_summary["cpa_inr"]       = (ch_summary["total_spend"] / ch_summary["total_ad_convs"].replace(0, np.nan)).round(0)
ch_summary["roas"]          = (ch_summary["total_revenue"] / ch_summary["total_spend"].replace(0, np.nan)).round(2)
ch_summary["roi_pct"]       = ((ch_summary["total_revenue"] - ch_summary["total_spend"]) / ch_summary["total_spend"].replace(0, np.nan) * 100).round(1)

ch_summary.to_csv(f"{OUT}/03_channel_roi_summary.csv", index=False)

print("\n  Channel ROI Summary:")
print(f"  {'Channel':<22} {'Sessions':>9} {'Conv Rate':>10} {'Spend (₹)':>11} {'ROAS':>7}")
print("  " + "-" * 62)
for _, r in ch_summary.sort_values("total_sessions", ascending=False).iterrows():
    roas = f"{r['roas']:.2f}x" if not pd.isna(r["roas"]) else "  N/A"
    crs  = f"{r['conversion_rate_pct']:.2f}%"
    spend = f"₹{r['total_spend']:,.0f}" if r["total_spend"] > 0 else "  Organic"
    print(f"  {r['channel']:<22} {r['total_sessions']:>9,} {crs:>10} {spend:>11} {roas:>7}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 – Campaign performance table
# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 7: Campaign performance export")

camp_summary = (
    ads.groupby(["campaign","platform","quality_score"])
    .agg(total_spend=("spend_inr","sum"),
         total_clicks=("clicks","sum"),
         total_convs=("conversions","sum"),
         total_revenue=("revenue_inr","sum"),
         avg_cpc=("cpc","mean"),
         avg_cpa=("cpa","mean"),
         avg_roas=("roas","mean"))
    .reset_index()
)
camp_summary["roi_pct"]  = ((camp_summary["total_revenue"] - camp_summary["total_spend"]) / camp_summary["total_spend"] * 100).round(1)
camp_summary["avg_cpc"]  = camp_summary["avg_cpc"].round(2)
camp_summary["avg_cpa"]  = camp_summary["avg_cpa"].round(2)
camp_summary["avg_roas"] = camp_summary["avg_roas"].round(3)
camp_summary.to_csv(f"{OUT}/04_campaign_performance.csv", index=False)
print(f"  Campaigns exported: {len(camp_summary)}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 – Daily traffic (for trend charts in Power BI)
# ─────────────────────────────────────────────────────────────────────────────
daily = (
    ga4.groupby("date")
    .agg(total_sessions=("sessions","sum"),
         total_users=("users","sum"),
         total_conversions=("conversions","sum"),
         total_pageviews=("pageviews","sum"))
    .reset_index()
)
daily["rolling_7d_sessions"] = daily["total_sessions"].rolling(7, min_periods=1).mean().round(0)
daily.to_csv(f"{OUT}/05_daily_traffic.csv", index=False)
print(f"\nSTEP 8: Daily traffic export → {len(daily)} rows")

# ─────────────────────────────────────────────────────────────────────────────
# DONE
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("ALL DONE — Power BI files ready in /powerbi_export/")
print("=" * 55)
print("\nFiles created:")
for f in sorted(os.listdir(OUT)):
    size = os.path.getsize(f"{OUT}/{f}")
    print(f"  {f:<45} {size:>7,} bytes")
