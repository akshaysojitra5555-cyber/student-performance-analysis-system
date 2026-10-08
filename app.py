"""
Main Application Entry Point: Student Performance & Result Analysis System
Built with Python and Streamlit strictly adhering to the Python Programming (PP) syllabus.
"""
import streamlit as st
import pandas as pd
from utils.auth import init_session, login, logout, is_admin, render_sidebar_auth
from utils.data_manager import load_students, load_marks, CORE_SUBJECTS, EXAMS
from utils.calculations import calculate_student_results

# Streamlit Configuration
st.set_page_config(
    page_title="Student Performance & Result Analysis",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State & CSV Data
init_session()
df_students = load_students()
df_marks = load_marks()

# Render User Profile / Logout in sidebar if logged in
render_sidebar_auth()

# Main Application Logic
if not st.session_state.get("logged_in", False):
    # LOGIN VIEW
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); padding: 22px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h1 style="color:white; margin:0; font-size: 28px;">🎓 Student Performance & Result Analysis System</h1>
        <p style="color:#DBEAFE; margin:6px 0 0 0; font-size: 15px;">
            Python Programming (PP) Project • Built with Streamlit, Pandas, NumPy & Visualization Tools
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.subheader("🔐 Staff & Faculty Login")
        st.write("Please sign in to access student records and academic analytics.")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="admin or teacher")
            password = st.text_input("Password", type="password", placeholder="admin123 or teacher123")
            submit_btn = st.form_submit_button("Sign In", type="primary", use_container_width=True)
            
            if submit_btn:
                success, msg = login(username, password)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
        st.markdown("---")
        st.markdown("""
        **Default Demo Accounts:**
        - 🛡️ **Administrator**: `admin` / `admin123`
        - 🧑‍🏫 **Teacher**: `teacher` / `teacher123`
        """)

    with col2:
        st.subheader("📚 Alignment with PP Syllabus")
        st.markdown("""
        This project directly applies concepts from the **Python Programming (PP)** curriculum:
        - **Unit 1 (Basics & Data Structures)**: Variables, branching, loops, lists, tuples, dictionaries, and list comprehensions.
        - **Unit 2 (Functions & Modules)**: Defining functions, default/keyword arguments, multiple return values, lambdas, custom modules (`utils/`).
        - **Unit 3 (Exceptions & File Handling)**: `try-except` blocks, custom exceptions, reading/writing CSV and Text files using `with open()`.
        - **Unit 4 (Classes & OOP)**: `Student` and `StudentResult` classes with constructors, attributes, and methods.
        - **Unit 5 (Data Science & Visualization)**: Pandas DataFrames from CSV, Excel, dicts, and list of tuples. Visualizations: **Bar Graph**, **Histogram**, **Pie Chart**, and **Line Graph**.
        - **Unit 6 (Regular Expressions)**: Validation of student roll numbers and emails using the `re` module.
        """)

else:
    # AUTHENTICATED HOME VIEW
    user_name = st.session_state.get("full_name", "User")
    user_role = st.session_state.get("role", "Staff")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); padding: 22px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h1 style="color:white; margin:0; font-size: 26px;">Welcome, {user_name}!</h1>
        <p style="color:#DBEAFE; margin:6px 0 0 0; font-size: 15px;">
            Role: <b>{user_role}</b> • Academic Session: 2025–2026 • Status: Connected
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate System KPI Metrics
    df_calc = calculate_student_results(df_marks)
    total_students = len(df_students)
    total_records = len(df_marks)
    pass_rate = round((df_calc["Result_Status"] == "Pass").mean() * 100, 1) if not df_calc.empty else 0.0
    avg_score = round(df_calc["Percentage"].mean(), 1) if not df_calc.empty else 0.0
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Students", total_students)
    with k2:
        st.metric("Total Exam Records", total_records)
    with k3:
        st.metric("Class Pass Rate", f"{pass_rate}%")
    with k4:
        st.metric("Overall Average", f"{avg_score}%")
        
    st.markdown("---")
    
    # Quick Navigation Cards
    st.subheader("🚀 System Modules")
    
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        with st.container(border=True):
            st.markdown("### 📊 Analysis Dashboard")
            st.write("Bar Graphs, Histograms, Pie Charts, Line Trends, Top/Bottom students, and At-risk alerts.")
            st.page_link("pages/1_📊_Dashboard.py", label="Open Dashboard", icon="📊")
            
    with r1_c2:
        with st.container(border=True):
            st.markdown("### 👨‍🎓 Student Management")
            st.write("Enroll, search, update, and manage student records with regex validation.")
            st.page_link("pages/2_👨‍🎓_Student_Management.py", label="Manage Students", icon="👨‍🎓")
            
    with r1_c3:
        with st.container(border=True):
            st.markdown("### 📝 Marks Entry")
            st.write("Enter subject marks per exam with instant percentage and grade preview.")
            st.page_link("pages/3_📝_Marks_Entry.py", label="Enter Marks", icon="📝")

    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r2_c1:
        with st.container(border=True):
            st.markdown("### 📤 Bulk Upload")
            st.write("Upload class marks using CSV or Excel templates.")
            st.page_link("pages/4_📤_Bulk_Upload.py", label="Bulk Upload", icon="📤")
            
    with r2_c2:
        with st.container(border=True):
            st.markdown("### 📜 Report Card")
            st.write("View individual report cards with comparison Bar Graphs and download text dossiers.")
            st.page_link("pages/5_📜_Report_Card.py", label="View Report Cards", icon="📜")
            
    with r2_c3:
        with st.container(border=True):
            st.markdown("### 💾 Export Data")
            st.write("Download complete student result sheets in CSV or multi-tab Excel format.")
            st.page_link("pages/6_💾_Export_Data.py", label="Export Files", icon="💾")

    st.markdown("---")
    
    # Syllabus Mapping Reference Card for Viva/Evaluation
    with st.expander("📖 Syllabus Concepts Reference (Viva & Evaluation Guide)", expanded=True):
        st.markdown("""
        | Syllabus Unit | Key Topics | Implementation in This Project |
        | :--- | :--- | :--- |
        | **Unit 1: Basics & Data Structures** | Lists, Tuples, Dictionaries, List Comprehension | Sample data created from List of Tuples; marks stored in dictionaries; list comprehensions for failed subject detection. |
        | **Unit 2: Functions & Modules** | Function definition, default arguments, multiple returns, lambdas | Custom modules in `utils/`; lambda functions for grade mapping; functions returning `(success, message)`. |
        | **Unit 3: Exceptions & Files** | `try-except`, User exceptions, File Handling (`with open`) | Custom `InvalidMarksError` exception; reading/writing `students.csv` and `marks.csv`; formatted text report card generation. |
        | **Unit 4: Classes & OOP** | Classes, `__init__`, encapsulation, methods | `Student` class and `StudentResult` class in `utils/models.py`. |
        | **Unit 5: Data Science & Visualization** | DataFrames (CSV, Excel, dict, list of tuples), Bar Graph, Histogram, Pie Chart, Line Graph | Pandas DataFrame operations (`read_csv`, `read_excel`, filtering, groupby, aggregation); 4 syllabus charts in `utils/charts.py`. |
        | **Unit 6: Regular Expressions** | Sequence characters, quantifiers, email/roll validation | `re.match()` for student email and roll number validation in `utils/data_manager.py`. |
        """)
