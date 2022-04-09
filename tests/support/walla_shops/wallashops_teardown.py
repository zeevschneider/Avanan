import logging
from tests.support.driver import WebDriver


def tear_down(driver):
    driver.clean_favorites()
    driver.clean_cart()

def clean_favorites():
    True

def clean_cart():
    True