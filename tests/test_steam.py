import random
import string

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def test_steam(driver):
    wait = WebDriverWait(driver, 15)

    # 1. Открываем главную страницу
    driver.get('https://store.steampowered.com/')
    wait.until(EC.title_contains('Steam'))

    # 2. Нажимаем кнопку Войти
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='global_action_menu']//a[contains(@href,'login')]")))
    login_button.click()

    # 3. Ждём загрузку страницы с логином и паролем
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@type,'password')]"))
    )

    # 4. Вводим рандомный логин и пароль и нажимаем кнопку Войти
    username = random_string()
    password = random_string()
    driver.find_element(By.XPATH, "(//form)[2]//input[contains(@type,'text')]").send_keys(username)
    driver.find_element(By.XPATH, "//*[contains(@type,'password')]").send_keys(password)
    submit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//button[@type='submit'])[2]")))
    submit_button.click()

    # 5. Идёт загрузка, кнопка Войти становится неактивной
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and @disabled]"))
    )

    # 6. Кнопка Войти снова активна
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and not(@disabled)]"))
    )

    # 7. Появляется сообщение об ошибке
    error_text = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']/parent::div/following-sibling::div[1]"))
    )
    assert error_text.is_displayed()