from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import StaleElementReferenceException


class SearchResultsPage(BasePage):
    SORT_TRIGGER = (By.XPATH, "//*[@id='sort_by_trigger']")
    PRICE_DESC_OPTION = (By.XPATH, "//*[@id='Price_DESC']")
    SORT_VALUE_INPUT = (By.XPATH, "//*[@id='sort_by']")
    RESULTS_CONTAINER = (By.XPATH, "//*[@id='search_resultsRows']")
    RESULT_ROWS = (By.XPATH, "//*[@id='search_resultsRows']//a[contains(@class,'search_result_row')]")
    TITLES_RESULT_TEMPLATE = "(//*[@id='search_resultsRows']//span[@class='title'])[position() <= {n}]"

    def wait_loaded(self, n: int = 1):
        self.visible(self.RESULTS_CONTAINER)
        self.wait.until(lambda d: len(d.find_elements(*self.RESULT_ROWS)) >= n)
        return self

    def sort_by_highest_price(self):
        self.wait_loaded()

        self.click(self.SORT_TRIGGER)

        self.click(self.PRICE_DESC_OPTION)

        self.wait.until(
            lambda d: d.find_element(*self.SORT_VALUE_INPUT).get_attribute('value') == 'Price_DESC'
        )

        return self

    def get_first_n_titles(self, n: int):
        titles_result = self.TITLES_RESULT_TEMPLATE.format(n=n)

        for _ in range(5):
            try:
                self.wait.until(
                    lambda d: len(d.find_elements(By.XPATH, titles_result)) >= n
                )

                titles = [
                    e.text.strip()
                    for e in self.driver.find_elements(By.XPATH, titles_result)
                ]

                if len(titles) == n and all(titles):
                    return titles

            except StaleElementReferenceException:
                continue

        raise AssertionError(f'Не удалось получить {n} игр')
