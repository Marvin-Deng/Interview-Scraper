# Interview Question Web Scraper

Script for scraping interview questions from Glassdoor

## Setup

1. Set up a virtual environment

```shell
python3 -m venv venv
```

2. Start the virtual environment

```shell
# Windows
venv\Scripts\activate

# Mac
source venv/bin/activate
```

3. Install requirements

```shell
pip install -r requirements.txt
```

4. Add Glassdoor login credentials to a .env file

```shell
# .env

EMAIL=
PASSWORD=
```

## Running Scraper

```shell
options:
    -c, --company: Company name to search on Glassdoor
    -p, --position: Position to search interview questions for
    -e, --export: Format to export the interview questions. Options: 'txt', 'docx', or 'csv'

# Example:
python3 main.py -c "Google" -p "Software Engineering Intern" -e "csv"
```

## Updating requirements

```shell
pip freeze > requirements.txt
```
