import streamlit as st
import pandas as pd
import pymysql
from dotenv import load_dotenv
import os
import plotly.express as px

# ---------------- LOAD ENV ----------------
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ---------------- MYSQL CONNECTION ----------------
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Transaction Dynamics", layout="wide")
st.title("Transaction Dynamics")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs([" Overall Trends", "Detailed by State/District"])

# ---------- TAB 1 (Your First Page) ----------
with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        conn = get_connection()
        query = """
        SELECT Year, Transaction_type, SUM(Transaction_count) AS total_transactions
        FROM transaction_aggr
        GROUP BY Year, Transaction_type
        ORDER BY Year, Transaction_type
        """
        df = pd.read_sql(query, conn)
        conn.close()

        fig = px.bar(
            df,
            x="Year",
            y="total_transactions",
            color="Transaction_type",
            barmode="group",
            title="Transaction Type Trends Over Years",
            labels={"total_transactions": "Transaction Count"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        conn = get_connection()
        query_summary = """
        SELECT Transaction_type, SUM(Transaction_count) AS total_transactions
        FROM transaction_aggr
        GROUP BY Transaction_type
        ORDER BY total_transactions desc
        """
        df_summary = pd.read_sql(query_summary, conn)
        conn.close()

        st.subheader("Transaction Type Summary (All Years)")
        st.dataframe(df_summary, use_container_width=True,hide_index=True)


# ---------- TAB 2 (Your Second Page) ----------
with tab2:
    conn = get_connection()

    # Dropdown for State
    state_query = "SELECT DISTINCT State FROM transaction_map ORDER BY State;"
    states = pd.read_sql(state_query, conn)["State"].tolist()
    selected_state = st.selectbox("Select State", states)

    # Dropdown for District (dependent on State)
    district_query = f"""
    SELECT DISTINCT District 
    FROM transaction_map 
    WHERE State = '{selected_state}'
    ORDER BY District;
    """
    districts = pd.read_sql(district_query, conn)["District"].tolist()
    selected_district = st.selectbox("Select District", districts)

    # Toggle metric
    metric = st.radio(
        "Select Metric",
        ("Transaction Count", "Transaction Amount"),
        horizontal=True
    )
    metric_col = "Transaction_count" if metric == "Transaction Count" else "Transaction_amount"

    # Chart Data
    query_chart = f"""
    SELECT a.Year, a.Transaction_type, SUM(a.{metric_col}) AS metric_value
    FROM transaction_aggr a
    JOIN transaction_map m
      ON a.State = m.State AND a.Year = m.Year AND a.Quarter = m.Quarter
    WHERE m.State = '{selected_state}' AND m.District = '{selected_district}'
    GROUP BY a.Year, a.Transaction_type
    ORDER BY a.Year, a.Transaction_type;
    """
    df_chart = pd.read_sql(query_chart, conn)

    # Table Data
    query_table = f"""
    SELECT a.Transaction_type, SUM(a.{metric_col}) AS metric_value
    FROM transaction_aggr a
    JOIN transaction_map m
      ON a.State = m.State AND a.Year = m.Year AND a.Quarter = m.Quarter
    WHERE m.State = '{selected_state}' AND m.District = '{selected_district}'
    GROUP BY a.Transaction_type
    ORDER BY metric_value DESC;
    """
    df_table = pd.read_sql(query_table, conn)
    conn.close()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Yearly {metric} Trends - {selected_district}, {selected_state}")
        fig = px.bar(
            df_chart,
            x="Year",
            y="metric_value",
            color="Transaction_type",
            barmode="group",
            labels={"metric_value": metric},
            title=f"{metric} by Transaction Type Over Years"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(f"{metric} Summary by Transaction Type (All Years)")
        st.dataframe(df_table, use_container_width=True,hide_index=True)
