import logging

from tests.support.driver import WebDriver
from collections import namedtuple
import re
import time

"""
    wallashops.co.il related  - all purchases are as guest 
"""
# TODO - add logic for purchase as registered user


class WallaShops:

    products_css = '.l-col-md-3.l-col-6.js-prod-col.prod-col.type-grid.b-product-grid-item'
    _selectors = {"search_box": '.search-field',
                  "search_button": '.c-search-form-submit',
                  "go_to_cart": '.b-header-minicart-title',
                  "products_link": f'{products_css} a',
                  "add_to_wish_list": f'{products_css} a.wish-list-tile',
                  "results_header": 'h1.t-category-title ',
                  "warning_message": 'p.b-empty-plp-title',
                  "add_to_cart_button": f'{products_css} button.js-add-to-cart-tile',
                  "product_description": f'{products_css} div.b-product-list-title div.b-product-link-wrapper a.b-product-link',
                  "product_price": f'{products_css} .value',
                  "price_in_cart": '.b-cart-product-details-price div.b-product-price-regular span.value',
                  "description_in_cart": '.b-cart-product-details-header a',
                  "proceed_to_checkout": '.f-checkout-btn',
                  "checkout": 'a[href="https://www.wallashops.co.il/Checkout"]',
                  "checkout_description": 'div.b-order-products-shipping div.b-line-item-name',
                  "checkout_total_price": 'div.card-body.order-total-summary ul.s-totals-list li',
                  "grand_total": '.t-grand-total',
                  "pick_up_first_name_field": 'input[name="dwfrm_supplierpickupinstore_firstName"]',
                  "pick_up_last_name_field": 'input[name="dwfrm_supplierpickupinstore_lastName"]',
                  "pick_up_phone": 'input[name="dwfrm_supplierpickupinstore_phone"]',
                  "pick_up_email": 'input[name="dwfrm_supplierpickupinstore_email"]',
                  "pick_up_id": 'input[name="dwfrm_supplierpickupinstore_customerid"]',
                  "submit_pick_up": 'div.shipping-section div.row button.submit-shipping',
                  }

    def __init__(self, driver=WebDriver()):
        """
        :param driver: receives an Web driver object
        """
        self.driver = driver

    def select_item(self, search_string):
        """
        Searches and selects the first item it finds
        :param search_string: item description
        """

        self.search_item(search_string)
        self.click_search()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector(self._selectors["results_header"])
        self._select_first_item()

    def search_item(self, item):
        """
        Searches an item
        :param item: item description
        :return:
        """
        self.driver.find_element_by_css_selector(self._selectors["search_box"]).send_keys(item)

    def click_search(self):
        """
        Clicks search
        :return:
        """
        self.driver.find_element_by_css_selector(self._selectors["search_button"]).click()

    def _select_first_item(self):
        """
        Selects the first item in search result
        :return:
        """
        products = self.driver.find_elements_by_css_selector(self._selectors["products_link"])
        products[1].click()

    def add_first_to_wish_list(self, search_string):
        """
        Adds first item in search results to wish list
        :param search_string: item description
        :return:
        """
        self._wait_for_results(search_string)
        products = self.driver.find_elements_by_css_selector(self._selectors["add_to_wish_list"])
        # some popups with promotions appear
        self.driver.execute_script("arguments[0].click();", products[1])

    def add_first_to_cart(self, search_string):
        """
        Adds first item in search results to cart
        :param search_string: item description
        :return:
        """
        self._wait_for_results(search_string)
        products = self.driver.find_elements_by_css_selector(self._selectors["add_to_cart_button"])
        self.driver.execute_script("arguments[0].click();", products[0])

    def add_first_to_cart_to_verify(self, search_string):
        """
        Adds first item in search results to cart and returns data in order to verify
        :param search_string: item description
        :return: tuple - description and price of item
        """
        ProductData = namedtuple("ProductData", "description price")
        self._wait_for_results(search_string)
        add_to_cart = self.driver.find_elements_by_css_selector(self._selectors["add_to_cart_button"])
        descriptions = self.driver.find_elements_by_css_selector(self._selectors["product_description"])
        prices = self.driver.find_elements_by_css_selector(self._selectors["product_price"])

        description = descriptions[0].get_attribute("data-full-text")
        price = prices[0].text

        self.driver.execute_script("arguments[0].click();", add_to_cart[0])
        self._close_cart_modal_win()
        return ProductData(description, price)

    def go_to_cart_and_verify_single(self, product_details: tuple):
        """
        Verifies added item in cart
        :param product_details: tuple - description and price of added item
        :return:
        """
        self._close_cart_modal_win()
        self.driver.find_elements_by_css_selector(self._selectors["go_to_cart"])[0].click()
        cart_items = self.driver.find_elements_by_css_selector(self._selectors["description_in_cart"])
        if len(cart_items) > 1:
            raise 'Multiple items in cart - this method is for single item only.'
        cart_description = cart_items[0].text
        cart_price_with_cur = self.driver.find_elements_by_css_selector(self._selectors["price_in_cart"])[0].text
        cart_price = self._get_price_from_text(cart_price_with_cur)
        orig_price = self._get_price_from_text(product_details[1])

        if (product_details[0], orig_price) != (cart_description, cart_price):
            raise 'Items do not match'

    def proceed_to_checkout_verify_and_pick(self, purchase_details: tuple, as_guest=True):
        """
        Proceed to checkout with pickup.
        Verifies purchase against item in cart
        :param purchase_details:
        :param as_guest:
        :return:
        """
        self.driver.find_elements_by_css_selector(self._selectors["proceed_to_checkout"])[0].click()
        if as_guest:
            self.driver.find_elements_by_css_selector(self._selectors["checkout"])[0].click()

        self._verify_purchase(purchase_details)

        # add buyers data
        self.driver.find_element_by_css_selector(self._selectors["pick_up_first_name_field"]).send_keys("סתם")
        self.driver.find_element_by_css_selector(self._selectors["pick_up_last_name_field"]).send_keys("אחד")
        self.driver.find_element_by_css_selector(self._selectors["pick_up_phone"]).send_keys("0542222222")
        self.driver.find_element_by_css_selector(self._selectors["pick_up_email"]).send_keys("stam1@gmail.com")
        self.driver.find_element_by_css_selector(self._selectors["pick_up_id"]).send_keys("011429008")
        self.driver.find_element_by_css_selector(self._selectors["submit_pick_up"]).click()

    def _wait_for_results(self, search_string):
        """
        Waits on result of a search. Raises exception if item not found
        :param search_string: item description
        :return:
        """
        self.search_item(search_string)
        self.click_search()
        self.driver.implicitly_wait(5)
        try:
            element = self.driver.find_element_by_css_selector(self._selectors["warning_message"])
            if element.is_displayed():
                logging.warning("Item not found")
                raise Exception("Test failed  - Item not found")

        except Exception:
            pass

        try:
            element = self.driver.find_element_by_css_selector(self._selectors["results_header"])
            if element.is_displayed():
                logging.warning("Items found")

        except Exception:
            raise "Search process did not succeed"

    def _verify_purchase(self, purchase_details: tuple, is_pick_up=True):
        """
        Verifies item against the data in cart (description and price) is the same before checkout
        :param purchase_details: tuple - cart data
        :param is_pick_up: is item for pickup
        :return:
        """
        checkout_description = self.driver.find_elements_by_css_selector(self._selectors["checkout_description"])[0].text
        checkout_price_str = self.driver.find_elements_by_css_selector(self._selectors["checkout_total_price"])[0].text

        checkout_price = self._get_price_from_text(checkout_price_str)
        cart_price = self._get_price_from_text(purchase_details[1])
        if (purchase_details[0], cart_price) != (checkout_description, cart_price):
            raise Exception('The item is not the same as in the cart.')

        if is_pick_up:
            self.driver.find_element_by_xpath('//input[@value="SupplierInStorePickup"]/../label').click()
            time.sleep(3)
            grand_total_str = self.driver.find_elements_by_css_selector(self._selectors["grand_total"])[0].text
            grand_total = self._get_price_from_text(grand_total_str)
            if grand_total != checkout_price:
                raise Exception('Total and purchase prices differ.')

        # TODO - check logic including shipment

    def _get_price_from_text(self, price_with_currency):
        """
        Gets the numeric value from the price - e.g 199ש"ח will return 199
        :param price_with_currency: e.g 199ש"ח
        :return:
        """
        price = re.findall(r'(\d+)', price_with_currency)
        return price

    def _close_cart_modal_win(self):
        """
        Close the modal window when adding to cart
        :return:
        """
        windows = self.driver.find_elements_by_css_selector('div.s-page-wrapper button.modal-close span')
        if windows[0].is_displayed():
            windows[0].click()

    def teardown(self, driver):
        """
        Quits the driver
        # TODO - add steps for proper teardown - remove items from favorites, cart etc.
        :return:
        """
        self.driver.quit()
