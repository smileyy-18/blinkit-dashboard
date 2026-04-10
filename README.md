# 📊 Blinkit Marketing Performance Dashboard

## 🚀 Project Overview
This project is an interactive data analytics dashboard built using **Streamlit** to analyze Blinkit's marketing campaign performance. It transforms raw marketing data into actionable business insights through intuitive visualizations and KPI tracking.

The dashboard provides insights into:
* **Campaign Effectiveness:** Identifying which strategies drive the most value.
* **Channel Performance:** Comparing Email, SMS, App, and Social Media.
* **Audience Segmentation:** Understanding behavior across New vs. Premium segments.
* **Revenue vs. Spend:** Visualizing ROI and budget efficiency.
* **Conversion Funnel:** Tracking the journey from Impression to Sale.

---

## 📁 Dataset Description
The analysis is based on a dataset containing **5,400 rows** covering marketing activities from **March 2023 to November 2024**.

**Key Metrics Tracked:**
* `campaign_name`: Type of marketing campaign.
* `target_audience`: Audience segments (New, Premium, etc.).
* `channel`: Platform used (Email, SMS, App, Social Media).
* `roas`: Return on Ad Spend ($Revenue / Spend$).
* `conversions`: Completed actions (purchases/signups).

---

## 📊 Dashboard Features

### 🔹 KPI Metrics
* **Total Reach:** Impressions, Clicks, and Conversions.
* **Financials:** Total Spend, Total Revenue, and ROAS.
* **Efficiency:** CTR (Click Through Rate), Conversion Rate, and CPA (Cost Per Acquisition).

### 🔹 Interactive Filters
* **Date Range:** Filter performance over specific periods.
* **Categorical Filters:** Drill down by Channel, Campaign, or Audience segment.

### 🔹 Visualizations
* **Revenue & ROAS Analysis:** Bar charts and trend lines by Channel and Campaign.
* **Audience Insights:** Conversion breakdown by user type.
* **Growth Trends:** Monthly Spend vs. Revenue tracking.
* **Marketing Funnel:** Visual representation of user drop-off rates.

---

## 🛠️ Technologies Used
* **Python** - Core logic
* **Pandas** - Data manipulation and cleaning
* **Plotly** - Interactive data visualizations
* **Streamlit** - Web framework for dashboard deployment

---

## ▶️ How to Run the Project

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
