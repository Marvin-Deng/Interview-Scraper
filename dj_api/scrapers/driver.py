import undetected_chromedriver as uc
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def install_web_driver(url) -> None:
    driver = Driver(uc=True)
    driver.get(url)
    wait = WebDriverWait(driver, 5)
    driver.get(url)
    wait.until(EC.url_to_be(url))
    print("Page source obtained successfully.")
    return driver

# def install_web_driver(self) -> None:
#     """Installs and initializes the web driver."""
#     try:
#         # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
#         options = uc.ChromeOptions()
#         # options.add_argument("--headless")
#         options.add_argument(f"user-agent={my_user_agent}")

#         self.driver = uc.Chrome(options=options)

#         self.driver.get(self.url)
#         wait = WebDriverWait(self.driver, 5)
#         self.driver.get(self.url)
#         wait.until(EC.url_to_be(self.url))
#         print("Page source obtained successfully.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
