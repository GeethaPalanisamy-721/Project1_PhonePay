import streamlit as st
import pandas as pd
import pymysql
from dotenv import load_dotenv
import os
import plotly.express as px
import json

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# -------------------------------
# Connect to MySQL
# -------------------------------
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# -------------------------------
# Load India GeoJSON from local file
# -------------------------------
@st.cache_data
def load_geojson():
    with open("C:/Users/Siva Sankar/Desktop/Python Workspace/MDTM46B/PhonePay/data/india_states.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

india_geojson = load_geojson()

# -------------------------------
# Streamlit Config
# -------------------------------
st.set_page_config(page_title="PhonePe Summary", layout="wide")
st.title("PhonePe India Summary (2020 - 2024)")

# -------------------------------
# Tabs for Metrics
# -------------------------------
tab1, tab2, tab3 = st.tabs(["Insurance", "Transactions", "Users"])

# -------------------------------
# Function to fetch data (Last 5 Years Only)
# -------------------------------
def fetch_data(metric):
    conn = get_connection()
    query_map = {
        "Transactions": """
            SELECT State, SUM(Transaction_count) AS value 
            FROM transaction_aggr 
            WHERE Year BETWEEN 2020 AND 2024
            GROUP BY State
        """,
        "Insurance": """
            SELECT State, SUM(Transaction_count) AS value 
            FROM insurance_aggr 
            WHERE Year BETWEEN 2020 AND 2024
            GROUP BY State
        """,
        "Users": """
            SELECT State, SUM(registeredUsers) AS value 
            FROM user_top 
            WHERE Year BETWEEN 2020 AND 2024
            GROUP BY State
        """
    }
    df = pd.read_sql(query_map[metric], conn)
    conn.close()
    return df

# -------------------------------
# Reusable function to draw chart + table
# -------------------------------
def render_tab(metric):
    df = fetch_data(metric)
    total_value = int(df["value"].sum())

    # Choropleth map
    fig = px.choropleth(
        df,
        geojson=india_geojson,
        featureidkey="properties.ST_NM",
        locations="State",
        color="value",
        color_continuous_scale="Viridis",
        title=f"{metric} (2020-2024, State-wise)",
    )
    fig.update_geos(fitbounds="locations", visible=False)

    # Layout: Map left, Top states + Summary right
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric(label=f"🇮🇳 Total {metric} (India, 2020-2024)", value=f"{total_value:,}")
        st.subheader(f"Top 10 States by {metric}")
        df_top10 = df.sort_values(by="value", ascending=False).head(10).reset_index(drop=True)
        df_top10.index += 1
        df_top10.index.name = "Rank"
        st.dataframe(df_top10)

# -------------------------------
# Render Each Tab
# -------------------------------
with tab1:
    render_tab("Insurance")

with tab2:
    render_tab("Transactions")

with tab3:
    render_tab("Users")
