import random

from selenium.common import NoSuchElementException

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
            search_input = self.browser.wait_for_element(by=By.XPATH, selector="/html/body/ps-header/header/div["
                                                                               "2]/button")
            return search_input
        except TimeoutError:
            logger.error("Button to make search visible not found withing timeout period.")
            logger.error(f"Image of state of browser make search visible timeout error saved in "
                         f"find_make_search_visible_timeout_error.png")
            self.browser.take_screenshot("find_make_search_visible_timeout_error")
        except NoSuchElementException:
            logger.error("Button to make search visible does not exist.")
            logger.error(f"Image of state of browser during make search visible no such element error saved in "
                         f"find_search_submit_button_no_such_element_error.png")
            self.browser.take_screenshot("find_make_search_visible_button_no_such_element_error")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.error(f"Image of state of browser during make search visible unexpected error saved in "
                         f"find_search_submit_button_no_such_element_error.png")
            self.browser.take_screenshot("find_make_search_visible_unexpected_error")

    def make_search_field_visible(self):
        search_box_button = self.find_make_search_visible_button()
        self.browser.scroll_to_element(search_box_button)
        search_box_button.click()

    def find_search_input_field(self):
        try:
            search_field = self.browser.wait_for_element(by=By.XPATH, selector="/html/body/ps-header/header/div["
                                                                               "2]/div[2]/form/label/input")
            return search_field
        except TimeoutError:
            logger.error("Search field not found within timeout period.")
            logger.error(f"Image of state of browser during find search input field timeout error saved in "
                         f"find_search_input_field_timeout_error.png")
            self.browser.take_screenshot("find_search_input_field_timeout_error")
        except NoSuchElementException:
            logger.error("Search button element does not exist.")
            logger.error(f"Image of state of browser during find search input field no such element error saved in "
                         f"find_search_submit_button_no_such_element_error.png")
            self.browser.take_screenshot("find_search_submit_button_no_such_element_error")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.error(f"Image of state of browser during find search input field unexpected error saved in "
                         f"find_search_input_field_unexpected_error.png")
            self.browser.take_screenshot("find_search_input_field_unexpected_error")

    def find_search_submit_button(self):
        try:
            search_button = self.browser.wait_for_element(by=By.XPATH, selector="/html/body/ps-header/header/div[2]/div[2]/form/button")
            return search_button
        except TimeoutError:
            logger.error("Search button not found.")
            logger.error(f"Image of state of browser during find search submit button timeout error saved in "
                         f"find_search_submit_button_timeout_error.png")
            self.browser.take_screenshot("find_search_submit_button_timeout_error")
        except NoSuchElementException:
            logger.error("Search button element does not exist.")
            logger.error(f"Image of state of browser during find search submit button no such element error saved in "
                         f"find_search_submit_button_no_such_element_error.png")
            self.browser.take_screenshot("find_search_submit_button_no_such_element_error")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.error(f"Image of state of browser during find search submit button unexpected error saved in "
                         f"find_search_submit_button_unexpected_erro.png")
            self.browser.take_screenshot("find_search_submit_button_unexpected_error")

    def submit_search_form(self):
        search_button = self.find_search_submit_button()
        self.browser.scroll_to_element(search_button)
        search_button.click()
        logger.info("Search button was pressed.")

    def search_for_keyword(self, keyword):
        self.make_search_field_visible()
        search_box = self.find_search_input_field()
        self.browser.scroll_to_element(search_box)
        if not search_box:
            return
        for char in keyword:
            search_box.send_keys(char)
            self.browser.time_wait(seconds=random.uniform(0.1, 0.3), quiet=True)
        logger.info(f"Keyword '{keyword}' is in the search input field.")

    def search(self, keyword):
        self.search_for_keyword(keyword)
        self.submit_search_form()

