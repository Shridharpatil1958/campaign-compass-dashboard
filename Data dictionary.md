# Data Dictionary

Reference for the fields and measures used across Campaign Compass.

## Sessions & Traffic

| Field | Description | Source |
|---|---|---|
| `total_sessions` | Count of sessions in the period | GA4 |
| `channel` | Traffic channel (Organic Search, Paid Search, Direct, Social Media, Referral, Email) | GA4 |
| `total_conversions` | Count of conversion events | GA4 |
| `conversion_rate_%` | `total_conversions / total_sessions` | Calculated |
| `avg_bounce_rate_%` | Average bounce rate for the period | GA4 |
| `avg_session_duration` | Average session length (minutes) | GA4 |
| `7d_rolling_sessions` | 7-day rolling average of daily sessions | Calculated |

## Ad Spend & ROAS

| Field | Description | Source |
|---|---|---|
| `total_ad_spend` | Total spend across ad platforms | Google Ads / Meta Ads |
| `total_ad_revenue` | Total attributed revenue | Google Ads / Meta Ads |
| `roas` | `total_ad_revenue / total_ad_spend` | Calculated |
| `roas_target` | Target ROAS benchmark | Business input |
| `roas_status` | On Target / Below Target / Above Target flag | Calculated |
| `cpa_inr` | Cost per acquisition (INR) | Calculated |
| `cpc_inr` | Cost per click (INR) | Google Ads / Meta Ads |
| `ad_platform` | Google Ads or Meta Ads | Ad platform export |

## Campaigns

| Field | Description | Source |
|---|---|---|
| `campaign` | Campaign name | Ad platform export |
| `platform` | Google Ads or Meta Ads | Ad platform export |
| `total_spend` | Spend by campaign | Ad platform export |
| `total_revenue` | Revenue attributed to campaign | Ad platform export |
| `roi_%` | `(total_revenue - total_spend) / total_spend` | Calculated |
| `quality_score_%` | Platform-reported quality/relevance score | Ad platform export |

## Notes

- All currency values are in INR (₹) unless otherwise labeled.
- Monthly figures are aggregated from daily-level source data.
- Update this file whenever a new field or measure is added to the model.
