import csv


def export_to_csv(company: str, questions: list):
    """Export interview questions to a CSV file"""
    headers = ["date_posted", "user", "experience", "question"]
    filename = f"{company}_interview_questions.csv"
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for question in questions:
                writer.writerow(
                    {header: question.get(header, "") for header in headers}
                )
    except IOError as e:
        raise Exception(f"Failed to export interview questions: {e}")
