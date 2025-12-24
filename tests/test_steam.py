from faker import Faker

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DocumentReadyStateComplete:
    def __call__(self, driver):
        state = driver.execute_script("return document.readyState")
        return state == 'complete'


WAIT_TIMEOUT = 15
URL = 'https://store.steampowered.com/'
LOGIN_BUTTON_LOCATOR = (By.XPATH, "//*[@id='global_action_menu']//a[contains(@href,'login')]")
LOGIN_PAGE_LOCATOR = (By.XPATH, "//*[contains(@type,'password')]")
USERNAME_INPUT_LOCATOR = (By.XPATH, "(//form)[2]//input[contains(@type,'text')]")
PASSWORD_INPUT_LOCATOR = (By.XPATH, "//*[contains(@type,'password')]")
SUBMIT_BUTTON_LOCATOR = (By.XPATH, "(//button[@type='submit'])[2]")
SUBMIT_BUTTON_DIS_LOCATOR = (By.XPATH, "//button[@type='submit' and @disabled]")
SUBMIT_BUTTON_NOT_DIS_LOCATOR = (By.XPATH, "//button[@type='submit' and not(@disabled)]")
ERROR_TEXT_LOCATOR = (By.XPATH, "//div[contains(@class, '_1W_6HXiG4JJ0By1qN_0fGZ')]")
EXPECTED_ERROR_TEXT = 'Please check your password and account name and try again.'


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_steam(driver):
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # 1. Открываем главную страницу
    driver.get(URL)
    WebDriverWait(driver, WAIT_TIMEOUT).until(DocumentReadyStateComplete())

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
    driver.find_element(*USERNAME_INPUT_LOCATOR).send_keys(username)
    driver.find_element(*PASSWORD_INPUT_LOCATOR).send_keys(password)
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
    error_text = wait.until(EC.presence_of_element_located(ERROR_TEXT_LOCATOR))

    actual_error_text = wait.until(lambda d: (
            error_text.get_attribute('textContent') or ''
    ).strip())

    assert actual_error_text == EXPECTED_ERROR_TEXT

    assert actual_error_text == EXPECTED_ERROR_TEXT, (
        f'Ожидаемый текст ошибки: {EXPECTED_ERROR_TEXT}, но получен: {actual_error_text}'
    )
