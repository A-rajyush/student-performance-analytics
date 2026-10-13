# Student Performance Analytics System

A small Python command-line project that reads student records from a CSV file and reports student marks, grades, pass/fail results, subject performance, and top performers. Pandas organizes the dataset and NumPy performs the numerical calculations.

## Project files

- `main.py` loads the CSV and prints the analysis report.
- `functions.py` contains reusable validation, grading, and analysis functions.
- `students.csv` contains 20 sample students in four departments.
- `requirements.txt` lists the Python dependencies.

## Rules used

- Each subject is scored from 0 to 100; attendance is a percentage from 0 to 100.
- Average marks of 90 or above receive A, 80-89.99 B, 70-79.99 C, and 60-69.99 D; below 60 receives F.
- A student passes only if the average is at least 60, every subject mark is at least 40, and attendance is at least 75%. Otherwise, the result is Fail.
- Top performers include every student tied for the highest average.

## Run

From this project directory, create and activate a virtual environment, install the dependencies, and run the report:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

The report displays the source records, each student's total, average, grade and result, class-level statistics, subject averages and ranges, top performer(s), and grade distribution.

## Run with Docker

Build the image and run the bundled sample dataset:

```powershell
docker build -t student-performance-analytics .
docker run --rm student-performance-analytics
```

To analyze another CSV, mount its containing directory and pass the mounted CSV path as the first argument:

```powershell
docker run --rm -v "${PWD}:/data" student-performance-analytics /data/students.csv
```

## Publish for deployment

Pushing to `main` or publishing a `v*` tag runs the GitHub Actions workflow, which builds the container and publishes it to GitHub Container Registry. After the first successful workflow run, the image is available as `ghcr.io/a-rajyush/student-performance-analytics:latest` (or by version tag). The workflow can also be started manually from the repository's Actions tab.