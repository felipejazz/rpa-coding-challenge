import random

from .browser import Browser
from selenium.webdriver.common.by import By

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)


# Criação de um logger
logger = logging.getLogger("RPA-LANDING-PAGE")


class LALandingPage:

    def __init__(self, browser: Browser):
        self.browser = browser

    def find_make_search_visible_button(self):
        try:
            search_input = self.browser.wait_for_element(by=By.XPATH, selector="/html/body/ps-header/header/div[2]/button")
            return search_input
        except TimeoutError:
            logger.error("Button to make search visible not found.")
            self.browser.take_screenshot("find_make_search_visible_error")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            self.browser.take_screenshot("find_make_search_visible_unexpected_error")

    def make_search_field_visible(self):
        search_box_button = self.find_make_search_visible_button()
        search_box_button.click()

    def find_search_input_field(self):
        try:
            search_field = self.browser.wait_for_element(by=By.XPATH, selector="/html/body/ps-header/header/div[2]/div[2]/form/label/input")
            return search_field
        except TimeoutError:
            logger.error("Search field not found.")
            self.browser.take_screenshot("find_search_input_field_error")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            self.browser.take_screenshot("find_search_input_field_unexpected_error")

    def find_search_submit_button(self):
        try:
            search_button = self.browser.wait_for_element(by=By.XPATH, selector="/html/body/ps-header/header/div[2]/div[2]/form/button")
            return search_button
        except TimeoutError:
            logger.error("Search button not found.")
            self.browser.take_screenshot("find_search_submit_button_timeout_error")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            self.browser.take_screenshot("find_search_submit_button_unexpected_error")

    def submit_search_form(self):
        search_button = self.find_search_submit_button()
        search_button.click()
        logger.info("Search button was pressed.")

    def search_for_keyword(self, keyword):
        try:
            self.make_search_field_visible()
            search_box = self.find_search_input_field()
            if not search_box:
                return
            for char in keyword:
                search_box.send_keys(char)
                self.browser.wait(seconds=random.uniform(0.1, 0.3))
            logger.info(f"Keyword '{keyword}' is in the search input field.")
        except TimeoutError:
            logger.error("Search input not found within the timeout period.")
            self.browser.take_screenshot("search_for_keyword_timeout_error.png")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            self.browser.take_screenshot("search_for_keyword_unexpected_error.png")

    def search(self, keyword):
        self.search_for_keyword(keyword)
        self.submit_search_form()

