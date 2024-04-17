# Interview Question Web Scraper

## Setup

1. Set up a virtual environment
```shell
python -m venv venv
```

2. Start the virtual environment
```shell
# Windows
venv\Scripts\activate

# Mac
source venv/bin/activate
```

3 Install requirements
```shell
pip install -r requirements.txt
```

## Running Scraper
```shell
cd scrapers
python dj_api/scrapers/glassdoor_scraper.py
```

## Running Django App
```shell
python dj_api/manage.py runserver 
```

## Migrations

1. Create migration files wiht latest changes
```shell
python .\dj_api/manage.py makemigrations 
```

2. Apply changes to the database
```shell
python .\dj_api/manage.py migrate  
```