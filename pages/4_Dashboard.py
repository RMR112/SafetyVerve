import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from db.database import fetch_all

st.set_page_config(page_title="Incident Dashboard", page_icon="📊", layout="wide")
st.title("📊 Incident Analytics Dashboard")

# Load companies
companies = fetch_all("SELECT company_id, name FROM companies")
company_options = {name: cid for cid, name in companies}
selected_company = st.selectbox("Select Company", list(company_options.keys()))
selected_company_id = company_options[selected_company]

# Query data
query = f"""
SELECT
    it.type_name AS incident_type,
    sv.label AS severity,
    p.project_name AS project,
    DATE(inc.incident_datetime) AS incident_date
FROM incidents inc
JOIN incident_types it ON it.type_id = inc.incident_type_id
JOIN severity_levels sv ON sv.severity_id = inc.severity_id
LEFT JOIN projects p ON p.project_id = inc.project_id
WHERE inc.company_id = {selected_company_id}
"""
conn = sqlite3.connect("incident_db.sqlite")
df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    st.warning("No incidents found for this company.")
    st.stop()

# Chart 1: Incidents by Type
type_count = df["incident_type"].value_counts().reset_index()
type_count.columns = ["Incident Type", "Count"]
fig1 = px.bar(type_count, x="Incident Type", y="Count", title="Incidents by Type", text="Count")

# Chart 2: Incidents by Severity
severity_count = df["severity"].value_counts().reset_index()
severity_count.columns = ["Severity", "Count"]
fig2 = px.pie(severity_count, names="Severity", values="Count", title="Incidents by Severity")

# Chart 3: Incidents over Time (Line Chart)
df["incident_date"] = pd.to_datetime(df["incident_date"])
df["month"] = df["incident_date"].dt.to_period("M").astype(str)
month_count = df["month"].value_counts().sort_index().reset_index()
month_count.columns = ["Month", "Count"]
fig3 = px.line(month_count, x="Month", y="Count", title="Incidents Over Time", markers=True)

# Chart 4: Incidents by Project
project_count = df["project"].value_counts().reset_index()
project_count.columns = ["Project", "Count"]
fig4 = px.bar(project_count, x="Project", y="Count", title="Incidents by Project", text="Count")

# Layout charts
st.subheader(f"📌 Dashboard for {selected_company}")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.plotly_chart(fig4, use_container_width=True)
