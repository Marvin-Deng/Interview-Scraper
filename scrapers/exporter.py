import csv


def export_to_txt(company: str, headers: list, questions: list) -> None:
    """Export interview questions to a TXT file"""
    try:
        filename = f"{company}_questions.txt"
        with open(filename, "w") as file:
            file.write(f"Interview Questions for {company}\n\n")
            for question in questions:
                for header in headers:
                    file.write(f"{header}: {question.get(header, '')}\n")
                file.write("\n")
    except Exception as e:
        raise Exception(f"An error occurred while exporting to TXT: {e}")


def export_to_csv(company: str, headers: list, questions: list) -> None:
    """Export interview questions to a CSV file"""
    filename = f"{company}_questions.csv"
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
