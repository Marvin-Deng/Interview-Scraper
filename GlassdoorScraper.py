import os
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


from utils import export_formatted_html, enter_input_by_id, click_button_by_css, click_element_by_data_test


class GlassdoorScraper:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.driver: Optional[WebDriver] = None

    def install_web_driver(self) -> None:
        """Installs and initializes the web driver."""
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()))
            wait = WebDriverWait(self.driver, 5)
            self.driver.get(self.url)
            wait.until(EC.url_to_be(self.url))
            print("Page source obtained successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def close_driver(self) -> None:
        """Closes the web driver."""
        if self.driver:
            self.driver.quit()

    def get_company_overview(self):
        click_button_by_css("h3.d-none.d-sm-block", self.driver)
        print("In company overview")

    def get_interview_page(self) -> None:
        """Enters into interview questions page"""
        click_element_by_data_test("ei-nav-interviews-link", self.driver)
        print("In interview page")

    def login_glassdoor(self) -> None:
        """Login to Glassdoor"""
        enter_input_by_id(os.getenv("EMAIL"), "hardsellUserEmail", self.driver)
        click_element_by_data_test("email-form-button", self.driver)
        enter_input_by_id(os.getenv("PASSWORD"),
                          "hardsellUserPassword", self.driver)
        click_button_by_css("button.Button[type='submit']", self.driver)
        time.sleep(4)
        print("Logged In!")

    def search_questions_for_position(self, position: str) -> None:
        """Search for interview questions for a specific position."""
        enter_input_by_id(
            position, "filter.jobTitleFTS-JobTitleAC", self.driver)
        click_element_by_data_test("ContentFiltersFindBtn", self.driver)

    @staticmethod
    def get_interview_questions(company: str, position: str) -> None:
        search_url = f"https://www.glassdoor.com/Search/results.htm?keyword={company}"
        scraper = GlassdoorScraper(search_url)
        scraper.install_web_driver()
        scraper.get_company_overview()
        scraper.get_interview_page()
        scraper.login_glassdoor()
        scraper.search_questions_for_position(position)
        time.sleep(10)
        # scraper.close_driver()


if __name__ == "__main__":
    company = "Amazon"
    position = "Software Engineering Intern"
    GlassdoorScraper.get_interview_questions(company, position)
