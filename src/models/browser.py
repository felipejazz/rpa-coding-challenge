import logging
import math
import random
import time
from datetime import timedelta

from selenium.webdriver.common.keys import Keys
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.chrome.options import Options

import requests

logger = logging.getLogger(__name__)


class Browser:

    def __init__(self, headless=False, proxy=None) -> None:
        self.browser = Selenium()
        self.proxy = proxy

#       @TODO PUT THIS IN CONFIG FILE
        self.options = Options()
        self.options.binary_location = "/usr/bin/google-chrome-stable"
        self.options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--remote-debugging-port=9222')

        if self.proxy:
            self.options.add_argument(f'--proxy-server={self.proxy}')

        if not headless:
            logger.info(f"Opening Browser without headless mode.")
            self.browser.open_available_browser(
                url=None,
                options=self.options,
                maximized=True)
            return

        logger.info(f"Opening Browser in headless mode.")
        self.options.add_argument('--headless')
        self.browser.open_available_browser(
            url=None,
            options=self.options,
            maximized=True)
        return

    @staticmethod
    def wait(seconds=None):
        if seconds is None:
            seconds = random.uniform(2, 5)
        logger.info(f"Waiting {math.ceil(seconds)} seconds due detectability purposes...")
        time.sleep(seconds)
        logger.info("Wait finished!")

    def navigate(self, url):
        logger.info(f"Attempting to redirect to {url}.")

        self.wait()
        try:
            self.browser.go_to(url=url)
            logger.info(f"Redirects successfully to {url}.")
            return
        except Exception as e:
            logger.error(f"Error during navigation attempt: {e}")
            raise TimeoutError(
                f"Failed to redirect to {url}\n{e}")

    def wait_for_element(self, selector, timeout=timedelta(seconds=10)):
        timeout_seconds = timeout.total_seconds()
        logger.info(f"Waiting for {selector} to become visible")
        try:
            self.browser.wait_until_element_is_visible(selector, timeout=timeout_seconds)
            element = self.browser.find_element(selector)
            logger.info(f"{selector} is now visible.")
            return element
        except Exception as e:
            self.take_screenshot(f"{__name__}")
            logger.error(f"Timeout waiting for element: {selector}. Error: {e}")
            raise TimeoutError(f"Timeout waiting for element: {selector}")

    def take_screenshot(self, screenshot_name="screenshot"):
        self.browser.capture_page_screenshot(f"{screenshot_name}.png")

    def find_make_search_visible_button(self):
        search_input = self.wait_for_element("css:[data-element='search-button']")
        if not search_input:
            logger.error("Button to make search visible not found.")
            self.take_screenshot(f"{__name__}")
            return None
        return search_input

    def make_search_field_visible(self):
        search_box_button = self.find_make_search_visible_button()
        self.browser.click_button(search_box_button)

    def find_search_input_field(self):
        search_field = self.wait_for_element("css:[data-element='search-form-input']")
        if not search_field:
            logger.error("Search field  not found.")
            self.take_screenshot(f"{__name__}")
            return None
        return search_field

    def find_search_submit_button(self):
        search_button = self.wait_for_element("css:[data-element='search-submit-button']")
        if not search_button:
            logger.error("Search button not found.")
            self.take_screenshot(f"{__name__}")
            return None
        return search_button

    def submit_search_form(self):
        search_button = self.find_search_submit_button()
        self.browser.click_button(search_button)
        logger.info("Search button were pressed.")

    def search_for_keyword(self, keyword):
        try:
            self.make_search_field_visible()
            search_box = self.find_search_input_field()
            if not search_box:
                logger.error("Search box not found, cannot proceed with search.")
                self.take_screenshot(f"{__name__}")
                return
            for char in keyword:
                search_box.send_keys(char)
                self.wait(seconds=random.uniform(0.1, 0.3))
            # search_box.send_keys(Keys.ENTER)
            logger.info(f"Keyword '{keyword}' is in the search input field.")
        except TimeoutError:
            logger.error("Search input not found within the timeout period.")
            self.browser.capture_page_screenshot("screenshot.png")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            self.browser.capture_page_screenshot("screenshot.png")

    def search(self, keyword):
        self.search_for_keyword(keyword)
        self.submit_search_form()
