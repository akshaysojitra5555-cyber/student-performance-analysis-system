"""
Report Card Page
Displays individual student report card with:
- Academic marks breakdown
- Performance comparison Bar Graph
- Official A4 PDF Report Card Download (.pdf)
"""
import streamlit as st
import pandas as pd
from utils.auth import check_authentication, render_sidebar_auth
from utils.data_manager import (
    load_students,
    load_marks,
    CORE_SUBJECTS,
    EXAMS
)
from utils.calculations import (
    calculate_student_results,
    get_student_vs_class_comparison,
    calculate_grade
)
from utils.charts import create_student_comparison_bar_graph
from utils.pdf_generator import generate_pdf_report_card

# Authentication check
if not check_authentication():
    st.stop()

render_sidebar_auth()

st.title("📜 Student Report Card")
st.caption("Generate individual student performance report card with performance bar graphs and official PDF download.")

df_students = load_students()
df_marks = load_marks()

if df_students.empty or df_marks.empty:
    st.warning("No records found.")
    st.stop()

# Selection bar
c1, c2 = st.columns(2)
with c1:
    exam_choice = st.selectbox("Exam Term", options=EXAMS, index=2)
with c2:
    class_choice = st.selectbox("Class Filter", options=["All"] + sorted(list(df_students["Class"].unique())))

pool = df_students.copy()
if class_choice != "All":
    pool = pool[pool["Class"] == class_choice]

if pool.empty:
    st.warning("No students available in selected class.")
    st.stop()

student_map = {f"{r} - {n}": r for r, n in zip(pool["Roll_No"], pool["Name"])}
chosen_label = st.selectbox("Choose Student", options=list(student_map.keys()))
chosen_roll = student_map[chosen_label]

# Get student records
df_results = calculate_student_results(df_marks)
df_exam_res = df_results[df_results["Exam"] == exam_choice]

s_marks = df_exam_res[df_exam_res["Roll_No"] == chosen_roll]
s_info = df_students[df_students["Roll_No"] == chosen_roll].iloc[0].to_dict()

if s_marks.empty:
    st.warning(f"No marks found for {s_info['Name']} in {exam_choice}.")
    st.stop()

rec = s_marks.iloc[0].to_dict()
class_rank = int(rec.get("Class_Rank", 1))
total_in_class = len(df_exam_res[df_exam_res["Class"] == s_info["Class"]])

# ----------------- REPORT CARD DISPLAY -----------------
with st.container(border=True):
    st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-bottom: 2px;'>EXCELLENCE ACADEMY SECONDARY SCHOOL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; margin-top: 0;'>OFFICIAL STUDENT PERFORMANCE DOSSIER • SESSION 2025-2026</p>", unsafe_allow_html=True)
    st.divider()
    
    # Bio row
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.write(f"**Name:** {s_info['Name']}")
    with b2:
        st.write(f"**Roll Number:** {s_info['Roll_No']}")
    with b3:
        st.write(f"**Class & Section:** {s_info['Class']} - {s_info['Section']}")
    with b4:
        st.write(f"**Exam Term:** {exam_choice}")
        
    st.markdown("---")
    
    # Subject breakdown table
    max_m = rec["Max_Marks"]
    pass_mark = round(max_m * 0.40, 1)
    
    table_rows = []
    for sub in CORE_SUBJECTS:
        score = float(rec[sub])
        pct = round((score / max_m) * 100.0, 1)
        sub_grade = calculate_grade(pct)
        status = "Pass" if score >= pass_mark else "Fail"
        table_rows.append({
            "Subject": sub,
            "Max Marks": int(max_m),
            "Passing Marks": pass_mark,
            "Marks Scored": score,
            "Percentage": f"{pct}%",
            "Grade": sub_grade,
            "Result": status
        })
    df_table = pd.DataFrame(table_rows)
    st.dataframe(df_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    # Summary Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Total Marks", f"{rec['Total_Marks']} / {int(rec['Total_Max_Marks'])}")
    with m2:
        st.metric("Percentage", f"{rec['Percentage']}%")
    with m3:
        st.metric("Overall Grade", rec["Grade"])
    with m4:
        st.metric("Division", rec["Division"])
    with m5:
        st.metric("Class Rank", f"Rank #{class_rank} of {total_in_class}")
        
    st.markdown("---")
    
    # Bar Graph comparison
    st.subheader("Performance Comparison (Bar Graph)")
    df_comp = get_student_vs_class_comparison(df_exam_res, chosen_roll)
    st.plotly_chart(create_student_comparison_bar_graph(df_comp, s_info["Name"]), use_container_width=True)

# ----------------- PDF DOWNLOAD SECTION -----------------
st.subheader("📥 Download Official Report Card")

with st.container(border=True):
    st.markdown("### 📄 Print-Ready Official PDF Dossier")
    st.write("Generate and download the formatted official academic report card in A4 PDF format including school header, subject scores, teacher remarks, and signature blocks.")
    
    # Generate PDF in-memory stream
    pdf_bytes = generate_pdf_report_card(
        student_info=s_info,
        marks_record=rec,
        class_rank=class_rank,
        total_students=total_in_class
    )
    
    st.download_button(
        label=f"📥 Download Official PDF Report Card for {s_info['Name']} (.pdf)",
        data=pdf_bytes,
        file_name=f"ReportCard_{s_info['Roll_No']}_{exam_choice.replace(' ', '_')}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
