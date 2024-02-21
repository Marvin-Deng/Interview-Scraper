from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_all_elements_by_css(css_selector: str, driver: WebDriver) -> list:
    """Return all elements that match the css selector."""
    if ' ' in css_selector:
        css_selector = '.' + '.'.join(css_selector.split())
    print(driver.current_url)
    try:
        elements = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, css_selector))
        )
        
        return elements
    except Exception:
        print("Error occured")
        return []


def get_sub_element_by_css(curr_element: WebElement, css_selector: str) -> str:
    """Finds a sub-element by CSS selector within the current element and returns its text."""
    if ' ' in css_selector:
        css_selector = '.' + '.'.join(css_selector.split())

    try:
        return curr_element.find_element(By.CSS_SELECTOR, css_selector).text
    except Exception:
        return ""


def get_sub_element_by_tag(curr_element: WebElement, tag: str) -> str:
    """Finds a sub-element by tag within the current element and returns its text."""
    try:
        return curr_element.find_element(By.TAG_NAME, tag).text
    except Exception:
        return ""
