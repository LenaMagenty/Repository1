from selenium import webdriver


class DriverSingleton:
    _driver = None

    @classmethod
    def get_driver(cls) -> webdriver.Chrome:
        if cls._driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--incognito')
            cls._driver = webdriver.Chrome(options=options)
            cls._driver.set_page_load_timeout(15)
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None
