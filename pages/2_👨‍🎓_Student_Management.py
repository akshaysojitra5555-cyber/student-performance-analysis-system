"""
Student Management Page (Syllabus: OOP Classes, Strings, Regular Expressions)
Demonstrates:
- Student Class object instantiation
- Regular Expression validation for Roll Number and Email
- DataFrame search and filtering
"""
import streamlit as st
import pandas as pd
from utils.auth import check_authentication, render_sidebar_auth
from utils.models import Student
from utils.data_manager import (
    load_students,
    add_student,
    update_student,
    delete_student,
    CLASSES,
    SECTIONS
)

# Authentication check
if not check_authentication():
    st.stop()

render_sidebar_auth()

st.title("👨‍🎓 Student Management")
st.caption("Enroll students, update student records, search rolls, and manage enrollment rosters.")

df_students = load_students()

tab_list, tab_add, tab_edit, tab_delete = st.tabs([
    "📋 Student Directory",
    "➕ Enroll New Student",
    "✏️ Edit Student Info",
    "🗑️ Delete Student"
])

# TAB 1: VIEW & SEARCH
with tab_list:
    st.subheader("Student Roster")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_kw = st.text_input("🔍 Search by Name or Roll Number", placeholder="Search...")
    with col2:
        class_filter = st.selectbox("Filter Class", options=["All"] + CLASSES)
        
    filtered = df_students.copy()
    if search_kw.strip():
        kw = search_kw.strip().lower()
        filtered = filtered[
            filtered["Name"].str.lower().str.contains(kw, na=False) |
            filtered["Roll_No"].astype(str).str.contains(kw, na=False)
        ]
    if class_filter != "All":
        filtered = filtered[filtered["Class"] == class_filter]
        
    st.write(f"Showing **{len(filtered)}** of {len(df_students)} students.")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

# TAB 2: ENROLL NEW STUDENT (Using Student OOP Class & Regex)
with tab_add:
    st.subheader("➕ Enroll New Student")
    st.caption("Validates inputs with Regular Expressions and creates a Student object.")
    
    with st.form("enroll_student_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            r_no = st.number_input("Roll Number", min_value=1, max_value=99999, value=int(df_students["Roll_No"].max() + 1) if not df_students.empty else 101, step=1)
            name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
        with c2:
            cls = st.selectbox("Class", options=CLASSES)
            sec = st.selectbox("Section", options=SECTIONS)
            email = st.text_input("Email Address (Regex Validated)", placeholder="e.g. rahul@school.edu")
            
        submitted = st.form_submit_button("Enroll Student", type="primary", use_container_width=True)
        
        if submitted:
            if not name.strip():
                st.error("Name cannot be empty.")
            else:
                # Instantiate Student OOP Class (Syllabus: OOP)
                s_obj = Student(r_no, name, cls, sec, gender, email)
                success, msg = add_student(s_obj.roll_no, s_obj.name, s_obj.class_name, s_obj.section, s_obj.gender, s_obj.email)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

# TAB 3: EDIT STUDENT
with tab_edit:
    st.subheader("✏️ Edit Student Profile")
    if not df_students.empty:
        student_opts = {f"{r} - {n}": r for r, n in zip(df_students["Roll_No"], df_students["Name"])}
        edit_choice = st.selectbox("Select Student to Edit", options=list(student_opts.keys()))
        edit_roll = student_opts[edit_choice]
        
        current_data = df_students[df_students["Roll_No"] == edit_roll].iloc[0]
        
        with st.form("edit_form"):
            e1, e2 = st.columns(2)
            with e1:
                st.text_input("Roll Number", value=str(edit_roll), disabled=True)
                new_n = st.text_input("Full Name", value=str(current_data["Name"]))
                new_g = st.selectbox("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(current_data["Gender"]) if current_data["Gender"] in ["Male", "Female", "Other"] else 0)
            with e2:
                new_c = st.selectbox("Class", options=CLASSES, index=CLASSES.index(current_data["Class"]) if current_data["Class"] in CLASSES else 0)
                new_s = st.selectbox("Section", options=SECTIONS, index=SECTIONS.index(current_data["Section"]) if current_data["Section"] in SECTIONS else 0)
                new_e = st.text_input("Email", value=str(current_data["Email"]))
                
            save_btn = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
            if save_btn:
                updates = {
                    "Name": new_n.strip(),
                    "Gender": new_g,
                    "Class": new_c,
                    "Section": new_s,
                    "Email": new_e.strip()
                }
                success, msg = update_student(edit_roll, updates)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

# TAB 4: DELETE STUDENT
with tab_delete:
    st.subheader("🗑️ Delete Student Record")
    if not df_students.empty:
        del_choice = st.selectbox("Select Student to Delete", options=list(student_opts.keys()), key="del_select")
        del_roll = student_opts[del_choice]
        
        st.warning(f"Are you sure you want to delete student Roll #{del_roll}?")
        confirm = st.checkbox("Confirm permanent deletion")
        
        if st.button("Delete Student", type="primary", disabled=not confirm):
            success, msg = delete_student(del_roll)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
