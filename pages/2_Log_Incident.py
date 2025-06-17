import streamlit as st
from db.database import fetch_all, execute_query
from datetime import datetime

st.set_page_config(page_title="Log Incident", page_icon="📋")

st.title("📋 Log a Workplace Incident")

# Step 1: Select company outside the form
companies = fetch_all("SELECT company_id, name FROM companies")
company_map = {name: cid for cid, name in companies}
selected_company = st.selectbox("Select Company", list(company_map.keys()))
company_id = company_map[selected_company]

# Step 2: Dynamically filter based on company
projects = fetch_all("SELECT project_id, company_id, project_name FROM projects WHERE company_id = ?", (company_id,))
divisions = fetch_all("SELECT division_id, company_id, division_name FROM divisions WHERE company_id = ?", (company_id,))
employees = fetch_all("SELECT employee_id, name FROM employees WHERE company_id = ?", (company_id,))

incident_types = fetch_all("SELECT type_id, type_name FROM incident_types")
severity_levels = fetch_all("SELECT severity_id, label FROM severity_levels")

# Step 3: Prepare dropdowns
project_map = {pname: pid for pid, _, pname in projects}
division_map = {dname: did for did, _, dname in divisions}
employee_map = {ename: eid for eid, ename in employees}
incident_type_map = {label: tid for tid, label in incident_types}
severity_map = {label: sid for sid, label in severity_levels}

# Step 4: Begin form
with st.form("incident_form"):
    employee = st.selectbox("Employee", list(employee_map.keys()))
    project = st.selectbox("Project", list(project_map.keys()))
    division = st.selectbox("Division", list(division_map.keys()))

    incident_type = st.selectbox("Incident Type", list(incident_type_map.keys()))
    severity = st.selectbox("Severity Level", list(severity_map.keys()))

    incident_date = st.date_input("Incident Date", value=datetime.today())
    incident_time = st.time_input("Incident Time", value=datetime.now().time())
    incident_datetime = datetime.combine(incident_date, incident_time)

    location = st.text_input("Location of Incident")
    reported_by = st.text_input("Reported By")
    description = st.text_area("Incident Description")

    submitted = st.form_submit_button("Log Incident")

    if submitted:
        if not location.strip() or not reported_by.strip() or not description.strip():
            st.warning("Please fill all required fields.")
        else:
            execute_query(
                """
                INSERT INTO incidents (
                    company_id, project_id, division_id, employee_id,
                    incident_type_id, severity_id,
                    incident_datetime, location, reported_by, description, report_datetime
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    company_id,
                    project_map[project],
                    division_map[division],
                    employee_map[employee],
                    incident_type_map[incident_type],
                    severity_map[severity],
                    incident_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    location.strip(),
                    reported_by.strip(),
                    description.strip(),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )
            st.success("✅ Incident logged successfully.")
