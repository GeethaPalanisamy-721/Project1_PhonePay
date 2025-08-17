import streamlit as st
import pandas as pd
import pymysql
from dotenv import load_dotenv
import os
import plotly.express as px

# ---------------- DB CONNECTION ----------------
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

st.set_page_config(page_title="User Engagement Analysis", layout="wide")
st.title("User Engagement Analysis")

tab1, tab2 = st.tabs(["Overall Trends", "State/District-wise Analysis"])

# ---------------- TAB 1: OVERALL TRENDS ----------------
with tab1:
    conn = get_connection()

    # Year dropdown
    years = pd.read_sql("SELECT DISTINCT Year FROM user_map ORDER BY Year;", conn)["Year"].tolist()
    selected_year = st.selectbox("Select Year", years)

    # Query for state-level users & app opens
    query_overall = f"""
        SELECT State, SUM(registeredUsers) AS total_users, SUM(AppOpens) AS total_appopens
        FROM user_map
        WHERE Year = {selected_year}
        GROUP BY State
        ORDER BY State;
    """
    df_overall = pd.read_sql(query_overall, conn)

    # Bar chart comparing AppOpens vs RegisteredUsers
    df_melt = df_overall.melt(id_vars="State", value_vars=["total_users", "total_appopens"],
                              var_name="Metric", value_name="Count")

    st.subheader(f"Overall User Engagement by State - {selected_year}")
    fig = px.bar(
        df_melt,
        x="State",
        y="Count",
        color="Metric",
        barmode="group",
        title=f"Registered Users vs App Opens by State ({selected_year})",
        color_discrete_map={
            "total_users": "royalblue",     # Registered Users = Blue
            "total_appopens": "orange"      # App Opens = Orange
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    # Top 5 and Bottom 5 states by Registered Users
    df_ranked = df_overall.sort_values("total_users", ascending=False).reset_index(drop=True)

    # Top 5
    top5 = df_ranked.head(5).copy().reset_index(drop=True)
    top5["Rank"] = range(1, len(top5) + 1)

    # Bottom 5
    bottom5 = df_ranked.tail(5).copy().reset_index(drop=True)
    bottom5 = bottom5.sort_values("total_users").reset_index(drop=True)
    bottom5["Rank"] = range(1, len(bottom5) + 1)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 States (Registered Users)")
        st.dataframe(top5[["Rank", "State", "total_users"]].reset_index(drop=True), use_container_width=True,hide_index=True)
    with col2:
        st.subheader("Bottom 5 States (Registered Users)")
        st.dataframe(bottom5[["Rank", "State", "total_users"]].reset_index(drop=True), use_container_width=True,hide_index=True)

    conn.close()

# ---------------- TAB 2: STATE/DISTRICT ----------------
with tab2:
    conn = get_connection()

    # State dropdown
    state_query = "SELECT DISTINCT State FROM user_map ORDER BY State;"
    states = pd.read_sql(state_query, conn)["State"].tolist()
    selected_state = st.selectbox("Select State", states)

    # District dropdown (dependent on state)
    district_query = f"""
        SELECT DISTINCT District FROM user_map WHERE State = '{selected_state}' ORDER BY District;
    """
    districts = pd.read_sql(district_query, conn)["District"].tolist()
    selected_district = st.selectbox("Select District", districts)

    # Query for State/District analysis
    query_district = f"""
        SELECT Year, SUM(registeredUsers) AS total_users, SUM(AppOpens) AS total_appopens
        FROM user_map
        WHERE State = '{selected_state}' AND District = '{selected_district}'
        GROUP BY Year
        ORDER BY Year;
    """
    df_district = pd.read_sql(query_district, conn)

    df_district_melt = df_district.melt(id_vars="Year", value_vars=["total_users", "total_appopens"],
                                        var_name="Metric", value_name="Count")

    st.subheader(f"User Engagement Trends in {selected_district}, {selected_state}")
    fig2 = px.bar(
        df_district_melt,
        x="Year",
        y="Count",
        color="Metric",
        barmode="group",
        title=f"Yearly User Engagement in {selected_district}, {selected_state}",
        color_discrete_map={
            "total_users": "royalblue",     # Registered Users = Blue
            "total_appopens": "orange"      # App Opens = Orange
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

    conn.close()
