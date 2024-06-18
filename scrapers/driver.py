from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def install_web_driver(url) -> None:
    driver = Driver(uc=True)
    driver.get(url)
    wait = WebDriverWait(driver, 5)
    driver.get(url)
    wait.until(EC.url_to_be(url))
    print("Page source obtained successfully.")
    return driver
