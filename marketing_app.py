import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Paid Media Dashboard", layout="wide")
st.title("📊 Paid Media Channels Performance Dashboard")

# Constants
AVG_ORDER_VALUE = 500  # ₹500 assumed for ROAS

# Load Data
fb = pd.read_csv("data/facebook_campaigns.csv", parse_dates=['date'])
ig = pd.read_csv("data/instagram_campaigns.csv", parse_dates=['date'])
sfmc = pd.read_csv("data/sfmc_email_campaigns.csv", parse_dates=['date'])

# Add platform label
fb['platform'] = 'Facebook'
ig['platform'] = 'Instagram'
sfmc['platform'] = 'SFMC'
sfmc.rename(columns={"emails_sent": "impressions", "opens": "clicks"}, inplace=True)
sfmc['spend'] = 0  # Dummy spend for SFMC

# Merge and calculate KPIs
common_cols = ['date', 'campaign_name', 'impressions', 'clicks', 'conversions', 'spend', 'platform']
df = pd.concat([fb[common_cols], ig[common_cols], sfmc[common_cols]], ignore_index=True)

# Replace 0 to avoid division by zero
df['impressions'] = df['impressions'].replace(0, 1)
df['conversions'] = df['conversions'].replace(0, 1)
df['spend'] = df['spend'].replace(0, 1)

# KPIs
df['CTR (%)'] = round((df['clicks'] / df['impressions']) * 100, 2)
df['CPA'] = round(df['spend'] / df['conversions'], 2)
df['ROAS'] = round((df['conversions'] * AVG_ORDER_VALUE) / df['spend'], 2)

# Sidebar filters
st.sidebar.header("🔍 Filter")
platforms = st.sidebar.multiselect("Platform", options=df['platform'].unique(), default=df['platform'].unique())
date_range = st.sidebar.date_input("Date Range", [df['date'].min(), df['date'].max()])

filtered_df = df[
    (df['platform'].isin(platforms)) &
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
]

# Aggregated metrics
st.subheader("📌 Summary Metrics by Platform")
agg_df = filtered_df.groupby('platform').agg({
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum',
    'spend': 'sum'
}).reset_index()

# Calculate KPIs at platform level
agg_df['CTR (%)'] = round((agg_df['clicks'] / agg_df['impressions']) * 100, 2)
agg_df['CPA'] = round(agg_df['spend'] / agg_df['conversions'], 2)
agg_df['ROAS'] = round((agg_df['conversions'] * AVG_ORDER_VALUE) / agg_df['spend'], 2)

st.dataframe(agg_df)

# Time Series Chart
st.subheader("📈 Clicks Over Time by Platform")
chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x='date:T',
    y='clicks:Q',
    color='platform:N',
    tooltip=['date:T', 'campaign_name', 'clicks', 'CTR (%)']
).interactive()

st.altair_chart(chart, use_container_width=True)

# Campaign Table
st.subheader("📋 Campaign-Level Data")
campaign_list = filtered_df[['date', 'campaign_name', 'platform', 'impressions', 'clicks', 'conversions', 'spend', 'CTR (%)', 'CPA', 'ROAS']]
selected_row = st.dataframe(campaign_list, use_container_width=True)

# Drilldown
selected_campaign = st.selectbox("🔎 Select a campaign to drill down", options=filtered_df['campaign_name'].unique())

if selected_campaign:
    st.markdown(f"### 📌 Drilldown: `{selected_campaign}`")
    drill_df = filtered_df[filtered_df['campaign_name'] == selected_campaign]
    
    kpis = drill_df[['CTR (%)', 'CPA', 'ROAS']].mean().to_frame().T.round(2)
    st.write("**Average KPIs:**")
    st.dataframe(kpis)

    line_chart = alt.Chart(drill_df).mark_line(point=True).encode(
        x='date:T',
        y='clicks:Q',
        color='platform:N',
        tooltip=['date:T', 'clicks', 'CTR (%)', 'CPA', 'ROAS']
    ).interactive()

    st.altair_chart(line_chart, use_container_width=True)
