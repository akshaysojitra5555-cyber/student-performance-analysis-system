"""
Analysis Dashboard Page (Syllabus: Data Science and Visualization)
Demonstrates:
- DataFrame operations (filtering, grouping, aggregation)
- Visualizations: Bar Graph, Histogram, Pie Chart, Line Graph
"""
import streamlit as st
import pandas as pd
from utils.auth import check_authentication, render_sidebar_auth
from utils.data_manager import load_students, load_marks, CORE_SUBJECTS, CLASSES, SECTIONS, EXAMS
from utils.calculations import (
    calculate_student_results,
    get_class_summary_metrics,
    get_subject_statistics,
    get_grade_distribution,
    get_top_and_bottom_students,
    get_at_risk_students,
    get_student_vs_class_comparison
)
from utils.charts import (
    create_grade_pie_chart,
    create_subject_bar_graph,
    create_student_comparison_bar_graph,
    create_score_histogram,
    create_exam_trend_line_graph
)

# Authentication check
if not check_authentication():
    st.stop()

render_sidebar_auth()

st.title("📊 Student Performance Analysis Dashboard")
st.caption("Visual results analysis covering syllabus visualization techniques: Bar Graph, Histogram, Pie Chart, and Line Graph.")

# Load Data
df_students = load_students()
df_marks = load_marks()

if df_marks.empty or df_students.empty:
    st.warning("No records found. Please check data files.")
    st.stop()

# ----------------- FILTER CONTROLS -----------------
with st.container(border=True):
    st.markdown("#### 🔍 Filter Dashboard")
    f_c1, f_c2, f_c3 = st.columns(3)
    with f_c1:
        selected_exam = st.selectbox("Exam", options=EXAMS, index=2)
    with f_c2:
        selected_class = st.selectbox("Class", options=["All Classes"] + CLASSES)
    with f_c3:
        selected_sec = st.selectbox("Section", options=["All Sections"] + SECTIONS)

# Calculate results and apply filters
df_results_all = calculate_student_results(df_marks)
df_filtered = df_results_all[df_results_all["Exam"] == selected_exam].copy()

if selected_class != "All Classes":
    df_filtered = df_filtered[df_filtered["Class"] == selected_class]
if selected_sec != "All Sections":
    df_filtered = df_filtered[df_filtered["Section"] == selected_sec]

if df_filtered.empty:
    st.warning("No students match the selected filter combination.")
    st.stop()

# ----------------- METRIC CARDS -----------------
summary = get_class_summary_metrics(df_filtered)

m1, m2, m3, m4, m5, m6 = st.columns(6)
with m1:
    st.metric("Total Students", summary["total_students"])
with m2:
    st.metric("Class Average", f"{summary['class_avg']}%")
with m3:
    st.metric("Highest", f"{summary['highest_pct']}%")
with m4:
    st.metric("Lowest", f"{summary['lowest_pct']}%")
with m5:
    st.metric("Pass Rate", f"{summary['pass_pct']}%")
with m6:
    st.metric("Failed", summary["failed_count"])

st.markdown("---")

# ----------------- SYLLABUS VISUALIZATIONS TABS -----------------
tab_overview, tab_subjects, tab_ranks, tab_compare, tab_risk = st.tabs([
    "📈 Grade & Score Distribution",
    "📚 Subject Performance",
    "🏆 Top & Bottom Students",
    "🎯 Student vs Class Comparison",
    "⚠️ At-Risk Students (<40%)"
])

# TAB 1: GRADES & SCORE DISTRIBUTION (Pie Chart & Histogram)
with tab_overview:
    st.subheader("Grade & Score Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie Chart
        df_dist = get_grade_distribution(df_filtered)
        st.plotly_chart(create_grade_pie_chart(df_dist), use_container_width=True)
        
    with col2:
        # Histogram
        st.plotly_chart(create_score_histogram(df_filtered), use_container_width=True)
        
    st.markdown("#### Grade Count Summary")
    st.dataframe(df_dist, use_container_width=True, hide_index=True)

# TAB 2: SUBJECT PERFORMANCE (Bar Graph)
with tab_subjects:
    st.subheader("Subject-Wise Analysis (Bar Graph)")
    df_subj = get_subject_statistics(df_filtered)
    
    # Bar Graph
    st.plotly_chart(create_subject_bar_graph(df_subj), use_container_width=True)
    
    st.markdown("#### Subject Statistics Table")
    st.dataframe(df_subj, use_container_width=True, hide_index=True)

# TAB 3: TOP & BOTTOM STUDENTS
with tab_ranks:
    st.subheader("Top 10 and Bottom 10 Performers")
    top_10, bottom_10 = get_top_and_bottom_students(df_filtered, n=10)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### 🥇 Top Performers")
        st.dataframe(top_10, use_container_width=True, hide_index=True)
    with col_t2:
        st.markdown("#### 📉 Bottom Performers")
        st.dataframe(bottom_10, use_container_width=True, hide_index=True)

# TAB 4: STUDENT COMPARISON & TREND (Bar Graph & Line Graph)
with tab_compare:
    st.subheader("Student vs Class Comparison & Exam Trend")
    
    student_map = {f"{r} - {n}": r for r, n in zip(df_filtered["Roll_No"], df_filtered["Name"])}
    chosen_label = st.selectbox("Select Student", options=list(student_map.keys()))
    chosen_roll = student_map[chosen_label]
    chosen_name = df_filtered[df_filtered["Roll_No"] == chosen_roll]["Name"].iloc[0]
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        # Grouped Bar Graph comparison
        df_comp = get_student_vs_class_comparison(df_filtered, chosen_roll)
        st.plotly_chart(create_student_comparison_bar_graph(df_comp, chosen_name), use_container_width=True)
    with col_c2:
        # Line Graph of longitudinal trend
        st.plotly_chart(create_exam_trend_line_graph(df_marks, roll_no=chosen_roll), use_container_width=True)
        
    st.markdown("#### Marks Comparison Details")
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

# TAB 5: AT-RISK STUDENTS (<40%)
with tab_risk:
    st.subheader("⚠️ Weak-Subject & At-Risk Students Detection (<40%)")
    st.write("Identifies students who scored below 40% aggregate or failed in individual subjects.")
    
    df_risk = get_at_risk_students(df_filtered)
    
    if df_risk.empty:
        st.success("🎉 All students have passed all subjects in the selected filter!")
    else:
        st.error(f"Found {len(df_risk)} student(s) scoring below passing threshold (40%).")
        st.dataframe(df_risk, use_container_width=True, hide_index=True)
        
        st.info("💡 Recommended Action: Organize remedial tutorial classes for the flagged failed subjects.")
