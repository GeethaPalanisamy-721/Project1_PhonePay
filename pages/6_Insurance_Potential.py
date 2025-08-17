import streamlit as st
import pandas as pd
import pymysql
from dotenv import load_dotenv
import os
import plotly.express as px

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# MySQL connection
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

st.set_page_config(page_title="Insurance Penetration", layout="wide")
st.title("Insurance Penetration")

# Create Tabs
tab1, tab2 = st.tabs(["Statewise Analysis", "State/Districtwise Analysis"])

# =========================
# TAB 1 : STATEWISE ANALYSIS
# =========================
with tab1:
    st.subheader("Statewise Transaction vs Insurance Amount")

    # Select Year
    year = st.selectbox("Select Year", [2020, 2021, 2022, 2023, 2024], key="year_tab1")

    # Fetch data from MySQL
    conn = get_connection()
    query = f"""
    SELECT t.State,
           SUM(t.Transaction_amount) AS total_transaction_amount,
           COALESCE(SUM(i.Transaction_amount), 0) AS total_insurance_amount
    FROM transaction_aggr t
    LEFT JOIN insurance_aggr i
           ON t.State = i.State
          AND t.Year = i.Year
          AND t.Quarter = i.Quarter
    WHERE t.Year = {year}
    GROUP BY t.State
    ORDER BY total_transaction_amount DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Add Insurance Penetration (%)
    df["insurance_penetration"] = (
        (df["total_insurance_amount"] / df["total_transaction_amount"]) * 100
    ).round(2)

    # ---- Bar Chart ----
    df_melt = df.melt(
        id_vars="State",
        value_vars=["total_transaction_amount", "total_insurance_amount"],
        var_name="Category",
        value_name="Amount"
    )

    df_melt["Category"] = df_melt["Category"].replace({
        "total_transaction_amount": "Transaction Amount",
        "total_insurance_amount": "Insurance Amount"
    })

    fig = px.bar(
        df_melt,
        x="State",
        y="Amount",
        color="Category",
        barmode="group",
        title=f"Transaction vs Insurance Amount by State ({year})",
        labels={"Amount": "Amount (₹)", "State": "State"},
        color_discrete_map={"Transaction Amount": "blue",
                            "Insurance Amount": "brown"}
    )

    # ---- Layout ----
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(f"Top 10 High-Transaction States Needing Insurance Push ({year})")

        # Top 10 by Transactions
        df_top10 = df.nlargest(10, "total_transaction_amount").copy()

        # Sort them by lowest insurance penetration %
        df_top10 = df_top10.sort_values(by="insurance_penetration", ascending=True)

        # Reset index for ranking
        df_top10 = df_top10.reset_index(drop=True)
        df_top10.index += 1
        df_top10.index.name = "Rank"

        # Show table
        st.dataframe(
            df_top10[["State", "total_transaction_amount", "total_insurance_amount", "insurance_penetration"]]
            .rename(columns={
                "total_transaction_amount": "Transaction Amount (₹)",
                "total_insurance_amount": "Insurance Amount (₹)",
                "insurance_penetration": "Insurance Penetration (%)"
            })
        )

# =========================
# TAB 2 : DISTRICTWISE ANALYSIS
# =========================
with tab2:
    st.subheader("Districtwise Transaction vs Insurance Amount")

    # Select State
    conn = get_connection()
    states_df = pd.read_sql("SELECT DISTINCT State FROM transaction_map ORDER BY State", conn)
    conn.close()
    state_selected = st.selectbox("Select State", states_df["State"], key="state_tab2")

    # Fetch Districts for that State
    conn = get_connection()
    districts_df = pd.read_sql(f"SELECT DISTINCT District FROM transaction_map WHERE State='{state_selected}' ORDER BY District", conn)
    conn.close()
    district_selected = st.selectbox("Select District", districts_df["District"], key="district_tab2")

    # Fetch districtwise data
    conn = get_connection()
    query_district = f"""
    SELECT t.Year,
           SUM(t.Transaction_amount) AS total_transaction_amount,
           COALESCE(SUM(i.Transaction_amount), 0) AS total_insurance_amount
    FROM transaction_map t
    LEFT JOIN insurance_map i
           ON t.State = i.State
          AND t.District = i.District
          AND t.Year = i.Year
          AND t.Quarter = i.Quarter
    WHERE t.State = '{state_selected}'
      AND t.District = '{district_selected}'
    GROUP BY t.Year
    ORDER BY t.Year
    """
    df_dist = pd.read_sql(query_district, conn)
    conn.close()

    # Melt dataframe for grouped bar chart
    df_dist_melt = df_dist.melt(
        id_vars="Year",
        value_vars=["total_transaction_amount", "total_insurance_amount"],
        var_name="Category",
        value_name="Amount"
    )

    df_dist_melt["Category"] = df_dist_melt["Category"].replace({
        "total_transaction_amount": "Transaction Amount",
        "total_insurance_amount": "Insurance Amount"
    })

    # Bar chart (Year vs Amount for that District)
    fig2 = px.bar(
        df_dist_melt,
        x="Year",
        y="Amount",
        color="Category",
        barmode="group",
        title=f"Yearly Transaction vs Insurance Amount in {district_selected}, {state_selected}",
        labels={"Amount": "Amount (₹)", "Year": "Year"},
        color_discrete_map={"Transaction Amount": "blue",
                            "Insurance Amount": "brown"}
    )
    st.plotly_chart(fig2, use_container_width=True)
