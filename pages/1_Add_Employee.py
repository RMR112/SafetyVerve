import streamlit as st
from db.database import fetch_all, execute_query

st.set_page_config(page_title="Add Employee", page_icon="🧑‍🏭")

st.title("🧑‍💼 Add New Employee")

# Load companies from DB
companies = fetch_all("SELECT company_id, name FROM companies")
company_options = {name: cid for cid, name in companies}

with st.form("employee_form"):
    name = st.text_input("Employee Name", max_chars=100)
    company = st.selectbox("Company", list(company_options.keys()))
    designation = st.text_input("Designation")
    age = st.number_input("Age", min_value=18, max_value=70)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    department = st.text_input("Department")

    submitted = st.form_submit_button("Add Employee")

    if submitted:
        if not name.strip():
            st.warning("Name is required.")
        else:
            company_id = company_options[company]
            execute_query(
                """
                INSERT INTO employees (company_id, name, designation, age, gender, department)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (company_id, name.strip(), designation, age, gender, department)
            )
            st.success(f"Employee '{name}' added successfully to {company}.")

# Show employee count per company (optional dashboard touch)
st.divider()
st.subheader("👥 Employee Count by Company")

counts = fetch_all("""
    SELECT c.name, COUNT(e.employee_id)
    FROM companies c
    LEFT JOIN employees e ON c.company_id = e.company_id
    GROUP BY c.name
""")

for company_name, count in counts:
    st.write(f"**{company_name}**: {count} employee(s)")
