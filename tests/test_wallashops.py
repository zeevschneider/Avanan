import pytest
import logging
from tests.support.driver import WebDriver
from tests.support.walla_shops.walla_shops import WallaShops
import time


"""
    A function scoped fixture(runs for every test).
    Initialized a WebDriver and browses into wallashops site
    At end tears down the driver 
"""
@pytest.fixture(scope='function')
def setup_and_teardown():
    logging.info("Getting WebDriver and going to wallashops.")
    driver = WebDriver("chrome").get_driver()
    driver.maximize_window()
    driver.get('https://www.wallashops.co.il')
    if driver.find_element_by_css_selector('#pe_confirm_optin_1'):
        driver.find_element_by_class_name('pe-optin-1_closeWrapper').click()

    yield driver
    walla = WallaShops(driver)
    walla.teardown(driver)


# Searches for a product, adds to favorites and verifies it is added (numerically)
def test_add_to_favorites(setup_and_teardown):
    walla = WallaShops(setup_and_teardown)
    walla.add_first_to_wish_list("כסא")
    quantity = setup_and_teardown.find_element_by_css_selector('.b-header-saved-products-quantity').text
    assert quantity == '1'


# Searches for a product, adds to cart and verifies it is added (numerically)
def test_add_to_cart(setup_and_teardown):
    walla = WallaShops(setup_and_teardown)
    walla.add_first_to_cart("כסא")
    cart_count = setup_and_teardown.find_element_by_css_selector('.b-header-minicart-quantity.js-minicart-quantity').text
    assert cart_count == '1'


# Searches for a product, adds to cart and nearly completes purchase process (verifies in the payment page)
def test_add_to_cart_and_purchase(setup_and_teardown):
    walla = WallaShops(setup_and_teardown)
    (description, price) = walla.add_first_to_cart_to_verify("כסא")
    walla.go_to_cart_and_verify_single((description, price))
    walla.proceed_to_checkout_verify_and_pick((description, price))
    time.sleep(3)
    assert setup_and_teardown.current_url == "https://www.wallashops.co.il/Checkout?stage=payment#payment"