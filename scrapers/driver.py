from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def install_web_driver(url: str) -> None:
    try:
        driver = Driver(uc=True)
        driver.get(url)
        wait = WebDriverWait(driver, 5)
        wait.until(EC.url_to_be(url))
        print("Page source obtained successfully.")
        return driver
    except Exception as e:
        raise Exception(f"Failed to install web driver: {e}")
