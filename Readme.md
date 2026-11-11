# ALU Transcript Generator

## Description

This project is an ALU Transcript Generator written in Python. It reads student grades from a CSV file, validates the grades and weights, calculates the final percentage and GPA, determines whether the student passed, and recommends formative assignments for resubmission.

## Files

- `grade-evaluator.py` - Python program for processing grades.
- `grades.csv` - Contains the assignment grades and weights.
- `organizer.sh` - Archives the current grades file and creates a new empty grades file.
- `Readme.md` - Project documentation.

## How to Run

Run the Python program:

```bash
python grade-evaluator.py
```

When prompted, enter:

```text
grades.csv
```

Run the organizer script:

```bash
./organizer.sh
```

The organizer creates an `archive` directory if needed, archives the current `grades.csv` using a timestamp, creates a new `grades.csv`, and records the operation in `organizer.log`.

## Grade Rules

- Scores must be between 0 and 100.
- Total weight must equal 100%.
- Formative weight must equal 60%.
- Summative weight must equal 40%.
- A student passes only when both Formative and Summative averages are at least 50%.
- GPA is calculated using the required 5.0 scale.

## Expected Result

For the provided grades, the program calculates:

- Final Percentage: 60.00%
- GPA: 3.00 / 5.0
- Formative Average: 56.67%
- Summative Average: 65.00%
- Final Decision: PASSED

The formative assignments below 50% are identified for possible resubmission.
