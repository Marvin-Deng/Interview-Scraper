import os
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


from scraper_utils.clicker_utils import (
    export_formatted_html,
    enter_input_by_id,
    click_button_by_css,
    click_element_by_data_test,
    get_sub_element_by_tag,
    get_sub_element_by_css,
)


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

    def switch_to_next_interview_page(self):
        """Shift to the next page"""
        click_button_by_css("next-icon")

    def parse_interview_questions(self):
        time.sleep(3)
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, '.mt-0.mb-0.my-md-std.css-l6fu5w.p-std.gd-ui-module.css-rntt2a.ec4dwm00')
        
        interview_objects = []
        for element in elements:
            date = get_sub_element_by_tag(element, "time")
            experience = get_sub_element_by_css(element, "css-w00cnv mt-xsm mb-std")
            question = get_sub_element_by_css(element, "d-inline-block mb-sm")

            question_data = {
                "date": date,
                "experience": experience,
                "question": question
            }
            
            interview_objects.append(question_data)
        print(interview_objects)
        print(len(interview_objects))

    @staticmethod
    def scrape_interview_questions(company: str, position: str) -> None:
        search_url = f"https://www.glassdoor.com/Search/results.htm?keyword={company}"
        scraper = GlassdoorScraper(search_url)
        scraper.install_web_driver()
        scraper.get_company_overview()
        scraper.get_interview_page()
        scraper.login_glassdoor()
        scraper.search_questions_for_position(position)
        scraper.parse_interview_questions()
        scraper.close_driver()


if __name__ == "__main__":
    company = "Google"
    position = "Software Engineering Intern"
    GlassdoorScraper.scrape_interview_questions(company, position)
