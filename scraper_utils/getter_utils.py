from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .helper_utils import parse_css_selector


def get_all_elements_by_css(driver: WebDriver, css_selector: str) -> list:
    """Return all elements that match the css selector."""

    css_selector = parse_css_selector(css_selector)
    try:
        elements = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
        return elements
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_sub_element_by_css(curr_element: WebElement, css_selector: str) -> str:
    """Finds a sub-element by CSS selector within the current element and returns its text."""
    css_selector = parse_css_selector(css_selector)
    try:
        return curr_element.find_element(By.CSS_SELECTOR, css_selector).text
    except Exception:
        return ""
