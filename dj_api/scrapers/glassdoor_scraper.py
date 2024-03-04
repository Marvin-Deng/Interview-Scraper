import os
import re
import time
from typing import Optional
from selenium import webdriver
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
)

from scraper_utils.getter_utils import (
    get_all_elements_by_css,
    get_sub_element_by_tag,
    get_sub_element_by_css,
)


class GlassdoorScraper:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.driver: Optional[WebDriver] = None
        self.curr_page: int = 1
        self.intervew_page_url: str = ""

        self.install_web_driver()
        self.get_company_overview()
        self.get_interview_page()
        self.login_glassdoor()

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
        print("Logged In!")

    def search_questions_for_position(self, position: str) -> None:
        """Search for interview questions for a specific position."""
        enter_input_by_id(
            position, "filter.jobTitleFTS-JobTitleAC", self.driver)
        click_element_by_data_test("ContentFiltersFindBtn", self.driver)
        self.intervew_page_url = self.driver.current_url

    def switch_to_new_page(self, new_page: int) -> None:
        """Shift to the next page"""
        url = self.intervew_page_url
        self.curr_page = new_page
        if new_page == 1:
            self.intervew_page_url = re.sub(r"_IP\d+\.htm", ".htm", )
        elif '.htm' in url:
            if re.search(r"_IP\d+\.htm", url):
                self.intervew_page_url = re.sub(
                    r"_IP\d+\.htm", f"_IP{new_page}.htm", url)
            else:
                self.intervew_page_url = re.sub(
                    r"\.htm", f"_IP{new_page}.htm", url)
        self.driver.get(self.intervew_page_url)
        print(f"Switched Pages to {new_page}!")

    def parse_interview_questions(self):
        """Parse the interview list on the current page"""
        if (self.curr_page == 1):
            elements = get_all_elements_by_css(
                ".mt-0.mb-0.my-md-std.css-l6fu5w.p-std.gd-ui-module.css-rntt2a.ec4dwm00", self.driver)
        else:
            elements = get_all_elements_by_css(
                "mt-0 mb-0 my-md-std p-std gd-ui-module css-cup1a5 ec4dwm00", self.driver)

        interview_objects = []
        for element in elements:
            date = get_sub_element_by_tag(element, "time")
            experience = get_sub_element_by_css(
                element, "css-w00cnv mt-xsm mb-std")
            question = get_sub_element_by_css(element, "d-inline-block mb-sm")

            question_data = {
                "date_posted": date,
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
        scraper.search_questions_for_position(position)
        scraper.parse_interview_questions()
        scraper.switch_to_new_page(2)
        scraper.parse_interview_questions()
        scraper.switch_to_new_page(3)
        scraper.parse_interview_questions()
        scraper.close_driver()


if __name__ == "__main__":
    company = "Google"
    position = "Software Engineering Intern"
    GlassdoorScraper.scrape_interview_questions(company, position)
