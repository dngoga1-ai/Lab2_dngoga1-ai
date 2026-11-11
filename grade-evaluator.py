import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input(
        "Enter the name of the CSV file to process (e.g., grades.csv): "
    )

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            required_fields = {
                'assignment', 'group', 'score', 'weight'
            }

            if not required_fields.issubset(reader.fieldnames or []):
                print("Error: CSV file is missing required fields.")
                sys.exit(1)

            for row in reader:
                if not row['assignment'] or not row['group']:
                    print("Error: CSV contains an empty assignment or group.")
                    sys.exit(1)

                try:
                    score = float(row['score'])
                    weight = float(row['weight'])
                except ValueError:
                    print(
                        f"Error: Invalid score or weight for "
                        f"'{row['assignment']}'."
                    )
                    sys.exit(1)

                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': score,
                    'weight': weight
                })

        if not assignments:
            print("Error: The CSV file is empty.")
            sys.exit(1)

        return assignments

    except KeyError as e:
        print(f"Error: Missing CSV field: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Validates grades, calculates the final grade and GPA,
    determines pass/fail status, and identifies
    formative assignments eligible for resubmission.
    """

    print("\n--- Processing Grades ---")

    # Check that all scores are between 0 and 100.
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(
                f"Error: Score for '{item['assignment']}' "
                f"must be between 0 and 100."
            )
            return

        if item['weight'] < 0:
            print(
                f"Error: Weight for '{item['assignment']}' "
                f"cannot be negative."
            )
            return

    # Calculate total, formative, and summative weights.
    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    for item in data:
        total_weight += item['weight']

        if item['group'].lower() == 'formative':
            formative_weight += item['weight']

        elif item['group'].lower() == 'summative':
            summative_weight += item['weight']

        else:
            print(
                f"Error: Unknown group '{item['group']}' "
                f"for '{item['assignment']}'."
            )
            return

    # Validate the required weights.
    if total_weight != 100:
        print(
            f"Error: Total weight must be 100%. "
            f"Current total is {total_weight}%."
        )
        return

    if formative_weight != 60:
        print(
            f"Error: Formative weight must be 60%. "
            f"Current total is {formative_weight}%."
        )
        return

    if summative_weight != 40:
        print(
            f"Error: Summative weight must be 40%. "
            f"Current total is {summative_weight}%."
        )
        return

    # Calculate weighted final percentage.
    total_score = 0

    for item in data:
        total_score += item['score'] * (item['weight'] / 100)

    # GPA formula from the rubric:
    # GPA = Total / 100 * 5.0
    gpa = (total_score / 100) * 5.0

    # Calculate average for each category.
    formative_score = 0
    summative_score = 0

    for item in data:
        if item['group'].lower() == 'formative':
            formative_score += item['score'] * (
                item['weight'] / formative_weight
            )

        elif item['group'].lower() == 'summative':
            summative_score += item['score'] * (
                item['weight'] / summative_weight
            )

    # A student must score at least 50% in BOTH categories.
    formative_pass = formative_score >= 50
    summative_pass = summative_score >= 50

    passed = formative_pass and summative_pass

    # Find failed formative assignments.
    failed_formative = []

    for item in data:
        if (
            item['group'].lower() == 'formative'
            and item['score'] < 50
        ):
            failed_formative.append(item)

    # Find the highest weight among failed formative assignments.
    resubmission = []

    if failed_formative:
        highest_weight = failed_formative[0]['weight']

        for item in failed_formative:
            if item['weight'] > highest_weight:
                highest_weight = item['weight']

        for item in failed_formative:
            if item['weight'] == highest_weight:
                resubmission.append(item)

    # Display results.
    print(f"\nFinal Percentage: {total_score:.2f}%")
    print(f"GPA: {gpa:.2f} / 5.0")
    print(f"Formative Average: {formative_score:.2f}%")
    print(f"Summative Average: {summative_score:.2f}%")

    if passed:
        print("\nFinal Decision: PASSED")
    else:
        print("\nFinal Decision: FAILED")

    if resubmission:
        print("\nFormative assignment(s) recommended for resubmission:")

        for item in resubmission:
            print(
                f"- {item['assignment']} "
                f"(Score: {item['score']:.2f}%, "
                f"Weight: {item['weight']:.2f}%)"
            )
    else:
        print("\nNo formative resubmission is required.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)