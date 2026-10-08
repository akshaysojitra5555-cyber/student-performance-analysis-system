# 🎓 Student Performance & Result Analysis System
### Python Programming (PP) Course Project

A clean, modular, and easy-to-understand **Student Performance & Result Analysis System** built using **Python** and **Streamlit**.

---

## 🌟 Key Features

1. **🔐 Multi-Role Login**: Session-based Admin (`admin`/`admin123`) & Teacher (`teacher`/`teacher123`) authentication.
2. **👨‍🎓 Student Management**: Add, Edit, Delete, and Search students with regex validation (`re`) and OOP `Student` class.
3. **📝 Marks Entry**: Enter and validate subject marks with real-time percentage and grade previews.
4. **📤 Bulk Marks Upload**: Upload CSV or Excel files with downloadable pre-formatted templates.
5. **⚡ Result Engine**: Compute Total, Percentage, Letter Grade (A+ to F), Division, and Class Rank.
6. **📊 Analysis Dashboard**: Visual analytics using the 4 syllabus visualizations:
   - 📊 **Bar Graph**: Subject-wise averages and topper benchmarks
   - 📉 **Histogram**: Class marks score distribution
   - 🥧 **Pie Chart**: Grade distribution
   - 📈 **Line Graph**: Longitudinal performance trend across exams
   - ⚠️ **At-Risk Detection**: Identifies students scoring below 40%
7. **📜 Official Report Card with PDF Download**:
   - Individual student evaluation with subject breakdown
   - Comparative Bar Graph against class benchmark
   - **📥 Download Official A4 PDF Report Card (.pdf)** complete with school header, rubric, remarks, and signature lines.
8. **💾 Master Data Export**: Export full results to CSV and multi-tab Excel workbooks (`.xlsx`).

---

## 🚀 How to Run the Project

### 1. Open Terminal in Project Folder
```powershell
cd "c:\Users\aksha\OneDrive\Desktop\Python"
```

### 2. Install Required Packages
```powershell
pip install -r requirements.txt
```

### 3. Launch Streamlit Application
```powershell
streamlit run app.py
```
*(Or: `streamlit run main.py`)*

### 4. Open in Browser
Navigate to: **[http://localhost:8501](http://localhost:8501)**

---

## 🔑 Login Accounts

| Role | Username | Password |
| :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` |
| **Faculty / Teacher** | `teacher` | `teacher123` |
