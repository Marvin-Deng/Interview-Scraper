import os

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapers.driver import install_web_driver
from scrapers.exporter import (
    export_to_csv,
    export_to_txt,
    export_to_docx,
    export_to_pdf,
)
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

        try:
            self._get_company_overview()
            self._get_interview_page()
            self._login_glassdoor()
        except Exception as e:
            print(f"Initialization failed: {e}")
            self._close_driver()
            raise

    def _close_driver(self) -> None:
        """Closes the web driver"""
        try:
            if self.driver:
                self.driver.quit()
                print("Quitted!")
        except Exception as e:
            print(f"Failed to close driver: {e}")

    def _get_company_overview(self) -> None:
        """Clicks on a button to open the company overview page"""
        try:
            click_button_by_css("h3.d-none.d-sm-block", self.driver)
            print("In company overview")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Failed to get company overview: {e}")
            raise

    def _get_interview_page(self) -> None:
        """Enters into interview questions page"""
        try:
            click_element_by_data_test("ei-nav-interviews-link", self.driver)
            print("In interview page")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Failed to get interview page: {e}")
            raise

    def _login_glassdoor(self) -> None:
        """Enters Glassdoor login credentials into the popup"""
        try:
            enter_input_by_id(os.getenv("EMAIL"), "hardsellUserEmail", self.driver)
            click_element_by_data_test("email-form-button", self.driver)
            enter_input_by_id(
                os.getenv("PASSWORD"), "hardsellUserPassword", self.driver
            )
            click_button_by_css("button.Button[type='submit']", self.driver)
            print("Logged In!")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Failed to login to Glassdoor: {e}")
            raise

    def _search_questions_for_position(self, position: str) -> None:
        """Search for interview questions for a specific position"""
        try:
            enter_input_by_id(position, "filter.jobTitleFTS-JobTitleAC", self.driver)
            click_element_by_data_test("ContentFiltersFindBtn", self.driver)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Failed to search questions for position: {e}")
            raise

    def _switch_to_new_page(self) -> None:
        """Shift to the next page"""
        try:
            click_next_button_by_css('[aria-label="Next"]', self.driver)
            self.curr_page += 1
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Failed to switch to new page: {e}")
            raise

    def _parse_interview_questions(self) -> list:
        """Parse the interview list on the current page"""
        try:
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
                    element,
                    ".interview-details__interview-details-module__interviewText",
                )
                question_data = {
                    "date_posted": date_str,
                    "user": user,
                    "experience": experience,
                    "question": question,
                }
                interview_objects.append(question_data)
            return interview_objects
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Failed to parse interview questions: {e}")
            raise

    @staticmethod
    def scrape_company_questions(company: str, position: str, export_file: str) -> None:
        """Driver function for scraping questions and exporting files"""
        questions = []
        search_url = f"https://www.glassdoor.com/Search/results.htm?keyword={company}"
        headers = ["date_posted", "user", "experience", "question"]
        scraper = GlassdoorScraper(search_url)
        scraper._search_questions_for_position(position)
        page = 1

        try:
            while True:
                try:
                    questions += scraper._parse_interview_questions()
                    print(f"Page: {page}")
                    page += 1
                    scraper._switch_to_new_page()
                except Exception as e:
                    print(f"Failed to process page {page}: {e}")
                    break
        finally:
            scraper._close_driver()

        try:
            if export_file == "csv":
                export_to_csv(company=company, headers=headers, questions=questions)
            elif export_file == "txt":
                export_to_txt(company=company, headers=headers, questions=questions)
            elif export_file == "docx":
                export_to_docx(company=company, headers=headers, questions=questions)
            elif export_file == "pdf":
                export_to_pdf(company=company, headers=headers, questions=questions)

        except Exception as e:
            print(e)
