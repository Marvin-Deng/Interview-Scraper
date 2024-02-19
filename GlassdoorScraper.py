import os
import time
from typing import Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


from utils import export_formatted_html, enter_input_by_id, click_button_by_class, click_button_by_css, click_element_by_data_test


class GlassdoorScraper:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.driver: Optional[WebDriver] = None
        self.wait: Optional[WebDriverWait] = None
        self.page_source: Optional[str] = None

    def install_web_driver(self) -> None:
        """Installs and initializes the web driver."""
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()))
            self.wait = WebDriverWait(self.driver, 5)
            self.driver.get(self.url)
            self.wait.until(EC.url_to_be(self.url))
            self.page_source = self.driver.page_source
            print("Page source obtained successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def close_driver(self) -> None:
        """Closes the web driver."""
        if self.driver:
            self.driver.quit()

    def get_company_overview(self):
        click_button_by_css("h3.d-none.d-sm-block", self.driver)

    def login_glassdoor(self) -> None:
        """Login to Glassdoor"""
        enter_input_by_id(os.getenv("EMAIL"), "hardsellUserEmail", self.driver)
        click_button_by_class("ButtonContent", self.driver)

    def get_interview_page(self) -> None:
        """Enters into interview questions page"""

    @staticmethod
    def get_interview_questions(company: str) -> None:
        search_url = f"https://www.glassdoor.com/Search/results.htm?keyword={company}"
        scraper = GlassdoorScraper(search_url)
        scraper.install_web_driver()
        scraper.get_company_overview()
        # scraper.login_glassdoor()
        time.sleep(10)
        # scraper.close_driver()


if __name__ == "__main__":
    company = "Amazon"
    GlassdoorScraper.get_interview_questions(company)
