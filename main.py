import argparse

from scrapers.scraper import GlassdoorScraper


def main():
    parser = argparse.ArgumentParser(
        description="Scrape interview questions from Glassdoor."
    )
    parser.add_argument(
        "-c",
        "--company",
        type=str,
        required=True,
        help="Company name to search on Glassdoor",
    )
    parser.add_argument(
        "-p",
        "--position",
        type=str,
        required=True,
        help="Position to search interview questions for",
    )

    args = parser.parse_args()
    company = args.company
    position = args.position

    GlassdoorScraper.scrape_company_questions(company=company, position=position)


if __name__ == "__main__":
    main()
