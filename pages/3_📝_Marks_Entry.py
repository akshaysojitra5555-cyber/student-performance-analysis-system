"""
Marks Entry Page (Syllabus: Functions, Validation, Exception Handling)
Allows inputting and validating marks per subject and exam stage.
"""
import streamlit as st
import pandas as pd
from utils.auth import check_authentication, render_sidebar_auth
from utils.data_manager import (
    load_students,
    load_marks,
    save_or_update_marks_entry,
    CORE_SUBJECTS,
    EXAMS,
    EXAM_MAX_MARKS
)
from utils.calculations import calculate_grade

# Authentication check
if not check_authentication():
    st.stop()

render_sidebar_auth()

st.title("📝 Student Marks Entry")
st.caption("Enter and validate subject marks for Unit Test, Mid-term, and Final examinations.")

df_students = load_students()
df_marks = load_marks()

if df_students.empty:
    st.warning("No students registered. Please enroll students first.")
    st.stop()

# Exam & Class selection
c1, c2 = st.columns(2)
with c1:
    exam_stage = st.selectbox("Select Exam", options=EXAMS, index=1)
    max_m = EXAM_MAX_MARKS[exam_stage]
    pass_cutoff = round(max_m * 0.40, 1)
with c2:
    class_filter = st.selectbox("Filter by Class", options=["All"] + sorted(list(df_students["Class"].unique())))

pool = df_students.copy()
if class_filter != "All":
    pool = pool[pool["Class"] == class_filter]

if pool.empty:
    st.warning("No students in this class.")
    st.stop()

student_map = {f"{r} - {n} ({c} {s})": r for r, n, c, s in zip(pool["Roll_No"], pool["Name"], pool["Class"], pool["Section"])}
chosen_label = st.selectbox("Select Student", options=list(student_map.keys()))
chosen_roll = student_map[chosen_label]
student_info = df_students[df_students["Roll_No"] == chosen_roll].iloc[0]

# Check existing marks
existing_record = df_marks[(df_marks["Roll_No"] == chosen_roll) & (df_marks["Exam"] == exam_stage)]
has_record = not existing_record.empty
old_scores = existing_record.iloc[0].to_dict() if has_record else {}

# Input Form
with st.container(border=True):
    st.markdown(f"### Marks Entry: {student_info['Name']} (Roll #{chosen_roll})")
    st.write(f"Exam: **{exam_stage}** | Maximum Marks per Subject: **{max_m}** | Pass Threshold: **{pass_cutoff}**")
    
    with st.form("marks_form"):
        inputs = {}
        cols = st.columns(len(CORE_SUBJECTS))
        
        for idx, sub in enumerate(CORE_SUBJECTS):
            with cols[idx]:
                default_val = float(old_scores.get(sub, 0.0)) if has_record else 0.0
                inputs[sub] = st.number_input(
                    f"{sub}",
                    min_value=0.0,
                    max_value=float(max_m),
                    value=float(default_val),
                    step=0.5
                )
                
        # Real-time calculation preview
        total_scored = sum(inputs.values())
        total_possible = max_m * len(CORE_SUBJECTS)
        pct = round((total_scored / total_possible) * 100.0, 1)
        grade = calculate_grade(pct)
        failed_subs = [s for s, sc in inputs.items() if sc < pass_cutoff]
        status = "Pass" if len(failed_subs) == 0 and pct >= 40.0 else "Fail"
        
        st.markdown("---")
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            st.metric("Total Score", f"{total_scored:.1f} / {total_possible}")
        with p2:
            st.metric("Percentage", f"{pct}%")
        with p3:
            st.metric("Predicted Grade", grade)
        with p4:
            st.metric("Status", status)
            
        save_btn = st.form_submit_button("Save Marks", type="primary", use_container_width=True)
        if save_btn:
            success, msg = save_or_update_marks_entry(chosen_roll, exam_stage, inputs)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

st.markdown("---")
st.subheader(f"📋 Registered {exam_stage} Marks Table")
table_view = df_marks[df_marks["Exam"] == exam_stage]
if class_filter != "All":
    table_view = table_view[table_view["Class"] == class_filter]
st.dataframe(table_view[["Roll_No", "Name", "Class", "Section"] + CORE_SUBJECTS], use_container_width=True, hide_index=True)
