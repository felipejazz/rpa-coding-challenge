import logging
import math
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)


logger = logging.getLogger("RPA-BROWSER")


class Browser:

    def __init__(self, headless=False, proxy=None, chrome_driver_path='/usr/local/bin/chromedriver', page_load_timeout=10) -> None:
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

    def wait(self) -> WebDriverWait:
        return WebDriverWait(self.driver, 20)

    def time_wait(self, seconds=None, quiet=False):
        if seconds is None:
            seconds = random.uniform(2, 5)
        if not quiet:
            logger.info(f"Waiting {math.ceil(seconds)} seconds for detectability purposes...")
        time.sleep(seconds)
        if not quiet:
            logger.info("Wait finished!")

    def navigate(self, url):
        self.time_wait()
        try:
            logger.info(f"Attempting to redirect to {url}.")
            t = time.time()
            self.driver.get(url)
            logger.info(f"Redirects successfully to {url}. Time taken: {time.time() - t} seconds.")
        except TimeoutException:
            self.driver.execute_script("window.stop();")
            logger.warning(f"Page load timeout exceeded. Stopped loading the page: {url}")

    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=10) -> webdriver.remote.webelement.WebElement:
        logger.info(f"Waiting for {selector} to become visible by {by}")
        try:
            element = self.wait().until(
                EC.visibility_of_element_located((by, selector))
            )
            logger.info(f"{selector} is now visible.")
            return element

        except NoSuchElementException:
            raise NoSuchElementException(f"No such element waiting for element: {selector}")

        except TimeoutException:
            logger.error(f"Timeout waiting for element: {selector}")
            raise TimeoutError(f"Timeout waiting for element: {selector}")

    def retry_action(self, action, retries=3, delay=1):
        for attempt in range(retries):
            try:
                return action()
            except StaleElementReferenceException:
                logger.warning(f"Attempt {attempt + 1} failed due to StaleElementReferenceException. Retrying...")
                time.sleep(delay)
        logger.error("Failed to perform the action after several retries.")

    def wait_for_element_in_shadow(self, shadow_host_selector, element_selector, by=By.CSS_SELECTOR):
        try:
            logger.info(f"Waiting for shadow host {shadow_host_selector} to be present.")
            shadow_host = self.wait().until(
                EC.presence_of_element_located((by, shadow_host_selector))
            )
            logger.info(f"Shadow host {shadow_host_selector} is present.")

            logger.info(f"Accessing shadow root and looking for element {element_selector}.")
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', shadow_host)

            # Use shadow_root to find the desired element
            element = shadow_root.find_element(by, element_selector)
            self.wait().until(EC.visibility_of(element))
            logger.info(f"Element {element_selector} found in shadow root.")
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element in shadow DOM: {element_selector}")
            raise TimeoutError(f"Timeout waiting for element in shadow DOM: {element_selector}")
        except NoSuchElementException:
            logger.error(f"No such element in shadow DOM: {element_selector}")
            raise NoSuchElementException(f"No such element in shadow DOM: {element_selector}")

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    @staticmethod
    def click(selector, if_intercepted):
        try:
            selector.click()
        except ElementClickInterceptedException:
            if_intercepted()



    def wait_for_elements(self, selector, by=By.CSS_SELECTOR, timeout=10) -> list:
        logger.info(f"Waiting for elements in {selector} to become visible by {by}")
        try:
            elements = self.wait().until(
                EC.visibility_of_all_elements_located((by, selector))
            )
            logger.info(f"Elements in {selector} are now visible.")
            return elements
        except TimeoutException:
            logger.error(f"Timeout waiting for elements: {selector}")
            raise TimeoutError(f"Timeout waiting for elements: {selector}")
        except NoSuchElementException:
            raise NoSuchElementException(f"No such element waiting for elements: {selector}")

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
