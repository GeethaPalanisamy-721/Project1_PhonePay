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

# MySQL connection function
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

st.set_page_config(page_title="Analysis", layout="wide")
st.title("Data Analysis")

# Dropdown selection
analysis_type = st.selectbox("Select Analysis", [
    "Insurance Expansion",
    "Transaction Growth",
    "User Registration Trends"
])

conn = get_connection()

if analysis_type == "Insurance Expansion":
    query = """
    SELECT Year, SUM(Transaction_count) AS Total_insurance_count
    FROM insurance_aggr
    GROUP BY Year
    ORDER BY Year
    """
    df = pd.read_sql(query, conn)
    fig = px.line(df, x="Year", y="Total_insurance_count", markers=True,
                  title="Insurance Growth Over Years")
    st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "Transaction Growth":
    query = """
    SELECT Year, SUM(Transaction_count) AS Total_transactions_count
    FROM transaction_aggr
    GROUP BY Year
    ORDER BY Year
    """
    df = pd.read_sql(query, conn)
    fig = px.line(df, x="Year", y="Total_transactions_count", markers=True,
                 title="Transaction Growth Over Years")
    st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "User Registration Trends":
    query = """
    SELECT Year, SUM(registeredUsers) AS Total_users
    FROM user_top
    GROUP BY Year
    ORDER BY Year
    """
    df = pd.read_sql(query, conn)
    fig = px.line(df, x="Year", y="Total_users", markers=True,
                  title="User Registration Growth Over Years")
    st.plotly_chart(fig, use_container_width=True)

conn.close()
