"""Reusable calculations for the student performance analytics project."""

import numpy as np
import pandas as pd


GRADE_THRESHOLDS = ((90, "A"), (80, "B"), (70, "C"), (60, "D"))
PASSING_MARKS = 40
MINIMUM_PASSING_AVERAGE = 60
MINIMUM_ATTENDANCE = 75


def validate_student_data(data, subject_columns):
    """Check required columns and ensure scores and attendance are valid."""
    required_columns = [
        "Student ID",
        "Name",
        "Department",
        "Attendance (%)",
        *subject_columns,
    ]
    missing_columns = [column for column in required_columns if column not in data]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    if data.empty:
        raise ValueError("The student dataset contains no records.")

    numeric_columns = [*subject_columns, "Attendance (%)"]
    for column in numeric_columns:
        values = pd.to_numeric(data[column], errors="coerce")
        if values.isna().any():
            raise ValueError(f"Column '{column}' must contain only numeric values.")
        if not values.between(0, 100).all():
            raise ValueError(f"Column '{column}' values must be between 0 and 100.")


def assign_grade(average_marks):
    """Return a letter grade based on the student's average marks."""
    for minimum_average, grade in GRADE_THRESHOLDS:
        if average_marks >= minimum_average:
            return grade
    return "F"


def process_student_data(data, subject_columns):
    """Return a copy of the data with totals, averages, grades, and status."""
    validate_student_data(data, subject_columns)
    processed = data.copy()
    marks = processed[subject_columns].to_numpy(dtype=float)

    processed[subject_columns] = marks
    processed["Total Marks"] = np.sum(marks, axis=1).astype(int)
    processed["Average Marks"] = np.mean(marks, axis=1)

    grades = []
    results = []
    for index, average in enumerate(processed["Average Marks"]):
        grades.append(assign_grade(average))
        passed_subjects = (
            average >= MINIMUM_PASSING_AVERAGE
            and np.all(marks[index] >= PASSING_MARKS)
        )
        attendance_is_sufficient = processed.iloc[index]["Attendance (%)"] >= MINIMUM_ATTENDANCE
        results.append("Pass" if passed_subjects and attendance_is_sufficient else "Fail")

    processed["Grade"] = grades
    processed["Result"] = results
    return processed


def get_subject_summary(processed_data, subject_columns):
    """Calculate average, highest, and lowest marks for each subject."""
    subject_results = []
    for subject in subject_columns:
        marks = processed_data[subject].to_numpy(dtype=float)
        subject_results.append(
            {
                "Subject": subject,
                "Average": np.mean(marks),
                "Highest": np.max(marks),
                "Lowest": np.min(marks),
            }
        )

    return pd.DataFrame(subject_results).sort_values("Average", ascending=False)


def get_class_summary(processed_data):
    """Summarize class averages and pass/fail counts."""
    averages = processed_data["Average Marks"].to_numpy(dtype=float)
    return {
        "student_count": len(processed_data),
        "overall_average": np.mean(averages),
        "highest_average": np.max(averages),
        "lowest_average": np.min(averages),
        "pass_count": int((processed_data["Result"] == "Pass").sum()),
        "fail_count": int((processed_data["Result"] == "Fail").sum()),
    }


def get_top_performers(processed_data):
    """Return every student tied for the highest average mark."""
    highest_average = processed_data["Average Marks"].max()
    return processed_data.loc[
        processed_data["Average Marks"] == highest_average
    ].sort_values("Name")