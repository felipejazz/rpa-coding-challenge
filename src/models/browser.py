import logging
import math
import random
import time
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

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
logger = logging.getLogger("RPA-BROWSER")

class Browser:

    def __init__(self, headless=False, proxy=None, chrome_driver_path='/usr/bin/chromedriver', page_load_timeout=15) -> None:
        self.proxy = proxy
        self.headless = headless
        self.page_load_timeout = page_load_timeout
        self.driver = None
        self.chrome_driver_path = chrome_driver_path
        self.set_webdriver()

    def set_chrome_options(self):
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-web-security')
        options.add_argument("--start-maximized")
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
        return options

    def set_webdriver(self):
        options = self.set_chrome_options()
        service = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(self.page_load_timeout)

    @staticmethod
    def wait(seconds=None):
        if seconds is None:
            seconds = random.uniform(2, 5)
        logger.info(f"Waiting {math.ceil(seconds)} seconds for detectability purposes...")
        time.sleep(seconds)
        logger.info("Wait finished!")

    def navigate(self, url):
        self.wait()
        try:
            logger.info(f"Attempting to redirect to {url}.")
            t = time.time()
            self.driver.get(url)
            logger.info(f"Redirects successfully to {url}. Time taken: {time.time() - t} seconds.")
        except TimeoutException:
            self.driver.execute_script("window.stop();")
            logger.warning(f"Page load timeout exceeded. Stopped loading the page: {url}")

    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=timedelta(seconds=10)) -> webdriver.remote.webelement.WebElement:
        #@TODO TREAT NO SUCH ELEMENT EXCEPTION
        timeout_seconds = timeout.total_seconds()
        logger.info(f"Waiting for {selector} to become visible by {by}")
        try:
            element = None
            element = self.driver.find_element(by, selector)
            logger.info(f"{selector} is now visible.")
            return element
        except Exception as e:
            self.take_screenshot(f"{__name__}")
            logger.error(f"Timeout waiting for element: {selector}. Error: {e}")
            raise TimeoutError(f"Timeout waiting for element: {selector}")

    def wait_for_elements(self, selector, by=By.CSS_SELECTOR, timeout=timedelta(seconds=10)) -> webdriver.remote.webelement.WebElement:
        # @TODO TREAT NO SUCH ELEMENT EXCEPTION
        timeout_seconds = timeout.total_seconds()
        logger.info(f"Waiting for elements in {selector} become visible by {by}")
        try:
            element = None
            element = self.driver.find_elements(by, selector)
            logger.info(f"Elements in {selector} are now visibles.")
            return element
        except Exception as e:
            self.take_screenshot(f"{__name__}")
            logger.error(f"Timeout waiting for element: {selector}. Error: {e}")
            raise TimeoutError(f"Timeout waiting for element: {selector}")

    def take_screenshot(self, screenshot_name="screenshot"):
        self.driver.save_screenshot(f"{screenshot_name}.png")

    def driver_quit(self):
        if self.driver:
            self.driver.quit()

    def full_page_screenshot(self, url):
        self.driver.get(url)
        page_width = self.driver.execute_script('return document.body.scrollWidth')
        page_height = self.driver.execute_script('return document.body.scrollHeight')
        self.driver.set_window_size(page_width, page_height)
        self.driver.save_screenshot('screenshot.png')
        self.driver.quit()
