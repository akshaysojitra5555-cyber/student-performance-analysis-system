"""
Simple PDF Report Card Generator
A lightweight, straightforward PDF generator using basic ReportLab canvas.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from utils.data_manager import CORE_SUBJECTS

def generate_pdf_report_card(student_info, marks_record, class_rank, total_students):
    """
    Generate a simple, clean A4 PDF report card using basic canvas drawing.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # 1. School Header
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "EXCELLENCE ACADEMY SECONDARY SCHOOL")
    
    p.setFont("Helvetica", 11)
    p.drawCentredString(width / 2, height - 70, "STUDENT PERFORMANCE REPORT CARD")
    p.setFont("Helvetica-Oblique", 9)
    p.drawCentredString(width / 2, height - 85, "Academic Session: 2025 - 2026")
    p.line(50, height - 95, width - 50, height - 95)
    
    # 2. Student Bio Details
    p.setFont("Helvetica-Bold", 10)
    y = height - 120
    p.drawString(50, y, f"Student Name : {student_info.get('Name')}")
    p.drawString(320, y, f"Roll Number  : {student_info.get('Roll_No')}")
    y -= 20
    p.drawString(50, y, f"Class & Sec  : {student_info.get('Class')} - {student_info.get('Section')}")
    p.drawString(320, y, f"Examination  : {marks_record.get('Exam')}")
    
    # 3. Table Header
    y -= 35
    p.line(50, y + 15, width - 50, y + 15)
    p.drawString(50, y, "Subject")
    p.drawString(200, y, "Max Marks")
    p.drawString(300, y, "Marks Scored")
    p.drawString(420, y, "Status")
    p.line(50, y - 5, width - 50, y - 5)
    
    # 4. Subject Rows
    p.setFont("Helvetica", 10)
    max_m = float(marks_record.get("Max_Marks", 100))
    for sub in CORE_SUBJECTS:
        y -= 25
        score = float(marks_record.get(sub, 0.0))
        status = "Pass" if score >= (max_m * 0.4) else "Fail"
        p.drawString(50, y, sub)
        p.drawString(200, y, str(int(max_m)))
        p.drawString(300, y, str(score))
        p.drawString(420, y, status)
        
    y -= 15
    p.line(50, y, width - 50, y)
    
    # 5. Overall Academic Summary
    y -= 30
    p.setFont("Helvetica-Bold", 10)
    tot_score = marks_record.get('Total_Marks')
    tot_max = int(marks_record.get('Total_Max_Marks', max_m * len(CORE_SUBJECTS)))
    p.drawString(50, y, f"Total Marks  : {tot_score} / {tot_max}")
    p.drawString(300, y, f"Percentage   : {marks_record.get('Percentage')}%")
    y -= 20
    p.drawString(50, y, f"Grade        : {marks_record.get('Grade')}")
    p.drawString(300, y, f"Division     : {marks_record.get('Division')}")
    y -= 20
    p.drawString(50, y, f"Class Rank   : #{class_rank} of {total_students}")
    p.drawString(300, y, f"Final Result : {marks_record.get('Result_Status')}")
    
    # 6. Signatures
    y -= 70
    p.setFont("Helvetica", 10)
    p.drawString(50, y, "Class Teacher Sign: ____________")
    p.drawString(330, y, "Principal Sign: ____________")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()
