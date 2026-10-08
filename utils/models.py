"""
OOP Models Module (Syllabus Unit: Classes and Object-Oriented Programming)
Defines Student and Result classes demonstrating:
- Constructors (__init__)
- Encapsulation & methods
- User-defined exception handling
"""

class InvalidMarksError(Exception):
    """User-defined exception raised when marks are out of valid range."""
    pass

class Student:
    """
    Student class representing an enrolled learner.
    Demonstrates encapsulation and object-oriented representation.
    """
    def __init__(self, roll_no, name, class_name, section, gender, email):
        self.roll_no = int(roll_no)
        self.name = str(name).strip()
        self.class_name = str(class_name).strip()
        self.section = str(section).strip()
        self.gender = str(gender).strip()
        self.email = str(email).strip()

    def to_dict(self):
        """Convert student object to a standard Python dictionary."""
        return {
            "Roll_No": self.roll_no,
            "Name": self.name,
            "Class": self.class_name,
            "Section": self.section,
            "Gender": self.gender,
            "Email": self.email
        }

    def __str__(self):
        """String representation of student object."""
        return f"Student(Roll: {self.roll_no}, Name: '{self.name}', Class: {self.class_name}-{self.section})"


class StudentResult:
    """
    Result class representing marks obtained across subjects for an exam.
    Computes total, percentage, grade, division, and pass/fail status.
    """
    def __init__(self, student, exam_name, marks_dict, max_marks_per_subject=100):
        self.student = student
        self.exam_name = exam_name
        self.marks = marks_dict  # Dictionary: {subject: score}
        self.max_marks = max_marks_per_subject
        
        # Validate marks using exception handling
        for sub, score in self.marks.items():
            if score < 0 or score > self.max_marks:
                raise InvalidMarksError(f"Marks for {sub} ({score}) must be between 0 and {self.max_marks}")

    def calculate_total(self):
        """Calculate total marks obtained."""
        return round(sum(self.marks.values()), 1)

    def calculate_total_max(self):
        """Calculate maximum total marks possible."""
        return self.max_marks * len(self.marks)

    def calculate_percentage(self):
        """Calculate percentage obtained."""
        total_max = self.calculate_total_max()
        if total_max == 0:
            return 0.0
        return round((self.calculate_total() / total_max) * 100.0, 2)

    def get_failed_subjects(self, passing_percentage=40.0):
        """
        List comprehension returning subjects where score < 40% of max.
        (Syllabus: List comprehension)
        """
        threshold = (passing_percentage / 100.0) * self.max_marks
        return [sub for sub, score in self.marks.items() if score < threshold]

    def is_passed(self):
        """Student passes if they pass all individual subjects and overall % >= 40."""
        return len(self.get_failed_subjects()) == 0 and self.calculate_percentage() >= 40.0

    def calculate_grade(self):
        """Determine letter grade A+ through F based on percentage."""
        pct = self.calculate_percentage()
        if pct >= 90.0:
            return "A+"
        elif pct >= 80.0:
            return "A"
        elif pct >= 70.0:
            return "B+"
        elif pct >= 60.0:
            return "B"
        elif pct >= 50.0:
            return "C"
        elif pct >= 40.0:
            return "D"
        else:
            return "F"

    def calculate_division(self):
        """Determine academic division."""
        if not self.is_passed():
            return "Failed"
        pct = self.calculate_percentage()
        if pct >= 60.0:
            return "1st Division"
        elif pct >= 50.0:
            return "2nd Division"
        elif pct >= 40.0:
            return "3rd Division"
        else:
            return "Failed"
