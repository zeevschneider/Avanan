from tests.support.driver import WebDriver
from selenium.webdriver.support.ui import Select


"""
    wallashops.co.il related
"""

class WallaShops:

    _selectors = {"search_box": '.aa-input-search',
                  "search_button": '.magnifier',
                  "go_to_cart": 'a[href="/cart"] div div.fright',
                  "login_button": 'span.action-inner',
                  "product_title": 'span#productTitle',
                  "add_to_cart_button": '#addToCartBtn',
                  "product_price": '#DealPrice',
                  "continue_shopping": "#CartPopupContinueShoppingText",
                  "empty_cart": ".removecartlink"
                  }

    def __init__(self, driver=WebDriver()):
        """
        :param driver: receives an Web driver object
        """
        self.driver = driver



    def buy_products(self, search_string, total_sum=None):
        """
        Logic of buying products
        :param search_string: to search in the site
        :param total_sum: the budget for shopping
        :return: list of bought items
        """
        if total_sum:
            self.budget = total_sum
        self.driver.find_element_by_css_selector(self._selectors["search_box"]).send_keys(search_string)
        self.driver.find_element_by_css_selector(self._selectors["search_button"]).click()
        time.sleep(5)
        # finds products on a page
        product_pages = self.driver.find_elements_by_xpath('//div[@id="currentPrice"]/../../../../a[@href]')

        items = self._get_shopping_list(product_pages)
        for item in items:
            self.driver.get(item)
            self._purchase(item)

        self._write_report(items)

    def _purchase(self, url):
        """
        Perches the item
        :param url:
        :return:
        """
        price = self._get_price()
        if price > 0:
            if self.purchased_sum + price < self.budget:
                if self.driver.find_elements_by_css_selector('.variation'):
                    ddelement= Select(self.driver.find_element_by_css_selector('.variation'))
                    ddelement.select_by_index(1)
                self.driver.find_element_by_css_selector(self._selectors["add_to_cart_button"]).click()
                time.sleep(3)
                self.driver.find_element_by_css_selector(self._selectors["continue_shopping"]).click()
                self.purchased_sum += price

    def _get_price(self):
        """
        finds the price on page
        :return: returns float
        """
        try:
            price = self.driver.find_element_by_css_selector(self._selectors["product_price"]).text

        except Exception:
            print("Price was not found for this item.")
            return

        return float(price)

    def _get_shopping_list(self, pages):
        """
        Returns a list of urls of items
        :param pages:
        :return:
        """
        scraper = Scraper()
        scraper.set_selector(self._selectors["product_price"])
        urls_to_prices = {}
        # creates a dict url_to_product: price
        for page in pages:
            # gets url to product page
            k = page.get_attribute("href")
            # scrapes for product price
            v = scraper.request_and_scrape(page)
            urls_to_prices[k] = float(v)

        shopping_list = self._simulate_purchase(urls_to_prices)
        return shopping_list

    def _simulate_purchase(self, purchase_dict):
        """
        Simulates the purchase and actually reduces the shopping list in
        case it expected to go over the budget limit
        :param purchase_dict:
        :return: a list of links to products
        """
        simulate_sum = 0
        temp_list = []
        items_list = []

        for k, v in purchase_dict.items():
            newt = (v, k)
            temp_list.append(newt)
        temp_list = sorted(temp_list)

        for index, item in enumerate(temp_list):
            simulate_sum += item[0]
            if simulate_sum < self.budget:
                items_list.append(item[1])
            else:
                return items_list
        return items_list

    def _write_report(self, item_list):
        file_name = "mission_products/purchase_azrieli.txt"
        try:
            os.remove(file_name)
        except OSError:
            pass
        with open(file_name, 'a') as f:
            f.write(f'Total shopping cost is {self.purchased_sum}\n\n')
            f.write("The following items were purchased:\n")
            for item in item_list:
                f.write("============================\n")
                f.write(f'{item}\n\n')


    def teardown(self):
        """
        Removes items from the cart
        :return:
        """
        self.driver.find_element_by_css_selector(self._selectors["go_to_cart"]).click()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        self.driver.find_element_by_css_selector(self._selectors["empty_cart"]).click()
        obj = self.driver.switch_to.alert
        obj.accept()
        self.driver.quit()
