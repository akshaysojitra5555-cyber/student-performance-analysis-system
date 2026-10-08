"""
Data Manager Module (Syllabus Units: File Handling, Regular Expressions, Data Frames)
Demonstrates:
- File handling with 'with open(...)', checking os.path.exists()
- DataFrames from List of Tuples, Dictionaries, and CSV/Excel files
- Regular Expressions (re) for validation of email and roll numbers
- Exception handling (try-except)
"""
import os
import re
import io
import pandas as pd
import numpy as np

# File paths using standard os module
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.csv")
MARKS_FILE = os.path.join(DATA_DIR, "marks.csv")

# Core configurations
CORE_SUBJECTS = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]
EXAMS = ["Unit Test", "Mid-term", "Final"]
EXAM_MAX_MARKS = {
    "Unit Test": 50,
    "Mid-term": 100,
    "Final": 100
}
CLASSES = ["Class 10", "Class 11", "Class 12"]
SECTIONS = ["A", "B"]

# Regular expression patterns for input validation (Syllabus: Regular Expressions)
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
ROLL_REGEX = r"^\d{1,5}$"

def validate_email_with_regex(email):
    """
    Validate email address format using regular expressions.
    (Syllabus: Regular Expressions - Sequence characters and quantifiers)
    """
    return bool(re.match(EMAIL_REGEX, str(email).strip()))

def validate_roll_no_with_regex(roll_no):
    """
    Validate roll number is numeric and 1 to 5 digits using regex.
    """
    return bool(re.match(ROLL_REGEX, str(roll_no).strip()))

def ensure_data_directory():
    """Ensure data directory exists using os module."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def generate_sample_data():
    """
    Generate 30 sample students and marks.
    Demonstrates creating a DataFrame from a Python List of Tuples.
    (Syllabus: 'Creating Data from Python List of Tuples')
    """
    ensure_data_directory()
    
    # 1. List of Tuples for students
    student_tuples = [
        # Class 10 - Section A (10 students)
        (101, "Aarav Sharma", "Class 10", "A", "Male", "aarav.sharma@school.edu"),
        (102, "Diya Patel", "Class 10", "A", "Female", "diya.patel@school.edu"),
        (103, "Rohan Verma", "Class 10", "A", "Male", "rohan.verma@school.edu"),
        (104, "Ananya Iyer", "Class 10", "A", "Female", "ananya.iyer@school.edu"),
        (105, "Ishaan Nair", "Class 10", "A", "Male", "ishaan.nair@school.edu"),
        (106, "Priya Singh", "Class 10", "A", "Female", "priya.singh@school.edu"),
        (107, "Kabir Mehta", "Class 10", "A", "Male", "kabir.mehta@school.edu"),
        (108, "Sneha Mukherjee", "Class 10", "A", "Female", "sneha.m@school.edu"),
        (109, "Aditya Joshi", "Class 10", "A", "Male", "aditya.j@school.edu"),
        (110, "Tanvi Kapoor", "Class 10", "A", "Female", "tanvi.k@school.edu"),
        
        # Class 10 - Section B (8 students)
        (111, "Vikram Malhotra", "Class 10", "B", "Male", "vikram.m@school.edu"),
        (112, "Pooja Gupta", "Class 10", "B", "Female", "pooja.gupta@school.edu"),
        (113, "Arjun Reddy", "Class 10", "B", "Male", "arjun.reddy@school.edu"),
        (114, "Riya Choudhury", "Class 10", "B", "Female", "riya.c@school.edu"),
        (115, "Nikhil Das", "Class 10", "B", "Male", "nikhil.das@school.edu"),
        (116, "Meera Rao", "Class 10", "B", "Female", "meera.rao@school.edu"),
        (117, "Siddharth Bhat", "Class 10", "B", "Male", "sid.bhat@school.edu"),
        (118, "Neha Saxena", "Class 10", "B", "Female", "neha.saxena@school.edu"),
        
        # Class 11 - Section A (6 students)
        (119, "Ayush Mishra", "Class 11", "A", "Male", "ayush.m@school.edu"),
        (120, "Simran Kaur", "Class 11", "A", "Female", "simran.k@school.edu"),
        (121, "Varun Pillai", "Class 11", "A", "Male", "varun.p@school.edu"),
        (122, "Shreya Bose", "Class 11", "A", "Female", "shreya.bose@school.edu"),
        (123, "Aryan Sen", "Class 11", "A", "Male", "aryan.sen@school.edu"),
        (124, "Kritika Jain", "Class 11", "A", "Female", "kritika.j@school.edu"),
        
        # Class 12 - Section A (6 students)
        (125, "Harsh Vardhan", "Class 12", "A", "Male", "harsh.v@school.edu"),
        (126, "Divya Nambiar", "Class 12", "A", "Female", "divya.n@school.edu"),
        (127, "Pranav Kulkarni", "Class 12", "A", "Male", "pranav.k@school.edu"),
        (128, "Natasha Roy", "Class 12", "A", "Female", "natasha.roy@school.edu"),
        (129, "Kunal Singhania", "Class 12", "A", "Male", "kunal.s@school.edu"),
        (130, "Bhavya Aggarwal", "Class 12", "A", "Female", "bhavya.a@school.edu"),
    ]
    
    # Create DataFrame from List of Tuples
    df_students = pd.DataFrame(
        student_tuples,
        columns=["Roll_No", "Name", "Class", "Section", "Gender", "Email"]
    )
    df_students.to_csv(STUDENTS_FILE, index=False)
    
    # 2. Performance profiles for marks distribution
    profiles = {
        101: 91, 102: 78, 103: 61, 104: 93, 105: 75,
        106: 94, 107: 58, 108: 79, 109: 64, 110: 82,
        111: 62, 112: 80, 113: 95, 114: 67, 115: 35,  # At-risk
        116: 76, 117: 63, 118: 81, 119: 60, 120: 55,  # Weak in Chemistry
        121: 90, 122: 77, 123: 65, 124: 92, 125: 84,
        126: 93, 127: 66, 128: 83, 129: 34, 130: 91   # At-risk
    }
    
    marks_records = []
    np.random.seed(42)
    
    for _, s in df_students.iterrows():
        roll = s["Roll_No"]
        base_pct = profiles.get(roll, 65)
        
        for exam in EXAMS:
            max_m = EXAM_MAX_MARKS[exam]
            scale = max_m / 100.0
            
            row = {
                "Roll_No": roll,
                "Name": s["Name"],
                "Class": s["Class"],
                "Section": s["Section"],
                "Exam": exam,
                "Max_Marks": max_m
            }
            
            for sub in CORE_SUBJECTS:
                sub_base = base_pct
                if roll == 120 and sub == "Chemistry":
                    sub_base = 32  # Failing in Chemistry
                elif roll in [115, 129] and sub in ["Mathematics", "Physics"]:
                    sub_base = 30  # Failing in STEM
                    
                score_pct = np.clip(np.random.normal(sub_base, 4.0), 15.0, 99.0)
                score = round(score_pct * scale, 1)
                row[sub] = min(float(max_m), max(0.0, score))
                
            marks_records.append(row)
            
    df_marks = pd.DataFrame(marks_records)
    df_marks.to_csv(MARKS_FILE, index=False)

def load_students():
    """Load students DataFrame from CSV (File Handling)."""
    ensure_data_directory()
    if not os.path.exists(STUDENTS_FILE):
        generate_sample_data()
    return pd.read_csv(STUDENTS_FILE)

def save_students(df):
    """Save students DataFrame to CSV."""
    ensure_data_directory()
    df.to_csv(STUDENTS_FILE, index=False)
    return True

def load_marks():
    """Load marks DataFrame from CSV."""
    ensure_data_directory()
    if not os.path.exists(MARKS_FILE):
        generate_sample_data()
    return pd.read_csv(MARKS_FILE)

def save_marks(df):
    """Save marks DataFrame to CSV."""
    ensure_data_directory()
    df.to_csv(MARKS_FILE, index=False)
    return True

def add_student(roll_no, name, class_name, section, gender, email):
    """
    Add a new student with validation.
    Returns (success: bool, message: str) - Demonstrates multiple return values.
    """
    # Validate roll number with regex
    if not validate_roll_no_with_regex(roll_no):
        return False, "Invalid Roll Number. Must be a 1-5 digit positive integer."
        
    # Validate email with regex
    if not validate_email_with_regex(email):
        return False, "Invalid Email format. Please enter a valid email address (e.g. name@school.edu)."
        
    df_s = load_students()
    roll_no = int(roll_no)
    
    if roll_no in df_s["Roll_No"].values:
        return False, f"Roll Number {roll_no} already exists in the student registry."
        
    new_data = {
        "Roll_No": [roll_no],
        "Name": [name.strip()],
        "Class": [class_name],
        "Section": [section],
        "Gender": [gender],
        "Email": [email.strip()]
    }
    # Creating DataFrame from a Python Dictionary (Syllabus concept)
    new_df = pd.DataFrame(new_data)
    df_s = pd.concat([df_s, new_df], ignore_index=True)
    save_students(df_s)
    return True, f"Student '{name}' (Roll #{roll_no}) enrolled successfully."

def update_student(roll_no, updated_dict):
    """Update student profile in CSV."""
    df_s = load_students()
    roll_no = int(roll_no)
    matches = df_s.index[df_s["Roll_No"] == roll_no].tolist()
    if not matches:
        return False, f"Student #{roll_no} not found."
        
    idx = matches[0]
    for key, val in updated_dict.items():
        if key in df_s.columns and key != "Roll_No":
            df_s.loc[idx, key] = val
    save_students(df_s)
    
    # Synchronize name/class/section in marks file as well
    df_m = load_marks()
    m_matches = df_m.index[df_m["Roll_No"] == roll_no].tolist()
    if m_matches:
        for k in ["Name", "Class", "Section"]:
            if k in updated_dict:
                df_m.loc[m_matches, k] = updated_dict[k]
        save_marks(df_m)
        
    return True, f"Student #{roll_no} updated successfully."

def delete_student(roll_no):
    """Delete student and their marks."""
    df_s = load_students()
    roll_no = int(roll_no)
    if roll_no not in df_s["Roll_No"].values:
        return False, f"Student #{roll_no} not found."
        
    df_s = df_s[df_s["Roll_No"] != roll_no]
    save_students(df_s)
    
    df_m = load_marks()
    df_m = df_m[df_m["Roll_No"] != roll_no]
    save_marks(df_m)
    
    return True, f"Student #{roll_no} and associated marks removed."

def save_or_update_marks_entry(roll_no, exam, marks_dict):
    """
    Save or update marks for a student for a specific exam.
    Uses exception handling.
    """
    df_s = load_students()
    df_m = load_marks()
    roll_no = int(roll_no)
    
    s_match = df_s[df_s["Roll_No"] == roll_no]
    if s_match.empty:
        return False, f"Roll Number {roll_no} does not exist."
        
    s_info = s_match.iloc[0]
    max_m = EXAM_MAX_MARKS.get(exam, 100)
    
    entry = {
        "Roll_No": roll_no,
        "Name": s_info["Name"],
        "Class": s_info["Class"],
        "Section": s_info["Section"],
        "Exam": exam,
        "Max_Marks": max_m
    }
    for sub in CORE_SUBJECTS:
        score = float(marks_dict.get(sub, 0.0))
        if score < 0 or score > max_m:
            return False, f"Marks for {sub} must be between 0 and {max_m}."
        entry[sub] = score
        
    existing_idx = df_m.index[(df_m["Roll_No"] == roll_no) & (df_m["Exam"] == exam)].tolist()
    if existing_idx:
        for col, val in entry.items():
            df_m.loc[existing_idx[0], col] = val
        save_marks(df_m)
        return True, f"Updated {exam} marks for Roll #{roll_no}."
    else:
        new_row = pd.DataFrame([entry])
        df_m = pd.concat([df_m, new_row], ignore_index=True)
        save_marks(df_m)
        return True, f"Saved {exam} marks for Roll #{roll_no}."

def generate_csv_template():
    """Generate a sample CSV template for bulk marks upload."""
    sample = {
        "Roll_No": [101, 102],
        "Exam": ["Final", "Final"],
        "Mathematics": [85.0, 65.5],
        "Physics": [78.0, 58.0],
        "Chemistry": [82.5, 42.0],
        "English": [90.0, 75.0],
        "Computer Science": [94.0, 80.0]
    }
    return pd.DataFrame(sample).to_csv(index=False).encode("utf-8")

def generate_excel_template():
    """Generate an Excel (.xlsx) template for bulk marks upload."""
    sample = {
        "Roll_No": [101, 102, 103],
        "Exam": ["Mid-term", "Mid-term", "Mid-term"],
        "Mathematics": [85.0, 65.5, 92.0],
        "Physics": [78.0, 58.0, 88.0],
        "Chemistry": [82.5, 42.0, 79.5],
        "English": [90.0, 75.0, 85.0],
        "Computer Science": [94.0, 80.0, 95.0]
    }
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        pd.DataFrame(sample).to_excel(writer, index=False, sheet_name="Marks_Template")
    return buf.getvalue()

def process_bulk_upload(file_obj, file_type):
    """
    Process bulk upload file (CSV or Excel).
    Demonstrates creating DataFrame from CSV or Excel Spreadsheet.
    (Syllabus: Creating DataFrame from Excel, Creating DataFrame from .csv)
    """
    try:
        if file_type == "csv":
            df_upload = pd.read_csv(file_obj)
        else:
            df_upload = pd.read_excel(file_obj)
            
        required_cols = ["Roll_No", "Exam"] + CORE_SUBJECTS
        missing = [c for c in required_cols if c not in df_upload.columns]
        if missing:
            return False, f"Missing required columns: {', '.join(missing)}", None
            
        df_students = load_students()
        registered = set(df_students["Roll_No"].dropna().astype(int))
        
        valid_records = []
        errors = []
        
        for idx, row in df_upload.iterrows():
            row_no = idx + 2
            try:
                roll = int(row["Roll_No"])
            except ValueError:
                errors.append(f"Row {row_no}: Roll No must be an integer.")
                continue
                
            if roll not in registered:
                errors.append(f"Row {row_no}: Roll #{roll} is not in the student registry.")
                continue
                
            exam = str(row["Exam"]).strip()
            if exam not in EXAM_MAX_MARKS:
                errors.append(f"Row {row_no}: Exam '{exam}' invalid. Must be one of {EXAMS}.")
                continue
                
            max_m = EXAM_MAX_MARKS[exam]
            s_row = df_students[df_students["Roll_No"] == roll].iloc[0]
            
            clean_entry = {
                "Roll_No": roll,
                "Name": s_row["Name"],
                "Class": s_row["Class"],
                "Section": s_row["Section"],
                "Exam": exam,
                "Max_Marks": max_m
            }
            
            has_sub_err = False
            for sub in CORE_SUBJECTS:
                try:
                    score = float(row[sub])
                    if score < 0 or score > max_m:
                        errors.append(f"Row {row_no}: Marks for {sub} ({score}) out of range [0-{max_m}].")
                        has_sub_err = True
                        break
                    clean_entry[sub] = score
                except (ValueError, TypeError):
                    errors.append(f"Row {row_no}: Non-numeric mark in {sub}.")
                    has_sub_err = True
                    break
                    
            if not has_sub_err:
                valid_records.append(clean_entry)
                
        if not valid_records:
            return False, f"No valid rows to import. Errors: {'; '.join(errors[:4])}", None
            
        df_marks = load_marks()
        added_count = 0
        updated_count = 0
        
        for rec in valid_records:
            matches = df_marks.index[(df_marks["Roll_No"] == rec["Roll_No"]) & (df_marks["Exam"] == rec["Exam"])].tolist()
            if matches:
                for k, v in rec.items():
                    df_marks.loc[matches[0], k] = v
                updated_count += 1
            else:
                df_marks = pd.concat([df_marks, pd.DataFrame([rec])], ignore_index=True)
                added_count += 1
                
        save_marks(df_marks)
        summary = {
            "total_processed": len(df_upload),
            "added": added_count,
            "updated": updated_count,
            "errors": errors
        }
        return True, f"Ingested {len(valid_records)} rows ({added_count} added, {updated_count} updated).", summary
        
    except Exception as e:
        return False, f"File processing error: {str(e)}", None

def generate_text_report_card(student_info, marks_record, class_rank, total_students):
    """
    Generate clean, printable, formatted academic report card string.
    Uses standard Python string formatting and file handling concepts.
    (Syllabus: Strings and Working with Text Files Containing Strings)
    """
    name = student_info.get("Name", "Student")
    roll = student_info.get("Roll_No", "N/A")
    cls = student_info.get("Class", "")
    sec = student_info.get("Section", "")
    exam = marks_record.get("Exam", "")
    max_m = marks_record.get("Max_Marks", 100)
    
    border = "=" * 68
    sep = "-" * 68
    
    lines = [
        border,
        "          EXCELLENCE ACADEMY SECONDARY SCHOOL - REPORT CARD",
        "                ACADEMIC SESSION: 2025 - 2026",
        border,
        f" Student Name : {name:<26} Roll Number : {roll}",
        f" Class & Sec  : {cls} - {sec:<19} Examination : {exam}",
        f" Student Email: {student_info.get('Email', 'N/A')}",
        sep,
        f" {'SUBJECT':<20} {'MAX':<8} {'PASS':<8} {'SCORED':<10} {'STATUS':<10}",
        sep
    ]
    
    pass_mark = round(max_m * 0.40, 1)
    for sub in CORE_SUBJECTS:
        score = float(marks_record.get(sub, 0.0))
        status = "PASS" if score >= pass_mark else "FAIL"
        lines.append(f" {sub:<20} {int(max_m):<8} {pass_mark:<8} {score:<10} {status:<10}")
        
    lines.append(sep)
    tot_obtained = marks_record.get("Total_Marks", 0.0)
    tot_max = marks_record.get("Total_Max_Marks", max_m * len(CORE_SUBJECTS))
    pct = marks_record.get("Percentage", 0.0)
    grade = marks_record.get("Grade", "N/A")
    division = marks_record.get("Division", "N/A")
    res = marks_record.get("Result_Status", "N/A")
    
    lines.append(f" Total Marks  : {tot_obtained} / {int(tot_max)} ({pct}%)")
    lines.append(f" Letter Grade : {grade:<15} Division    : {division}")
    lines.append(f" Class Rank   : {class_rank} of {total_students:<12} Final Result: {res.upper()}")
    lines.append(border)
    lines.append(" Evaluation Remarks:")
    if pct >= 80:
        lines.append(" Excellent performance! Consistent conceptual understanding.")
    elif pct >= 60:
        lines.append(" Good effort. Continue regular practice and revision.")
    elif pct >= 40:
        lines.append(" Average performance. Needs more focused attention in weak subjects.")
    else:
        lines.append(" Underperforming. Needs remedial tutorial sessions and parent consultation.")
    lines.append(border)
    lines.append("\n  Class Teacher Sign.       Exam Coordinator Sign.       Principal Sign.")
    lines.append("  ___________________       ______________________       ______________\n")
    
    return "\n".join(lines)
