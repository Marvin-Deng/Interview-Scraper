from scrapers.scraper import GlassdoorScraper

if __name__ == "__main__":
    company = "Google"
    position = "Software Engineering Intern"
    GlassdoorScraper.scrape_interview_questions(company, position)
