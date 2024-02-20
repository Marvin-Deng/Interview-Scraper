from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def enter_input_by_id(input_text: str, input_id: str, driver: WebDriver) -> None:
    """Enter info into an input bar given its id."""
    try:
        input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, input_id)))
        input.clear()
        input.send_keys(input_text)
    except TimeoutException:
        print(
            f"Timeout: Input with ID '{input_id}' not visible within the wait time.")
    except NoSuchElementException:
        print(f"Error: Input with ID '{input_id}' not found.")


def click_button_by_css(css: str, driver: WebDriver) -> None:
    """Click on the first button matching the css."""
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css))).click()
    except TimeoutException:
        print(
            f"Timeout: Button with css '{css}' not clickable within the wait time.")
    except NoSuchElementException:
        print(f"Error: Button with css '{css}' not found.")


def click_element_by_data_test(data_test_value: str, driver: WebDriver) -> None:
    """Click on the first element matching the data-test attribute."""
    try:
        css_selector = f'[data-test="{data_test_value}"]'
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, css_selector))).click()
    except TimeoutException:
        print(
            f"Timeout: Element with data-test='{data_test_value}' not clickable within the wait time.")
    except NoSuchElementException:
        print(f"Error: Element with data-test='{data_test_value}' not found.")

def get_elements_by_css(css: str, driver: WebDriver) -> None:

    css_selector = css
    if ' ' in css:
        css_selector = '.' + '.'.join(css.split())

    try:
        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        elements_list = []

        for element in elements:
            elements_list.append(element.text)
            
        return elements_list

    except Exception as e:
        print(f"An error occurred while trying to extract elements: {e}")


def export_formatted_html(soup: BeautifulSoup, file_name: str = "output.txt") -> None:
    """Exports formatted HTML from a BeautifulSoup object to a text file."""
    formatted_html = soup.prettify()

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(formatted_html)
    print(f"Formatted HTML has been written to {file_name}")
