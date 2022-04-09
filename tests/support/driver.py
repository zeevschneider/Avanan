from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

"""
    Initializes a webdriver : Firefox or Chrome
"""


class WebDriver(ChromeDriverManager, GeckoDriverManager):
    def __init__(self, driver_name="chrome"):
        """

        :param driver_name:
        """
        super(WebDriver, self).__init__()
        self.name = driver_name
        self.driver = None

    def get_driver(self):
        """

        :return: webdriver
        """
        if self.name == "firefox".lower():
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

        # Todo - add initialization parameter and headless support

        return self.driver

