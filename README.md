# Campaign Compass

Marketing performance and ROI dashboard built in Power BI, covering sessions, conversions, ad spend, ROAS, and campaign-level ROI across channels and platforms.
<img width="1027" height="570" alt="1000448590" src="https://github.com/user-attachments/assets/2c2af0cd-1178-4d96-919f-ea41b4af5258" />


## Pages

| Page | What it shows |
|---|---|
| [Overview](#overview) | Sessions, conversions, spend, and ROAS at a glance, plus channel and campaign breakdowns |
| [Channel Performance](#channel-performance) | Best channel, conversion rate, session duration, and bounce rate by month and channel |
| [Ad Spend & ROAS](#ad-spend--roas) | Ad spend vs revenue, ROAS gauge against target, CPC by platform, revenue waterfall |
| [Campaign Performance](#campaign-performance) | Top ROI and lowest CPA campaigns, spend and revenue by campaign, quality score table |
| [Daily Traffic & Trends](#daily-traffic--trends) | Daily sessions, 7-day rolling average, and daily conversions by platform |

## Tech stack

- Power BI Desktop
- Data sources: GA4 (sessions, channels), Google Ads / Meta Ads (spend, conversions, ROAS), campaign performance tables
- Custom Inforiver visual for channel spend/revenue/ROAS status

## Key metrics tracked

- Total sessions and conversions, conversion rate %, bounce rate %
- Ad spend, ad revenue, ROAS, CPA, CPC
- Campaign-level ROI %, quality score, top/lowest performers
- Daily traffic trend with 7-day rolling average

## Screenshots

### Overview
Total sessions, conversions, spend, and ROAS, with a monthly trend line, channel breakdown, campaign donut, and summary table.

<img width="1027" height="570" alt="1000448590" src="https://github.com/user-attachments/assets/1d5ff252-f838-4187-9397-f904ddd43267" />


### Channel Performance
Best-performing channel, conversion rate, session duration, and bounce rate, broken down by month and channel.

<img width="1009" height="574" alt="1000448591" src="https://github.com/user-attachments/assets/1010b203-c91a-442e-9a52-c5f353354fea" />


### Ad Spend & ROAS
Ad spend vs revenue by month, ROAS against target on a gauge, CPC by platform, and a revenue waterfall by ad platform.

<img width="990" height="567" alt="1000448592" src="https://github.com/user-attachments/assets/d7a7224f-faa0-4654-8ae5-caaa2b100448" />


### Campaign Performance
Top ROI campaign, lowest CPA campaign, revenue and spend by campaign, and a full campaign quality/ROI table.

<img width="1019" height="574" alt="1000448593" src="https://github.com/user-attachments/assets/85e646b2-6860-43ec-b1cd-e2b8010ac5a4" />


### Daily Traffic & Trends
Peak day sessions, average daily sessions, 7-day rolling sessions, and daily conversions by platform.

<img width="994" height="559" alt="1000448594" src="https://github.com/user-attachments/assets/173d480a-df31-4592-a258-6f2ea92fe075" />


## Setup

1. Clone this repo.
2. Open `Campaign_Compass.pbix` in Power BI Desktop.
3. Update the data source connections under **Transform data → Data source settings** to point to your own GA4 and Ads data.
4. Refresh the data model.

## Repo structure

```
├── Campaign_Compass.pbix
├── README.md
└── screenshots/
    ├── 01-overview.png
    ├── 02-channel-performance.png
    ├── 03-ad-spend-roas.png
    ├── 04-campaign-performance.png
    └── 05-daily-traffic-trends.png
```
