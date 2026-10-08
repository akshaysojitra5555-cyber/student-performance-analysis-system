"""
Data Visualization Module (Syllabus: Data Visualization)
Implements the 4 core visualization types specified in the PP syllabus:
1. Bar Graph
2. Histogram
3. Pie Chart
4. Line Graph
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_manager import CORE_SUBJECTS

# 1. PIE CHART: Grade Distribution (Syllabus: 'creating a Pie Chart')
def create_grade_pie_chart(df_dist):
    """Render a Pie Chart showing distribution of student grades."""
    fig = px.pie(
        df_dist,
        names="Grade",
        values="Count",
        title="<b>Grade Distribution (Pie Chart)</b>",
        color="Grade",
        color_discrete_map={
            "A+": "#16A34A",
            "A":  "#22C55E",
            "B+": "#3B82F6",
            "B":  "#06B6D4",
            "C":  "#EAB308",
            "D":  "#F97316",
            "F":  "#EF4444"
        }
    )
    fig.update_layout(height=350, margin=dict(t=40, b=20, l=20, r=20))
    return fig

# 2. BAR GRAPH: Subject Performance & Comparison (Syllabus: 'Bar Graph')
def create_subject_bar_graph(df_subj):
    """Render a Grouped Bar Graph comparing Class Average vs Highest score."""
    fig = go.Figure()
    
    # Class Average Bar
    fig.add_trace(go.Bar(
        x=df_subj["Subject"],
        y=df_subj["Class Average"],
        name="Class Average",
        marker_color="#2563EB",
        text=df_subj["Class Average"],
        textposition="outside"
    ))
    
    # Highest Score Bar
    fig.add_trace(go.Bar(
        x=df_subj["Subject"],
        y=df_subj["Highest Score"],
        name="Highest Score",
        marker_color="#10B981",
        text=df_subj["Highest Score"],
        textposition="outside"
    ))
    
    fig.update_layout(
        title="<b>Subject-Wise Class Average vs Highest (Bar Graph)</b>",
        xaxis_title="Subject",
        yaxis_title="Marks",
        barmode="group",
        height=380,
        margin=dict(t=40, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def create_student_comparison_bar_graph(df_comp, student_name):
    """Render a Bar Graph comparing an individual student's marks with class average."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_comp["Subject"],
        y=df_comp["Student Score"],
        name=f"{student_name}",
        marker_color="#3B82F6",
        text=df_comp["Student Score"],
        textposition="outside"
    ))
    
    fig.add_trace(go.Bar(
        x=df_comp["Subject"],
        y=df_comp["Class Average"],
        name="Class Average",
        marker_color="#94A3B8",
        text=df_comp["Class Average"],
        textposition="outside"
    ))
    
    fig.update_layout(
        title=f"<b>Student Marks vs Class Average (Bar Graph)</b>",
        xaxis_title="Subject",
        yaxis_title="Score",
        barmode="group",
        height=360,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    return fig

# 3. HISTOGRAM: Marks Distribution (Syllabus: 'Histogram')
def create_score_histogram(df_filtered):
    """Render a Histogram showing score frequency distribution across the class."""
    fig = px.histogram(
        df_filtered,
        x="Percentage",
        nbins=10,
        title="<b>Class Percentage Score Distribution (Histogram)</b>",
        color_discrete_sequence=["#6366F1"],
        marginal="rug"
    )
    fig.update_layout(
        xaxis_title="Aggregate Percentage (%)",
        yaxis_title="Number of Students",
        height=350,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    return fig

# 4. LINE GRAPH: Longitudinal Exam Trend (Syllabus: 'Creating Line Graph')
def create_exam_trend_line_graph(df_all_marks, roll_no=None):
    """Render a Line Graph tracking performance progression across exams."""
    exam_order = ["Unit Test", "Mid-term", "Final"]
    
    df_temp = df_all_marks.copy()
    df_temp["Total"] = df_temp[CORE_SUBJECTS].sum(axis=1)
    df_temp["Pct"] = (df_temp["Total"] / (df_temp["Max_Marks"] * len(CORE_SUBJECTS))) * 100.0
    
    # Class Average trend
    class_trend = df_temp.groupby("Exam")["Pct"].mean().reindex(exam_order).reset_index()
    
    fig = go.Figure()
    
    # Class line
    fig.add_trace(go.Scatter(
        x=class_trend["Exam"],
        y=class_trend["Pct"].round(1),
        mode="lines+markers+text",
        name="Class Average",
        line=dict(color="#475569", width=3, dash="dash"),
        marker=dict(size=8),
        text=[f"{v:.1f}%" for v in class_trend["Pct"]],
        textposition="top center"
    ))
    
    # Selected student line (if provided)
    if roll_no:
        s_data = df_temp[df_temp["Roll_No"] == roll_no]
        if not s_data.empty:
            s_name = s_data["Name"].iloc[0]
            s_trend = s_data.set_index("Exam")["Pct"].reindex(exam_order).reset_index()
            fig.add_trace(go.Scatter(
                x=s_trend["Exam"],
                y=s_trend["Pct"].round(1),
                mode="lines+markers+text",
                name=f"{s_name} (Roll #{roll_no})",
                line=dict(color="#2563EB", width=4),
                marker=dict(size=10, color="#1D4ED8"),
                text=[f"{v:.1f}%" if pd.notna(v) else "" for v in s_trend["Pct"]],
                textposition="bottom center"
            ))
            
    fig.update_layout(
        title="<b>Performance Progression Across Exams (Line Graph)</b>",
        xaxis_title="Exam Stage",
        yaxis_title="Percentage (%)",
        yaxis=dict(range=[0, 105]),
        height=380,
        margin=dict(t=40, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    return fig
