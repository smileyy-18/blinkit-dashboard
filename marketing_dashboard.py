import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Blinkit Marketing Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Blinkit Marketing Performance Dashboard")
st.markdown("Analyze campaign performance, revenue, spend, conversions, and ROAS.")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filter Data")

# Date filter
min_date = df["date"].min()
max_date = df["date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Convert to datetime
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Other filters
channel_filter = st.sidebar.multiselect(
    "Select Channel",
    options=df["channel"].unique(),
    default=df["channel"].unique()
)

campaign_filter = st.sidebar.multiselect(
    "Select Campaign",
    options=df["campaign_name"].unique(),
    default=df["campaign_name"].unique()
)

audience_filter = st.sidebar.multiselect(
    "Select Target Audience",
    options=df["target_audience"].unique(),
    default=df["target_audience"].unique()
)

# Apply filters
filtered_df = df[
    (df["date"] >= start_date) &
    (df["date"] <= end_date) &
    (df["channel"].isin(channel_filter)) &
    (df["campaign_name"].isin(campaign_filter)) &
    (df["target_audience"].isin(audience_filter))
]

# -------------------------------
# KPI Calculations
# -------------------------------
total_impressions = filtered_df["impressions"].sum()
total_clicks = filtered_df["clicks"].sum()
total_conversions = filtered_df["conversions"].sum()
total_spend = filtered_df["spend"].sum()
total_revenue = filtered_df["revenue_generated"].sum()

roas = total_revenue / total_spend if total_spend > 0 else 0
ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
cpc = total_spend / total_clicks if total_clicks > 0 else 0
cpa = total_spend / total_conversions if total_conversions > 0 else 0

# -------------------------------
# KPI Cards
# -------------------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Impressions", f"{total_impressions:,.0f}")
col2.metric("Clicks", f"{total_clicks:,.0f}")
col3.metric("Conversions", f"{total_conversions:,.0f}")
col4.metric("Spend", f"₹{total_spend:,.2f}")
col5.metric("Revenue", f"₹{total_revenue:,.2f}")
col6.metric("ROAS", f"{roas:.2f}")

col7, col8, col9 = st.columns(3)
col7.metric("CTR", f"{ctr:.2f}%")
col8.metric("Conversion Rate", f"{conversion_rate:.2f}%")
col9.metric("CPA", f"₹{cpa:.2f}")

st.markdown("---")

# -------------------------------
# Channel-wise Analysis
# -------------------------------
st.subheader("📢 Channel-wise Performance")

channel_perf = filtered_df.groupby("channel", as_index=False).agg({
    "impressions": "sum",
    "clicks": "sum",
    "conversions": "sum",
    "spend": "sum",
    "revenue_generated": "sum"
})
channel_perf["ROAS"] = channel_perf["revenue_generated"] / channel_perf["spend"]

col1, col2 = st.columns(2)

with col1:
    fig_channel_rev = px.bar(
        channel_perf,
        x="channel",
        y="revenue_generated",
        color="channel",
        title="Revenue by Channel"
    )
    st.plotly_chart(fig_channel_rev, use_container_width=True)

with col2:
    fig_channel_roas = px.bar(
        channel_perf,
        x="channel",
        y="ROAS",
        color="channel",
        title="ROAS by Channel"
    )
    st.plotly_chart(fig_channel_roas, use_container_width=True)

# -------------------------------
# Campaign-wise Analysis
# -------------------------------
st.subheader("🎯 Campaign-wise Performance")

campaign_perf = filtered_df.groupby("campaign_name", as_index=False).agg({
    "spend": "sum",
    "revenue_generated": "sum",
    "conversions": "sum"
})
campaign_perf["ROAS"] = campaign_perf["revenue_generated"] / campaign_perf["spend"]

col1, col2 = st.columns(2)

with col1:
    fig_campaign_rev = px.bar(
        campaign_perf.sort_values("revenue_generated", ascending=False),
        x="campaign_name",
        y="revenue_generated",
        color="campaign_name",
        title="Revenue by Campaign"
    )
    fig_campaign_rev.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_campaign_rev, use_container_width=True)

with col2:
    fig_campaign_roas = px.bar(
        campaign_perf.sort_values("ROAS", ascending=False),
        x="campaign_name",
        y="ROAS",
        color="campaign_name",
        title="ROAS by Campaign"
    )
    fig_campaign_roas.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_campaign_roas, use_container_width=True)

# -------------------------------
# Audience-wise Analysis
# -------------------------------
st.subheader("👥 Target Audience Analysis")

audience_perf = filtered_df.groupby("target_audience", as_index=False).agg({
    "spend": "sum",
    "revenue_generated": "sum",
    "conversions": "sum"
})
audience_perf["ROAS"] = audience_perf["revenue_generated"] / audience_perf["spend"]

col1, col2 = st.columns(2)

with col1:
    fig_audience_conv = px.pie(
        audience_perf,
        names="target_audience",
        values="conversions",
        title="Conversions by Target Audience"
    )
    st.plotly_chart(fig_audience_conv, use_container_width=True)

with col2:
    fig_audience_roas = px.bar(
        audience_perf,
        x="target_audience",
        y="ROAS",
        color="target_audience",
        title="ROAS by Target Audience"
    )
    st.plotly_chart(fig_audience_roas, use_container_width=True)

# -------------------------------
# Monthly Trend Analysis
# -------------------------------
st.subheader("📅 Monthly Trends")

filtered_df["month"] = filtered_df["date"].dt.to_period("M").astype(str)

monthly_perf = filtered_df.groupby("month", as_index=False).agg({
    "spend": "sum",
    "revenue_generated": "sum",
    "conversions": "sum"
})
monthly_perf["ROAS"] = monthly_perf["revenue_generated"] / monthly_perf["spend"]

col1, col2 = st.columns(2)

with col1:
    fig_monthly = px.line(
        monthly_perf,
        x="month",
        y=["spend", "revenue_generated"],
        title="Monthly Spend vs Revenue"
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

with col2:
    fig_monthly_roas = px.line(
        monthly_perf,
        x="month",
        y="ROAS",
        markers=True,
        title="Monthly ROAS Trend"
    )
    st.plotly_chart(fig_monthly_roas, use_container_width=True)

# -------------------------------
# Funnel Analysis
# -------------------------------
st.subheader("🛒 Marketing Funnel")

funnel_df = pd.DataFrame({
    "Stage": ["Impressions", "Clicks", "Conversions"],
    "Value": [total_impressions, total_clicks, total_conversions]
})

fig_funnel = px.funnel(
    funnel_df,
    x="Value",
    y="Stage",
    title="Marketing Funnel"
)
st.plotly_chart(fig_funnel, use_container_width=True)

# -------------------------------
# Detailed Data Table
# -------------------------------
st.subheader("📋 Filtered Data Table")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# Download Filtered Data
# -------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_blinkit_marketing_data.csv",
    mime="text/csv"
)