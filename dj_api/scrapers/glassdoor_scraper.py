import os
from datetime import datetime
from driver import install_web_driver

from scraper_utils.clicker_utils import (
    enter_input_by_id,
    click_button_by_css,
    click_next_button_by_css,
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
        self.curr_page: int = 1
        self.driver = install_web_driver(url)
        
        self.get_company_overview()
        self.get_interview_page()
        self.login_glassdoor()

    def close_driver(self) -> None:
        """Closes the web driver."""
        if self.driver:
            self.driver.quit()
            print("Quitted!")

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
        enter_input_by_id(os.getenv("PASSWORD"), "hardsellUserPassword", self.driver)
        click_button_by_css("button.Button[type='submit']", self.driver)
        print("Logged In!")

    def search_questions_for_position(self, position: str) -> None:
        """Search for interview questions for a specific position."""
        enter_input_by_id(position, "filter.jobTitleFTS-JobTitleAC", self.driver)
        click_element_by_data_test("ContentFiltersFindBtn", self.driver)

    def switch_to_new_page(self) -> None:
        """Shift to the next page"""
        click_next_button_by_css('[aria-label="Next"]', self.driver)
        self.curr_page += 1

    def parse_interview_questions(self):
        """Parse the interview list on the current page"""
        elements = get_all_elements_by_css(".mt-0.mb-0.my-md-std.css-l6fu5w.p-std.gd-ui-module.css-rntt2a.ec4dwm00", self.driver)

        interview_objects = []
        for element in elements:
            date_str = get_sub_element_by_tag(element, "time")
            experience = get_sub_element_by_css(element, "css-w00cnv mt-xsm mb-std")
            question = get_sub_element_by_css(element, "d-inline-block mb-sm")
            date_field = datetime.strptime(date_str, "%b %d, %Y").strftime("%Y-%m-%d")

            question_data = {
                "date_posted": date_field,
                "experience": experience,
                "question": question
            }

            interview_objects.append(question_data)

        print(interview_objects)
        print(len(interview_objects))
        return interview_objects

    @staticmethod
    def scrape_interview_questions(company: str, position: str) -> None:
        questions = []
        search_url = f"https://www.glassdoor.com/Search/results.htm?keyword={company}"
        scraper = GlassdoorScraper(search_url)
        scraper.search_questions_for_position(position)
        page = 1

        while True:
            try:
                questions += scraper.parse_interview_questions()
                print(f"Page: {page}")
                page += 1
                scraper.switch_to_new_page()

            except Exception as e:
                print(f"Failed to switch to page {page + 1}: {e}")
                break

        scraper.close_driver()
        return questions


if __name__ == "__main__":
    company = "Google"
    position = "Software Engineering Intern"
    GlassdoorScraper.scrape_interview_questions(company, position)
