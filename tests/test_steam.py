from faker import Faker

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class text_not_empty:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        text = element.text.strip()
        return text if text else False


WAIT_TIMEOUT = 15
URL = 'https://store.steampowered.com/'
LOGIN_BUTTON_LOCATOR = (By.XPATH, "//*[@id='global_action_menu']//a[contains(@href,'login')]")
LOGIN_PAGE_LOCATOR = (By.XPATH, "//*[contains(@type,'password')]")
USERNAME_INPUT_LOCATOR = (By.XPATH, "(//form)[2]//input[contains(@type,'text')]")
PASSWORD_INPUT_LOCATOR = (By.XPATH, "//*[contains(@type,'password')]")
SUBMIT_BUTTON_LOCATOR = (By.XPATH, "(//button[@type='submit'])[2]")
SUBMIT_BUTTON_DIS_LOCATOR = (By.XPATH, "//button[@type='submit' and @disabled]")
SUBMIT_BUTTON_NOT_DIS_LOCATOR = (By.XPATH, "//button[@type='submit' and not(@disabled)]")
ERROR_TEXT_LOCATOR = (By.XPATH,
                      "(//button[@type='submit'])[2]/parent::div/following-sibling::"
                      "div[string-length(normalize-space(.)) > 1][1]")
EXPECTED_ERROR_TEXT = 'Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова.'
OPTIONS = webdriver.ChromeOptions()


@pytest.fixture
def driver():
    OPTIONS.add_argument('--window-size=1920,1080')
    OPTIONS.add_argument('--incognito')
    driver = webdriver.Chrome(options=OPTIONS)
    yield driver
    driver.quit()


def test_steam(driver):
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # 1. Открываем главную страницу
    driver.get(URL)
    wait.until(EC.visibility_of_element_located(LOGIN_BUTTON_LOCATOR))

    # 2. Нажимаем кнопку Войти
    login_button = wait.until(
        EC.element_to_be_clickable(LOGIN_BUTTON_LOCATOR))
    login_button.click()

    # 3. Ждём загрузку страницы с логином и паролем
    wait.until(
        EC.presence_of_element_located(LOGIN_PAGE_LOCATOR)
    )

    # 4. Вводим рандомный логин и пароль и нажимаем кнопку Войти
    faker = Faker()
    username = faker.user_name()
    password = faker.password()
    wait.until(EC.visibility_of_element_located(USERNAME_INPUT_LOCATOR)).send_keys(username)
    wait.until(EC.visibility_of_element_located(PASSWORD_INPUT_LOCATOR)).send_keys(password)
    submit_button = wait.until(
        EC.element_to_be_clickable(SUBMIT_BUTTON_LOCATOR))
    submit_button.click()

    # 5. Идёт загрузка, кнопка Войти становится неактивной
    wait.until(
        EC.presence_of_element_located(SUBMIT_BUTTON_DIS_LOCATOR)
    )

    # 6. Кнопка Войти снова активна
    wait.until(
        EC.presence_of_element_located(SUBMIT_BUTTON_NOT_DIS_LOCATOR)
    )

    # 7. Появляется сообщение об ошибке
    actual_error_text = wait.until(text_not_empty(ERROR_TEXT_LOCATOR))

    assert actual_error_text == EXPECTED_ERROR_TEXT, (
        f'Ожидаемый текст ошибки: {EXPECTED_ERROR_TEXT}, но получен: {actual_error_text}'
    )
