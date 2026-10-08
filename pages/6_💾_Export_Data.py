"""
Data Export & Master Records Page
Enables educators and administrators to filter and download comprehensive
result sheets, subject summaries, and student rosters in CSV and Excel formats.
"""
import io
import streamlit as st
import pandas as pd
from utils.auth import check_authentication, render_sidebar_auth
from utils.data_manager import load_students, load_marks, CORE_SUBJECTS, EXAMS, CLASSES, SECTIONS
from utils.calculations import calculate_student_results, get_subject_statistics

# Authentication check
if not check_authentication():
    st.stop()

render_sidebar_auth()

st.title("💾 Master Data Export & Archives")
st.caption("Generate structured Excel workbooks and CSV dossiers with computed grades, divisions, and rankings.")

df_students = load_students()
df_marks = load_marks()

if df_marks.empty:
    st.warning("⚠️ No data available to export.")
    st.stop()

df_calculated = calculate_student_results(df_marks)

# Filter Criteria
with st.container(border=True):
    st.subheader("🔍 Export Filters")
    e_col1, e_col2, e_col3 = st.columns(3)
    
    with e_col1:
        exam_filter = st.selectbox("Exam Filter", options=["All Exams"] + EXAMS)
    with e_col2:
        class_filter = st.selectbox("Class Filter", options=["All Classes"] + CLASSES)
    with e_col3:
        sec_filter = st.selectbox("Section Filter", options=["All Sections"] + SECTIONS)

# Apply filters
export_df = df_calculated.copy()
if exam_filter != "All Exams":
    export_df = export_df[export_df["Exam"] == exam_filter]
if class_filter != "All Classes":
    export_df = export_df[export_df["Class"] == class_filter]
if sec_filter != "All Sections":
    export_df = export_df[export_df["Section"] == sec_filter]

# Display Export Preview
st.markdown(f"#### 📋 Previewing Data ({len(export_df)} records)")
columns_order = [
    "Roll_No", "Name", "Class", "Section", "Exam",
    "Mathematics", "Physics", "Chemistry", "English", "Computer Science",
    "Total_Marks", "Total_Max_Marks", "Percentage", "Grade", "Division", "Class_Rank", "Result_Status", "Failed_Subjects"
]
existing_cols = [c for c in columns_order if c in export_df.columns]
st.dataframe(export_df[existing_cols], use_container_width=True, hide_index=True)

st.markdown("---")

# Download options
st.subheader("📥 Download Dossiers")

d_col1, d_col2 = st.columns(2)

with d_col1:
    with st.container(border=True):
        st.markdown("### 📄 Comma Separated Values (CSV)")
        st.write("Export active filtered records as a standard CSV format compatible with any spreadsheet software.")
        
        csv_bytes = export_df[existing_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_bytes,
            file_name=f"Student_Results_{exam_filter}_{class_filter}.csv".replace(" ", "_"),
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

with d_col2:
    with st.container(border=True):
        st.markdown("### 📊 Microsoft Excel Workbook (.xlsx)")
        st.write("Export multi-tab workbook containing **Master Results**, **Subject Statistics**, and **Student Directory**.")
        
        # Build multi-tab Excel
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            export_df[existing_cols].to_excel(writer, sheet_name="Master_Results", index=False)
            
            # Subject summary tab
            df_subj = get_subject_statistics(export_df)
            if not df_subj.empty:
                df_subj.to_excel(writer, sheet_name="Subject_Statistics", index=False)
                
            # Student directory tab
            df_students.to_excel(writer, sheet_name="Student_Roster", index=False)
            
        excel_bytes = excel_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Multi-Tab Excel Workbook (.xlsx)",
            data=excel_bytes,
            file_name=f"Student_Performance_Dossier_{exam_filter}_{class_filter}.xlsx".replace(" ", "_"),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )

st.markdown("---")

# Additional Quick Exports
with st.expander("📦 Raw Database Table Downloads", expanded=False):
    st.write("Download unprocessed system CSV databases directly for backups or external integrations:")
    raw_col1, raw_col2 = st.columns(2)
    with raw_col1:
        st.download_button(
            "Download Raw students.csv",
            data=df_students.to_csv(index=False).encode("utf-8"),
            file_name="students.csv",
            mime="text/csv",
            use_container_width=True
        )
    with raw_col2:
        st.download_button(
            "Download Raw marks.csv",
            data=df_marks.to_csv(index=False).encode("utf-8"),
            file_name="marks.csv",
            mime="text/csv",
            use_container_width=True
        )
