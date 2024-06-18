import os

from scrapers.driver import install_web_driver
from scraper_utils.clicker_utils import (
    enter_input_by_id,
    click_button_by_css,
    click_next_button_by_css,
    click_element_by_data_test,
)
from scraper_utils.getter_utils import (
    get_all_elements_by_css,
    get_sub_element_by_css,
)


class GlassdoorScraper:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.curr_page: int = 1
        self.driver = install_web_driver(url)

        self._get_company_overview()
        self._get_interview_page()
        self._login_glassdoor()

    def _close_driver(self) -> None:
        """Closes the web driver"""
        if self.driver:
            self.driver.quit()
            print("Quitted!")

    def _get_company_overview(self) -> None:
        """Clicks on a button to open the company overview page"""
        click_button_by_css("h3.d-none.d-sm-block", self.driver)
        print("In company overview")

    def _get_interview_page(self) -> None:
        """Enters into interview questions page"""
        click_element_by_data_test("ei-nav-interviews-link", self.driver)
        print("In interview page")

    def _login_glassdoor(self) -> None:
        """Enters Glassdoor login credentials into the popup"""
        enter_input_by_id(os.getenv("EMAIL"), "hardsellUserEmail", self.driver)
        click_element_by_data_test("email-form-button", self.driver)
        enter_input_by_id(os.getenv("PASSWORD"), "hardsellUserPassword", self.driver)
        click_button_by_css("button.Button[type='submit']", self.driver)
        print("Logged In!")

    def _search_questions_for_position(self, position: str) -> None:
        """Search for interview questions for a specific position"""
        enter_input_by_id(position, "filter.jobTitleFTS-JobTitleAC", self.driver)
        click_element_by_data_test("ContentFiltersFindBtn", self.driver)

    def _switch_to_new_page(self) -> None:
        """Shift to the next page"""
        click_next_button_by_css('[aria-label="Next"]', self.driver)
        self.curr_page += 1

    def _parse_interview_questions(self) -> list:
        """Parse the interview list on the current page"""
        elements = get_all_elements_by_css(
            self.driver,
            ".InterviewContainer__InterviewDetailsStyles__interviewContainer",
        )

        interview_objects = []
        for element in elements:
            date_str = get_sub_element_by_css(
                element, ".timestamp__timestamp-module__reviewDate"
            )
            user = get_sub_element_by_css(
                element, ".interview-details__interview-details-module__userLine"
            )
            experience = get_sub_element_by_css(
                element,
                ".truncated-text__truncated-text-module__truncate.interview-details__interview-details-module__textStyle",
            )
            question = get_sub_element_by_css(
                element, ".interview-details__interview-details-module__interviewText"
            )

            question_data = {
                "date_posted": date_str,
                "user": user,
                "experience": experience,
                "question": question,
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
        scraper._search_questions_for_position(position)
        page = 1

        while True:
            try:
                questions += scraper._parse_interview_questions()
                print(f"Page: {page}")
                page += 1
                scraper._switch_to_new_page()

            except Exception as e:
                print(f"Failed to switch to page {page + 1}: {e}")
                break

        scraper._close_driver()
        return questions
