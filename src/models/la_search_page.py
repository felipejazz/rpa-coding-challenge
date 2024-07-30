import logging
from selenium.webdriver.common.by import By

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("RPA-SEARCH-PAGE")


class LASearchPage:
    def __init__(self, la_landing_page):
        self.browser = la_landing_page.browser

    def get_news(self):
        try:
            ul_element = self.browser.wait_for_element(by=By.XPATH, selector="//ul[contains(@class, 'search-results')]")
            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
            for index, li in enumerate(li_elements):
                title_element = li.find_element(By.XPATH, ".//h3[@class='promo-title']//a")
                description_element = li.find_element(By.XPATH, ".//p[@class='promo-description']")
                date_element = li.find_element(By.XPATH, ".//p[@class='promo-timestamp']")

                title = title_element.text
                description = description_element.text
                date = date_element.text

                logger.info(f"Notícia {index + 1}: {title}")
                print(f"Notícia {index + 1}:")
                print(f"Título: {title}")
                print(f"Descrição: {description}")
                print(f"Data: {date}")
                print("-" * 30)
        except Exception as e:
            logger.error(f"An error occurred while getting news: {e}")
            self.browser.take_screenshot("get_news_error")

    def find_sort_button(self):
        try:
            sort_by_relevance_button = self.browser.wait_for_element(by=By.XPATH,
                                                                     selector="//select[@aria-label='Sort by']")
            sort_by_relevance_button.click()
            select_newest_relevance = self.browser.wait_for_element(by=By.XPATH, selector="//option[text()='Newest']")
            select_newest_relevance.click()
            logger.info("Search news sorted descending.")
        except Exception as e:
            logger.error(f"An error occurred while sorting news: {e}")
            self.browser.take_screenshot("find_sort_button_error")

    def sort_news(self, descending=True):
        if descending:
            self.find_sort_button()
