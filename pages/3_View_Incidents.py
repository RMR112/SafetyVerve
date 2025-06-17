import streamlit as st
from db.database import fetch_all
import pandas as pd

st.set_page_config(page_title="View Incidents", page_icon="🗂️")

st.title("🗂️ Incident Report Viewer")

# Load base dropdown data
companies = fetch_all("SELECT company_id, name FROM companies")
projects = fetch_all("SELECT project_id, project_name, company_id FROM projects")
divisions = fetch_all("SELECT division_id, division_name, company_id FROM divisions")
severity_levels = fetch_all("SELECT severity_id, label FROM severity_levels")

# Create filters
company_map = {name: cid for cid, name in companies}
project_map = {(pname, cid): pid for pid, pname, cid in projects}
division_map = {(dname, cid): did for did, dname, cid in divisions}
severity_map = {label: sid for sid, label in severity_levels}

# Sidebar Filters
st.sidebar.header("🔎 Filters")

selected_company = st.sidebar.selectbox("Company", ["All"] + list(company_map.keys()))
selected_severity = st.sidebar.selectbox("Severity", ["All"] + list(severity_map.keys()))

# Fetch incidents with joins
query = """
    SELECT
        inc.incident_id,
        c.name AS company,
        p.project_name,
        d.division_name,
        emp.name AS employee,
        it.type_name AS incident_type,
        sv.label AS severity,
        inc.incident_datetime,
        inc.location,
        inc.reported_by,
        inc.description
    FROM incidents inc
    JOIN companies c ON c.company_id = inc.company_id
    JOIN employees emp ON emp.employee_id = inc.employee_id
    JOIN incident_types it ON it.type_id = inc.incident_type_id
    JOIN severity_levels sv ON sv.severity_id = inc.severity_id
    LEFT JOIN projects p ON p.project_id = inc.project_id
    LEFT JOIN divisions d ON d.division_id = inc.division_id
    ORDER BY inc.incident_datetime DESC
"""
rows = fetch_all(query)
df = pd.DataFrame(rows, columns=[
    "Incident ID", "Company", "Project", "Division", "Employee",
    "Type", "Severity", "Date/Time", "Location", "Reported By", "Description"
])

# Apply filters
if selected_company != "All":
    df = df[df["Company"] == selected_company]

if selected_severity != "All":
    df = df[df["Severity"] == selected_severity]

# Display
st.subheader(f"📄 Showing {len(df)} incident(s)")
st.dataframe(df, use_container_width=True)

# Optional: download
csv = df.to_csv(index=False)
st.download_button("📤 Download CSV", data=csv, file_name="incident_report.csv", mime="text/csv")
