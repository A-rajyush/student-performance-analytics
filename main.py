"""Load student records and print a readable performance report."""

import argparse
from pathlib import Path

import pandas as pd

from functions import (
    get_class_summary,
    get_subject_summary,
    get_top_performers,
    process_student_data,
)


SUBJECT_COLUMNS = ["Math", "Science", "English", "Computer Science"]
DATA_FILE = Path(__file__).with_name("students.csv")


def main(data_file=DATA_FILE):
    """Run the student performance analysis and display its results."""
    students = pd.read_csv(data_file)
    processed = process_student_data(students, SUBJECT_COLUMNS)
    class_summary = get_class_summary(processed)
    subject_summary = get_subject_summary(processed, SUBJECT_COLUMNS)
    top_performers = get_top_performers(processed)

    print("STUDENT PERFORMANCE ANALYTICS")
    print("=" * 78)
    print(
        f"Loaded {class_summary['student_count']} students across "
        f"{students['Department'].nunique()} departments."
    )
    print("\nSTUDENT RECORDS")
    print(students.to_string(index=False))

    print("\nSTUDENT MARKS SUMMARY")
    display_columns = [
        "Student ID",
        "Name",
        "Total Marks",
        "Average Marks",
        "Grade",
        "Result",
    ]
    print(
        processed[display_columns]
        .sort_values("Average Marks", ascending=False)
        .to_string(index=False, formatters={"Average Marks": "{:.2f}".format})
    )

    print("\nCLASS SUMMARY")
    print(f"Overall class average: {class_summary['overall_average']:.2f}")
    print(f"Highest student average: {class_summary['highest_average']:.2f}")
    print(f"Lowest student average: {class_summary['lowest_average']:.2f}")
    print(
        f"Pass: {class_summary['pass_count']} | "
        f"Fail: {class_summary['fail_count']}"
    )

    print("\nSUBJECT-WISE PERFORMANCE")
    print(
        subject_summary.to_string(
            index=False,
            formatters={
                "Average": "{:.2f}".format,
                "Highest": "{:.0f}".format,
                "Lowest": "{:.0f}".format,
            },
        )
    )
    best_subject = subject_summary.iloc[0]
    print(
        f"Best-performing subject: {best_subject['Subject']} "
        f"(average {best_subject['Average']:.2f})"
    )

    print("\nTOP PERFORMER(S)")
    print(
        top_performers[["Student ID", "Name", "Department", "Average Marks", "Grade"]]
        .to_string(index=False, formatters={"Average Marks": "{:.2f}".format})
    )

    print("\nGRADE DISTRIBUTION")
    grade_counts = processed["Grade"].value_counts().reindex(
        ["A", "B", "C", "D", "F"], fill_value=0
    )
    for grade, count in grade_counts.items():
        print(f"{grade}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze student performance from a CSV file.")
    parser.add_argument(
        "data_file",
        nargs="?",
        type=Path,
        default=DATA_FILE,
        help="CSV file to analyze (defaults to the bundled students.csv).",
    )
    main(parser.parse_args().data_file)