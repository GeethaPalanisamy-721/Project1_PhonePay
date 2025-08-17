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

# Page Config
st.set_page_config(page_title="Top Mobile Brands", layout="wide")
st.title("Top Mobile Brands")

# --- Get Data ---
conn = get_connection()
query = """
    SELECT Brand, SUM(Count) AS total_users
    FROM user_aggr
    GROUP BY Brand
    ORDER BY total_users DESC;
"""
df = pd.read_sql(query, conn)
conn.close()

# --- Prepare Top 10 + Others ---
top10 = df.head(10).copy()
others_sum = df["total_users"].iloc[5:].sum()

if others_sum > 0:
    top10.loc[len(top10.index)] = ["Others", others_sum]

# --- Add Rank ---
top10.reset_index(drop=True, inplace=True)
top10.insert(0, "Rank", range(1, len(top10) + 1))

# --- Layout: Chart Left, Table Right ---
col1, col2 = st.columns([2, 1])  # chart takes 2/3, table 1/3

with col1:
    # Pie Chart with good color variety
    fig = px.pie(
        top10,
        names="Brand",
        values="total_users",
        title="Top 10 Mobile Brands using PhonePay",
        hole=0.3,  # donut style
        color_discrete_sequence=px.colors.qualitative.Set3  # better color set
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Data Summary")
    st.dataframe(top10, hide_index=True)
