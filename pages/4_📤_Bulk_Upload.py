"""
Bulk Marks Upload Page (Syllabus: Creating DataFrame from CSV and Excel)
Demonstrates:
- Creating Data Frame from an Excel Spreadsheet (.xlsx)
- Creating Data Frame from .csv Files
- File Handling and Exception Handling
"""
import streamlit as st
import pandas as pd
from utils.auth import check_authentication, render_sidebar_auth
from utils.data_manager import (
    generate_csv_template,
    generate_excel_template,
    process_bulk_upload,
    CORE_SUBJECTS,
    EXAM_MAX_MARKS
)

# Authentication check
if not check_authentication():
    st.stop()

render_sidebar_auth()

st.title("📤 Marks Upload")
st.caption("Batch upload student exam marks using CSV or Excel spreadsheets.")

# 1. Download Templates
with st.container(border=True):
    st.subheader("1. Download Upload Template")
    st.write("Download pre-configured templates with the required columns:")
    st.code("Roll_No, Exam, " + ", ".join(CORE_SUBJECTS))
    
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            label="📄 Download CSV Template (.csv)",
            data=generate_csv_template(),
            file_name="marks_template.csv",
            mime="text/csv",
            use_container_width=True
        )
    with c2:
        st.download_button(
            label="📊 Download Excel Template (.xlsx)",
            data=generate_excel_template(),
            file_name="marks_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

st.markdown("---")

# 2. File Upload & Processing
st.subheader("2. Upload Marks Spreadsheet")
uploaded = st.file_uploader("Select a CSV or Excel file", type=["csv", "xlsx"])

if uploaded is not None:
    is_csv = uploaded.name.endswith(".csv")
    file_type = "csv" if is_csv else "excel"
    
    try:
        # Create DataFrame from uploaded file (Syllabus: DataFrame from CSV & Excel)
        if is_csv:
            df_preview = pd.read_csv(uploaded)
        else:
            df_preview = pd.read_excel(uploaded)
            
        st.markdown(f"**Spreadsheet Preview** ({len(df_preview)} rows):")
        st.dataframe(df_preview.head(5), use_container_width=True)
        
        uploaded.seek(0)
        if st.button("Process & Save Marks", type="primary", use_container_width=True):
            success, msg, summary = process_bulk_upload(uploaded, file_type)
            if success:
                st.success(msg)
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    st.metric("Total Rows", summary["total_processed"])
                with sc2:
                    st.metric("New Records", summary["added"])
                with sc3:
                    st.metric("Updated Records", summary["updated"])
                    
                if summary["errors"]:
                    with st.expander("Warnings / Skipped Rows"):
                        for err in summary["errors"]:
                            st.write(f"- {err}")
            else:
                st.error(msg)
                
    except Exception as e:
        st.error(f"Error reading spreadsheet: {str(e)}")
