# SQL Web Analytics — Unveiling Trends & Strategies in Political Advocacy

This repository houses SQL queries, data analysis scripts, and an **interactive Streamlit dashboard** focused on website analytics. These tools are designed to generate insights specifically tailored for a fictional web team within a prominent political advocacy organization. The queries cover various aspects such as user engagement, revenue analysis, and page views over time. The repository includes both a Streamlit app and Tableau visualizations alongside recommendations based on the analysis performed. The exercises are structured to demonstrate proficiency in SQL querying, data analysis, and presentation of insights to support decision-making processes.

---

## 🚀 Interactive Dashboard

An interactive version of this analysis is available as a **Streamlit web app** — run it locally or deploy it for free in minutes.

### Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Deploy to Streamlit Community Cloud (Free)

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the entry point
4. Click **Deploy** — live in ~2 minutes

### App Features

| Page | Description |
|------|-------------|
| 📊 Executive Summary | KPI cards, top-level overview charts |
| 📱 Device Analysis | Revenue, avg gift size, and page preference by device |
| 🔗 Referral Sources | Traffic acquisition breakdown |
| 📄 Page Performance | Monthly trends, Q1/Q2 homepage comparisons |
| 💰 Donor Insights | Lifetime value rankings |
| ⏰ Time Patterns | Day-of-week analysis for visits and donations |
| 🔍 Query Explorer | Run your own SQL live against the embedded database |

All data is embedded directly in `app.py` and loaded into an in-memory SQLite database at startup — no external files or database setup required.

### Stack

| Tool | Purpose |
|------|---------|
| Streamlit | App framework |
| SQLite (stdlib) | In-memory database |
| Pandas | Data manipulation |
| Plotly Express | Interactive charts |

---

## Report

## Key Insights and Recommendations:

### Device Segmentation:
Understanding user behavior across various devices is essential. iOS users emerge as the top revenue generators, signaling the need for a mobile-first approach in design and functionality. Conversely, Windows users, contributing larger average gift sizes, might benefit from tailored messaging to encourage more frequent donations. The discernible trends among user segments underscore the significance of customized strategies to optimize revenue and engagement.

The data underscores distinct trends among user segments regarding revenue and average gift size. iOS users lead as the highest revenue generators, accumulating a total of $2066. Meanwhile, Windows users boast the highest average gift size, averaging $45 per donation, ranking second in overall revenue.

Conversely, Android users lag behind in both revenue and average gift size metrics, indicating a potential correlation between user profiles and donor value. It's plausible that younger, more affluent demographics gravitate towards iOS devices which foster a culture of frequent, on-the-go donations, consequently driving higher revenue figures. To reinforce this trend, consider expanding donation options, such as iMessage/SMS-to-donate functionality, to further engage iOS users and capitalize on their propensity for charitable giving. Meanwhile, optimizing engagement with Android users is crucial, considering their potentially limited UI/UX experiences compared to iOS users, which may contribute to lower lifetime value and donation size.

We may conjecture that older donors, typically possessing higher net worth, may favor Windows devices for their donation activities. While their contributions may be less frequent, their inclination towards larger donations could be attributed to their higher net worth and perhaps a preference for 'traditional' computing devices such as desktops and laptops.

![Sheet 2](https://github.com/k10sj02/aclu-web-analytics-sql/assets/35823259/13332e78-e625-41c9-9720-baef93a738da)

### Engagement Analysis:
Our data uncovers valuable insights into user behavior on our website. The issues page emerges as the focal point of activity, closely followed by news and homepage. iOS users demonstrate a notable preference for the issues page, likely reflecting a younger demographic's interest in trending topics. Conversely, Windows users, often more mature and deeply committed to the organization, gravitate towards blog content which helps them to feel like a part of the mission. Enhancing individualized user content and calls-to-action on these pages could substantially boost engagement and conversions.

![monthly-page-visits](https://github.com/k10sj02/aclu-web-analytics-sql/assets/35823259/d0381bc4-686a-4802-8317-32f08beed370)

### Referral Source Analysis:

Google easily emerges as the primary driver of traffic, followed by Twitter and Facebook which account for a much smaller share of referrals. Double down on high referral score from Google by enhancing search engine optimization (SEO) practices to boost click-through rate.

Notably, Instagram yielded the fewest referrals, with only 7 URL conversions, despite its popularity among youth, superior UX/UI, and affiliation with Facebook, our third-largest referral source. This might stem from Instagram's inclination towards aspirational lifestyle content, ads, and micro-blogging, with less emphasis on political discourse and advocacy. However, this ripe landscape appears to be evolving, with Instagram maturing (i.e. the new "Facebook") and the social media realm witnessing consolidation amidst the decline of platforms like Twitter and Facebook.

Considering these shifts, piloting an Instagram engagement strategy tailored to youth, and leveraging politically active influencers and celebrities like Hasan Piker and Cynthia Nixon, could present promising opportunities for our organization's outreach efforts. As older social media platforms experience a decline in engagement, I would suggest conducting further ROI research to determine whether we should scale up or scale down our acquisition efforts on Facebook and Twitter. However, based on current insights, I would maintain our current approach for the time being.

### Time Analysis:
Fridays emerge as the peak day for both page visits and donations, emphasizing the significance of scheduling campaigns and communications during high-engagement periods.

### Donor Value:
Identifying and engaging active donors, such as Donor 164904200849, who has made significant contributions, is crucial for sustaining support. Creating user personas for top donors can provide valuable insights into the motivations and behaviors of this cohort, aiding in donor retention and engagement efforts.

### Follow-up Questions for the Web Team:
1. What specific metrics or KPIs does the Web team prioritize, and how do they align with organizational goals?
2. Are there particular user segments or demographics that the Web team aims to target, and how can we tailor web experiences to meet their preferences?
3. What UX research and testing methodologies are currently employed, and have any usability issues been identified by users?
4. How does the Web team track and measure the effectiveness of marketing campaigns and website optimizations?
5. Are there any ongoing or planned initiatives related to website redesign, content strategy, or technology upgrades that could impact the analysis and recommendations provided?

By collaboratively addressing these questions, we can refine our insights and recommendations to closely align with the Web team's objectives, fostering meaningful improvements to the web experience.

---

## Data

- **Period:** March 2020 – March 2022 (7 quarters)
- `page_views` — 149 rows
- `conversions` — 98 rows