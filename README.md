# Interview Question Web Scraper

## Setup

1. Set up a virtual environment
```shell
python -m venv venv
```

2. Install requirements
```shell
pip install requirements.txt
```

## Running Scraper
```shell 
python dj_api/scrapers/glassdoor_scraper.py
```

## Running Django App
```shell
python .\manage.py runserver 
```

## Migrations

1. Create migration files wiht latest changes
```shell
python .\manage.py makemigrations 
```

2. Apply changes to the database
```shell
python .\manage.py migrate  
```