from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage

URL = 'https://store.steampowered.com/'


class HomePage(BasePage):
    LOGIN_BUTTON = (By.XPATH, "//*[@id='global_action_menu']//a[contains(@href,'login')]")
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder,'Поиск') or contains(@placeholder,'Search')]")
    SEARCH_BUTTON = (By.XPATH, "//form[contains(@role,'search')]//button[@type='submit']")

    def open_home(self):
        self.open(URL)
        self.visible(self.LOGIN_BUTTON)
        return self

    def search(self, game_name: str):
        self.type(self.SEARCH_INPUT, game_name)
        self.click(self.SEARCH_BUTTON)
        return SearchResultsPage(self.driver)
