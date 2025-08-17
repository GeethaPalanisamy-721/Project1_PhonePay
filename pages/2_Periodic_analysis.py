import streamlit as st
import pandas as pd
import pymysql
from dotenv import load_dotenv
import os
import plotly.express as px
import json

# Load env variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Load geojson
@st.cache_data
def load_geojson():
    with open("C:/Users/Siva Sankar/Desktop/Python Workspace/MDTM46B/PhonePay/data/india_states.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

india_geojson = load_geojson()

st.set_page_config(page_title="PhonePe Data Analysis", layout="wide")
st.title("PhonePe India Map Analysis")

# Tabs
tab1, tab2 = st.tabs(["Yearly Analysis", "Quarterly Analysis"])

# ================================
# TAB 1 - YEARLY ANALYSIS
# ================================
with tab1:
    st.subheader("Yearly Analysis")
    analysis_type = st.selectbox("Select Data Type", ["Transactions", "Insurance", "Users"], key="yearly_type")
    if analysis_type == "Insurance":
        years = [2020,2021,2022,2023,2024]
    else:
        years = [2018, 2019, 2020, 2021, 2022, 2023,2024]
    year = st.selectbox("Select Year",years,key="yearly_year")

    conn = get_connection()
    if analysis_type == "Transactions":
        query = f"""
        SELECT State, SUM(Transaction_count) AS total_value
        FROM transaction_aggr
        WHERE Year = {year}
        GROUP BY State
        """
    elif analysis_type == "Insurance":
        query = f"""
        SELECT State, SUM(Transaction_count) AS total_value
        FROM insurance_aggr
        WHERE Year = {year}
        GROUP BY State
        """
    else:  # Users
        query = f"""
        SELECT State, SUM(registeredUsers) AS total_value
        FROM user_map
        WHERE Year = {year}
        GROUP BY State
        """

    df_yearly = pd.read_sql(query, conn)
    conn.close()

    # Map
    fig_yearly = px.choropleth(
        df_yearly,
        geojson=india_geojson,
        featureidkey="properties.ST_NM",
        locations="State",
        color="total_value",
        color_continuous_scale="Viridis",
        title=f"{analysis_type} in {year} (Yearly)"
    )
    fig_yearly.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_yearly, use_container_width=True)

    # Top 10 states with ranking
    st.subheader(f"Top 10 States for {analysis_type} in {year}")
    df_top10_yearly = df_yearly.sort_values(by="total_value", ascending=False).head(10).reset_index(drop=True)
    df_top10_yearly.index += 1  # Start ranking at 1
    df_top10_yearly.index.name = "Rank"

    # Layout: Bar chart + Table
    col1, col2 = st.columns([2, 1])

    with col1:
        fig_bar_yearly = px.bar(
            df_top10_yearly,
            x="total_value",
            y=df_top10_yearly.index,
            orientation="h",
            text="total_value",
            title=f"Top 10 States by {analysis_type} ({year})",
            labels={"total_value": "Count", "y": "Rank"}
        )
        fig_bar_yearly.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        st.plotly_chart(fig_bar_yearly, use_container_width=True)

    with col2:
        st.dataframe(df_top10_yearly)

# ================================
# TAB 2 - QUARTERLY ANALYSIS
# ================================
with tab2:
    st.subheader("Quarterly Analysis")

    
    analysis_type_q = st.selectbox("Select Data Type", ["Transactions", "Insurance", "Users"], key="quarterly_type")
    if analysis_type_q == "Insurance":
        years = [2020,2021,2022,2023,2024]
    else:
        years = [2018, 2019, 2020, 2021, 2022, 2023,2024]
    year_q = st.selectbox("Select Year", years, key="quarterly_year")
    quarter = st.selectbox("Select Quarter", [1, 2, 3, 4], key="quarterly_quarter")

    conn = get_connection()
    if analysis_type_q == "Transactions":
        query = f"""
        SELECT State, SUM(Transaction_count) AS total_value
        FROM transaction_aggr
        WHERE Year = {year_q} AND Quarter = {quarter}
        GROUP BY State
        """
    elif analysis_type_q == "Insurance":
        query = f"""
        SELECT State, SUM(Transaction_count) AS total_value
        FROM insurance_aggr
        WHERE Year = {year_q} AND Quarter = {quarter}
        GROUP BY State
        """
    else:  # Users
        query = f"""
        SELECT State, SUM(registeredUsers) AS total_value
        FROM user_map
        WHERE Year = {year_q} AND Quarter = {quarter}
        GROUP BY State
        """

    df_quarterly = pd.read_sql(query, conn)
    conn.close()

    # Map
    fig_quarterly = px.choropleth(
        df_quarterly,
        geojson=india_geojson,
        featureidkey="properties.ST_NM",
        locations="State",
        color="total_value",
        color_continuous_scale="Viridis",
        title=f"{analysis_type_q} in {year_q} Q{quarter}"
    )
    fig_quarterly.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_quarterly, use_container_width=True)

    # Top 10 states with ranking
    st.subheader(f"Top 10 States for {analysis_type_q} in {year_q} Q{quarter}")
    df_top10_quarterly = df_quarterly.sort_values(by="total_value", ascending=False).head(10).reset_index(drop=True)
    df_top10_quarterly.index += 1  # Start ranking at 1
    df_top10_quarterly.index.name = "Rank"

    # Layout: Bar chart + Table
    col1, col2 = st.columns([2, 1])

    with col1:
        fig_bar_quarterly = px.bar(
            df_top10_quarterly,
            x="total_value",
            y=df_top10_quarterly.index,
            orientation="h",
            text="total_value",
            title=f"Top 10 States by {analysis_type_q} ({year_q} Q{quarter})",
            labels={"total_value": "Count", "y": "Rank"}
        )
        fig_bar_quarterly.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        st.plotly_chart(fig_bar_quarterly, use_container_width=True)

    with col2:
        st.dataframe(df_top10_quarterly)
