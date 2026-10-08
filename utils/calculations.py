"""
Calculations Engine (Syllabus Units: Functions, Structured Types, Data Frames)
Demonstrates:
- Functions returning multiple values
- Positional, keyword, and default arguments
- List comprehensions and Lambda functions
- DataFrame operations: filtering, grouping, aggregation
"""
import pandas as pd
from utils.data_manager import CORE_SUBJECTS

def calculate_grade(percentage):
    """
    Calculate letter grade from percentage.
    (Syllabus: Branching programs if-elif-else)
    """
    if percentage >= 90.0:
        return "A+"
    elif percentage >= 80.0:
        return "A"
    elif percentage >= 70.0:
        return "B+"
    elif percentage >= 60.0:
        return "B"
    elif percentage >= 50.0:
        return "C"
    elif percentage >= 40.0:
        return "D"
    else:
        return "F"

def calculate_division(percentage, is_passed=True):
    """
    Determine division with default argument is_passed=True.
    (Syllabus: Default Arguments)
    """
    if not is_passed:
        return "Failed"
    if percentage >= 60.0:
        return "1st Division"
    elif percentage >= 50.0:
        return "2nd Division"
    elif percentage >= 40.0:
        return "3rd Division"
    else:
        return "Failed"

def calculate_student_results(df_marks):
    """
    Enrich raw marks DataFrame with totals, percentage, grades, division, and ranks.
    (Syllabus: Operations on Data Frames)
    """
    if df_marks.empty:
        return pd.DataFrame()
        
    df = df_marks.copy()
    
    # 1. Total Marks Scored
    df["Total_Marks"] = df[CORE_SUBJECTS].sum(axis=1).round(1)
    
    # 2. Maximum Marks Total
    df["Total_Max_Marks"] = df["Max_Marks"] * len(CORE_SUBJECTS)
    
    # 3. Percentage
    df["Percentage"] = ((df["Total_Marks"] / df["Total_Max_Marks"]) * 100.0).round(2)
    
    # 4. Check Individual Subject Pass (minimum 40% in each subject)
    def evaluate_pass_status(row):
        max_m = row["Max_Marks"]
        pass_cutoff = max_m * 0.40
        # List comprehension (Syllabus: List Comprehension)
        failed_subs = [sub for sub in CORE_SUBJECTS if row[sub] < pass_cutoff]
        is_pass = (len(failed_subs) == 0) and (row["Percentage"] >= 40.0)
        status = "Pass" if is_pass else "Fail"
        failed_str = ", ".join(failed_subs) if failed_subs else "None"
        # Returning multiple values (Syllabus: Returning Multiple Values from a Function)
        return pd.Series([status, failed_str, len(failed_subs)], index=["Result_Status", "Failed_Subjects", "Failed_Count"])
        
    eval_df = df.apply(evaluate_pass_status, axis=1)
    df["Result_Status"] = eval_df["Result_Status"]
    df["Failed_Subjects"] = eval_df["Failed_Subjects"]
    df["Failed_Count"] = eval_df["Failed_Count"]
    
    # 5. Grade & Division using Lambda function (Syllabus: Anonymous Functions or Lambdas)
    df["Grade"] = df["Percentage"].apply(lambda p: calculate_grade(p))
    df["Division"] = df.apply(lambda r: calculate_division(r["Percentage"], r["Result_Status"] == "Pass"), axis=1)
    
    # 6. Class Rank (Groupby and Rank operations on DataFrame)
    df["Class_Rank"] = (
        df.groupby(["Class", "Section", "Exam"])["Percentage"]
        .rank(method="min", ascending=False)
        .astype(int)
    )
    
    return df

def get_class_summary_metrics(df_results):
    """
    Calculate summary statistics for the filtered dataset.
    Returns dictionary of results.
    """
    if df_results.empty:
        return {
            "total_students": 0, "class_avg": 0.0, "highest_pct": 0.0,
            "lowest_pct": 0.0, "pass_pct": 0.0, "passed_count": 0, "failed_count": 0
        }
        
    total = len(df_results)
    avg_pct = round(df_results["Percentage"].mean(), 2)
    highest_pct = round(df_results["Percentage"].max(), 2)
    lowest_pct = round(df_results["Percentage"].min(), 2)
    
    passed_count = int((df_results["Result_Status"] == "Pass").sum())
    failed_count = total - passed_count
    pass_pct = round((passed_count / total) * 100.0, 1) if total > 0 else 0.0
    
    return {
        "total_students": total,
        "class_avg": avg_pct,
        "highest_pct": highest_pct,
        "lowest_pct": lowest_pct,
        "pass_pct": pass_pct,
        "passed_count": passed_count,
        "failed_count": failed_count
    }

def get_subject_statistics(df_results):
    """Compute mean, min, max, and pass count per subject."""
    if df_results.empty:
        return pd.DataFrame()
        
    records = []
    max_m = df_results["Max_Marks"].iloc[0] if "Max_Marks" in df_results.columns else 100
    pass_cutoff = max_m * 0.40
    
    for sub in CORE_SUBJECTS:
        scores = df_results[sub]
        avg_score = round(scores.mean(), 1)
        highest_score = round(scores.max(), 1)
        lowest_score = round(scores.min(), 1)
        pass_count = (scores >= pass_cutoff).sum()
        pass_rate = round((pass_count / len(scores)) * 100.0, 1)
        
        topper_row = df_results.loc[scores.idxmax()]
        topper_info = f"{topper_row['Name']} ({highest_score})"
        
        records.append({
            "Subject": sub,
            "Max Marks": int(max_m),
            "Class Average": avg_score,
            "Highest Score": highest_score,
            "Lowest Score": lowest_score,
            "Pass Rate": f"{pass_rate}%",
            "Subject Topper": topper_info
        })
        
    return pd.DataFrame(records)

def get_grade_distribution(df_results):
    """Calculate grade counts for Pie and Bar charts."""
    all_grades = ["A+", "A", "B+", "B", "C", "D", "F"]
    if df_results.empty:
        return pd.DataFrame({"Grade": all_grades, "Count": [0]*7})
        
    counts = df_results["Grade"].value_counts().reindex(all_grades, fill_value=0)
    return pd.DataFrame({"Grade": all_grades, "Count": counts.values})

def get_top_and_bottom_students(df_results, n=10):
    """
    Return top N and bottom N students.
    Returns two DataFrames (Multiple return values).
    """
    if df_results.empty:
        return pd.DataFrame(), pd.DataFrame()
        
    cols = ["Class_Rank", "Roll_No", "Name", "Class", "Section", "Total_Marks", "Percentage", "Grade", "Result_Status"]
    sorted_df = df_results.sort_values(by="Percentage", ascending=False)
    top_n = sorted_df.head(n)[cols].copy()
    bottom_n = df_results.sort_values(by="Percentage", ascending=True).head(n)[cols].copy()
    return top_n, bottom_n

def get_at_risk_students(df_results):
    """Identify students scoring below 40% or failing subjects."""
    if df_results.empty:
        return pd.DataFrame()
        
    at_risk = df_results[
        (df_results["Result_Status"] == "Fail") | 
        (df_results["Percentage"] < 40.0) |
        (df_results["Failed_Count"] > 0)
    ].copy()
    
    cols = ["Roll_No", "Name", "Class", "Section", "Percentage", "Grade", "Failed_Subjects", "Result_Status"]
    return at_risk[cols].sort_values(by="Percentage", ascending=True)

def get_student_vs_class_comparison(df_results, roll_no):
    """Compare student scores with class average across subjects."""
    match = df_results[df_results["Roll_No"] == roll_no]
    if match.empty:
        return pd.DataFrame()
        
    s = match.iloc[0]
    comp_list = []
    
    for sub in CORE_SUBJECTS:
        s_score = s[sub]
        c_avg = round(df_results[sub].mean(), 1)
        diff = round(s_score - c_avg, 1)
        comp_list.append({
            "Subject": sub,
            "Student Score": s_score,
            "Class Average": c_avg,
            "Difference": diff,
            "Remark": "Above Average" if diff > 0 else ("Equal" if diff == 0 else "Below Average")
        })
    return pd.DataFrame(comp_list)
