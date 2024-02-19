from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def enter_input_by_id(input_text: str, input_id: str, driver: WebDriver) -> None:
    """Enter info into an input bar given its id."""
    try:
        email_input = driver.find_element(By.ID, input_id)
        email_input.clear()
        email_input.send_keys(input_text)
    except NoSuchElementException:
        print(f"Error: Input with ID '{input_id}' not found.")


def click_button_by_css(css: str, driver: WebDriver) -> None:
    """Click on the first button matching the css"""
    try:
        button = driver.find_element(By.CSS_SELECTOR, css)
        button.click()
    except NoSuchElementException:
        print(f"Error: Button with css name '{css}' not found.")


def click_button_by_class(class_name: str, driver: WebDriver) -> None:
    """Click on the first button matching the class name"""
    try:
        button = driver.find_element(By.CLASS_NAME, class_name)
        button.click()
    except NoSuchElementException:
        print(f"Error: Button with class name '{class_name}' not found.")

def click_element_by_data_test(data_test_value: str, driver: WebDriver) -> None:
    """Click on the first element matching the data-test attribute."""
    try:
        css_selector = f'[data-test="{data_test_value}"]'
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        element.click()
    except NoSuchElementException:
        print(f"Error: Element with data-test='{data_test_value}' not found.")


def export_formatted_html(soup: BeautifulSoup, file_name: str = "output.txt") -> None:
    """Exports formatted HTML from a BeautifulSoup object to a text file."""
    formatted_html = soup.prettify()

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(formatted_html)
    print(f"Formatted HTML has been written to {file_name}")
