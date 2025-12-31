from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT_TIMEOUT = 15


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)

    def open(self, url: str):
        self.driver.get(url)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.send_keys(text)

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
