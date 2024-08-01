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

    def __init__(self, headless=False, proxy=None, chrome_driver_path='chromedriver', page_load_timeout=20) -> None:
        self.proxy = proxy
        self.headless = headless
        self.page_load_timeout = page_load_timeout
        self.driver = None
        self.chrome_driver_path = chrome_driver_path
        self.window_size = (1920, 1080)
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
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-port=9222')
        # options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(f'--window-size={self.window_size[0]},{self.window_size[1]}')
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
        return options

    def set_webdriver(self):
        options = self.set_chrome_options()
        service = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(self.page_load_timeout)

    def wait(self, timeout=10) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=timeout)

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

    def click(self, selector):
        self.driver.execute_script("arguments[0].click();", selector)

    def wait_for_element(self, selector, by=By.CSS_SELECTOR,
                         selector_name=None) -> webdriver.remote.webelement.WebElement:
        name_to_log = selector_name if selector_name else selector
        logger.info(f"Waiting for {name_to_log} to become visible by {by}")
        try:
            element = self.wait().until(
                EC.visibility_of_element_located((by, selector))
            )
            logger.info(f"{name_to_log} is now visible.")
            return element
        except NoSuchElementException:
            raise NoSuchElementException(f"No such element waiting for element: {name_to_log}")
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {name_to_log}")
            raise TimeoutError(f"Timeout waiting for element: {name_to_log}")

    def wait_for_element_be_clickable(self, selector, by=By.CSS_SELECTOR, selector_name=None):
        name_to_log = selector_name if selector_name else selector
        logger.info(f"Waiting for {name_to_log} to become visible by {by}")
        try:
            element = self.wait().until(
                EC.visibility_of_element_located((by, selector))
            )
            logger.info(f"{name_to_log} is now visible.")
            self.scroll_to_element(element)
            # Ensure the element is clickable
            logger.info(f"Waiting for {name_to_log} to become clickable")
            element = self.wait().until(
                EC.element_to_be_clickable((by, selector))
            )
            logger.info(f"{name_to_log} is now clickable.")
            return element
        except NoSuchElementException:
            raise NoSuchElementException(f"No such element waiting for element: {name_to_log}")
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {name_to_log}")
            raise TimeoutError(f"Timeout waiting for element: {name_to_log}")
        except ElementClickInterceptedException:
            logger.error(f"Element click intercepted: {name_to_log}")
            raise ElementClickInterceptedException(f"Element click intercepted: {name_to_log}")

    def retry_action(self, action, retries=3, delay=1):
        for attempt in range(retries):
            try:
                return action()
            except StaleElementReferenceException:
                logger.warning(f"Attempt {attempt + 1} failed due to StaleElementReferenceException. Retrying...")
                time.sleep(delay)
        logger.error("Failed to perform the action after several retries.")

    def wait_for_element_in_shadow(self, shadow_host_selector, element_selector, by=By.CSS_SELECTOR, shadow_selector_name=None, element_selector_name=None):
        name_to_log_shadow = shadow_selector_name if shadow_selector_name else shadow_host_selector
        name_to_log_shadow_button = element_selector_name if element_selector_name else element_selector
        try:
            logger.info(f"Waiting for shadow host {name_to_log_shadow} to be present.")
            shadow_host = self.wait(timeout=2).until(
                EC.presence_of_element_located((by, shadow_host_selector))
            )

            logger.info(f"Shadow host {name_to_log_shadow} is present.")

            logger.info(f"Accessing shadow root and looking for element {name_to_log_shadow}.")
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', shadow_host)

            element = shadow_root.find_element(by, element_selector)
            self.wait().until(EC.visibility_of(element))
            logger.info(f"Element {name_to_log_shadow_button} found in shadow root.")
            return element
        except TimeoutException:
            logger.info(f"Timeout waiting for element in shadow DOM: {name_to_log_shadow_button}")
            return None

        except NoSuchElementException:
            logger.error(f"No such element in shadow DOM: {name_to_log_shadow_button}")
            raise NoSuchElementException(f"No such element in shadow DOM: {name_to_log_shadow_button}")

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)


    def wait_for_elements(self, selector, by=By.CSS_SELECTOR, selector_name=None) -> list:
        logger.info(f"Waiting for elements in {selector if selector_name is None else selector_name} to become visible by {by}")
        name_to_log = selector_name if selector_name else selector

        try:
            elements = self.wait().until(
                EC.visibility_of_all_elements_located((by, selector))
            )
            logger.info(f"Elements in {name_to_log} are now visible.")
            return elements
        except TimeoutException:
            logger.error(f"Timeout waiting for elements: {name_to_log}")
            raise TimeoutError(f"Timeout waiting for elements: {name_to_log}")
        except NoSuchElementException:
            raise NoSuchElementException(f"No such element waiting for elements: {name_to_log}")

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
