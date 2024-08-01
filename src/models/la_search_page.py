import logging
import os

import requests
from openpyxl import Workbook
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import re
from src.utils.count_words import count_words

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
        self.search_phrases = ["search phrase1", "search phrase2"]

    def get_news(self):
        news_data = []

        subscription_closed = False
        try:

            ul_element = self.browser.wait_for_element(by=By.XPATH, selector="//ul[contains(@class, 'search-results')]", selector_name="News Results")
            self.browser.scroll_to_element(ul_element)
            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
            for index, li in enumerate(li_elements):
                if not subscription_closed:
                    subscription_closed = self.check_if_subscribe_popup_is_open()
                self.browser.scroll_to_element(li)
                title_element = li.find_element(By.XPATH, ".//h3[@class='promo-title']//a")
                description_element = li.find_element(By.XPATH, ".//p[@class='promo-description']")
                date_element = li.find_element(By.XPATH, ".//p[@class='promo-timestamp']")

                try:
                    picture_element = li.find_element(By.XPATH, ".//div[contains(@class, 'promo-media')]//picture")
                except NoSuchElementException:
                    picture_element = None

                image_url = None
                if picture_element:
                    image_url = self.get_image_url_from_picture(picture_element)

                picture_filename = None
                if image_url:
                    picture_filename = f"{index + 1}.jpg"
                    self.download_image(image_url, picture_filename)

                title = title_element.text
                description = description_element.text
                date = date_element.text
                title_word_count = count_words(title)
                description_word_count = count_words(description)

                words_count = title_word_count + description_word_count
                has_money = bool(re.search(r'\$\d+(\.\d+)?|\d+ dollars|\d+ USD', title + description, re.IGNORECASE))

                news_data.append({
                    "title": title,
                    "date": date,
                    "description": description,
                    "picture_filename": picture_filename,
                    "words-counts_title-description": words_count,
                    "has_money": has_money
                })

                logger.info(f"Notícia {index + 1}: {title}")
                print(f"News: {index + 1}:")
                print(f"Date: {date}")
                print(f"Title: {title}")
                print(f"Title Word Count: {title_word_count}")
                print(f"Image: {picture_filename}")
                print(f"Description: {description}")
                print(f"Description Word Count: {description_word_count}")
                print(f"Total Word Counts: {words_count}")
                print("-" * 30)

        except Exception as e:
            self.browser.take_screenshot("get_news_error")
            logger.error(f"An error occurred while getting news: {e}", exc_info=True)
            logger.error(f"Image of state of browser during get news error saved in get_new_error.png", exc_info=True)

        return news_data

    def get_image_url_from_picture(self, picture_element):
        try:
            img_element = picture_element.find_element(By.TAG_NAME, 'img')
            image_url = img_element.get_attribute('src')
            return image_url
        except NoSuchElementException:
            logger.error("Image element not found within the <picture> tag.", exc_info=True)
            return None

    def check_if_subscribe_popup_is_open(self, close=True):
        def action():
            shadow_host_selector = 'modality-custom-element'
            popup_selector = '.met-flyout-close'

            try:
                close_modal = self.browser.wait_for_element_in_shadow(shadow_host_selector, popup_selector, shadow_selector_name="Subsription PopUp", element_selector_name="Subscription Close Button")
                if close_modal:
                    if close:
                        close_modal.click()
                        logger.info(f"Subscription modal was closed!")
                        return True
            except NoSuchElementException:
                logger.info("Modal not found.")
                return False

        try:
            return self.browser.retry_action(action, retries=3, delay=2)
        except Exception as e:
            logger.error(f"An error occurred while handling the subscription modal: {e}", exc_info=True)
            self.browser.take_screenshot("check_if_subscribe_popup_is_open_error")
            logger.error(
                f"Image of state of browser during check_if_subscribe_popup_is_open error saved in check_if_subscribe_popup_is_open_error.png",
                exc_info=True)
            return False

    def find_sort_button(self):
        try:
            sort_by_relevance_button = self.browser.wait_for_element(by=By.CSS_SELECTOR,
                                                                     selector="body > div.page-content > ps-search-results-module > form > div.search-results-module-ajax > ps-search-filters > div > main > div.search-results-module-results-header > div.search-results-module-sorts > div > label > select", selector_name="Sort By Button")

            sort_by_relevance_button.click()
            select_newest_relevance = self.browser.wait_for_element(by=By.XPATH, selector="//option[text()='Newest']", selector_name="Ascending Sorting")
            select_newest_relevance.click()
            self.browser.time_wait(2)
            logger.info("Search news sorted descending.")
        except Exception as e:
            self.browser.take_screenshot("find_sort_button_error")
            logger.error(f"An error occurred while sorting news: {e}", exc_info=True)
            logger.error(f"Image of state of browser during sorting error saved in find_sort_button_error.png",
                         exc_info=True)

    def sort_news(self, descending=True):
        if descending:
            self.find_sort_button()

    def download_image(self, url, filename):
        try:
            response = requests.get(url)
            os.makedirs(os.path.dirname(f"output/img/{filename}"), exist_ok=True)
            with open(f"output/img/{filename}", 'wb') as file:
                file.write(response.content)
            logger.info(f"Image downloaded: {filename}")
        except Exception as e:
            self.browser.take_screenshot("download_error")
            logger.error(f"An error occurred while downloading the image: {e}", exc_info=True)
            logger.error(f"Image of state of browser during download error saved in download_error.png", exc_info=True)

    def save_to_excel(self, news_data):
        wb = Workbook()
        ws = wb.active
        ws.title = "News Data"

        ws.append(["Title", "Date", "Description", "Picture Filename", "Words Count", "Contains Money"])

        for news in news_data:
            ws.append([
                news["title"],
                news["date"],
                news["description"],
                news["picture_filename"],
                news["words-counts_title-description"],
                news["has_money"]
            ])

        file_name = "output/news_data.xlsx"
        wb.save(file_name)
        logger.info(f"Data saved to Excel file: {file_name}")

    def scrap_news(self):
        self.sort_news()
        news_data = self.get_news()
        self.save_to_excel(news_data)
