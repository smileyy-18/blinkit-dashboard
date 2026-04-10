import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

st.title("📊 Blinkit Marketing Dashboard ")

# -------------------------------
# KPIs
# -------------------------------
total_spend = df["spend"].sum()
total_revenue = df["revenue_generated"].sum()
roas = total_revenue / total_spend

st.write(f"**Total Spend:** ₹{total_spend:,.2f}")
st.write(f"**Total Revenue:** ₹{total_revenue:,.2f}")
st.write(f"**ROAS:** {roas:.2f}")

# -------------------------------
# Channel-wise Revenue
# -------------------------------
st.subheader("📢 Revenue by Channel")

channel_data = df.groupby("channel")["revenue_generated"].sum()

fig1, ax1 = plt.subplots()
ax1.bar(channel_data.index, channel_data.values)
ax1.set_xlabel("Channel")
ax1.set_ylabel("Revenue")
ax1.set_title("Revenue by Channel")

st.pyplot(fig1)

# -------------------------------
# Campaign-wise ROAS
# -------------------------------
st.subheader("🎯 ROAS by Campaign")

campaign = df.groupby("campaign_name").agg({
    "spend": "sum",
    "revenue_generated": "sum"
})

campaign["ROAS"] = campaign["revenue_generated"] / campaign["spend"]

fig2, ax2 = plt.subplots()
ax2.barh(campaign.index, campaign["ROAS"])
ax2.set_xlabel("ROAS")
ax2.set_title("ROAS by Campaign")

st.pyplot(fig2)

# -------------------------------
# Monthly Trend
# -------------------------------
st.subheader("📅 Monthly Spend vs Revenue")

df["month"] = df["date"].dt.to_period("M").astype(str)

monthly = df.groupby("month").agg({
    "spend": "sum",
    "revenue_generated": "sum"
})

fig3, ax3 = plt.subplots()
ax3.plot(monthly.index, monthly["spend"], marker='o', label="Spend")
ax3.plot(monthly.index, monthly["revenue_generated"], marker='o', label="Revenue")

ax3.set_xlabel("Month")
ax3.set_ylabel("Amount")
ax3.set_title("Monthly Trend")
ax3.legend()

plt.xticks(rotation=45)

st.pyplot(fig3)

# -------------------------------
# Funnel Chart (Simple Version)
# -------------------------------
st.subheader("🛒 Marketing Funnel")

impressions = df["impressions"].sum()
clicks = df["clicks"].sum()
conversions = df["conversions"].sum()

funnel_labels = ["Impressions", "Clicks", "Conversions"]
funnel_values = [impressions, clicks, conversions]

fig4, ax4 = plt.subplots()
ax4.bar(funnel_labels, funnel_values)
ax4.set_title("Marketing Funnel")

st.pyplot(fig4)