import logging
import os

import requests
from openpyxl import Workbook
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import re
from src.utils.count_words import count_words
from src.utils.is_within_range import is_within_range

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

    def get_news(self, month_range=0, subscription_closed=False):
        news_data = []
        total_news_count = 0  # Inicializa o contador global de notícias

        while True:
            try:
                ul_element = self.browser.wait_for_element(by=By.XPATH,
                                                           selector="//ul[contains(@class, 'search-results')]",
                                                           selector_name="News Results")
                self.browser.scroll_to_element(ul_element)
                li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
                if not li_elements:
                    logger.info("No more news items found.")
                    break

                # Identifica o índice da última notícia da página atual
                last_index = len(li_elements) - 1

                for index in range(len(li_elements)):
                    li = li_elements[index]
                    if not subscription_closed:
                        subscription_closed = self.check_if_subscribe_popup_is_open()
                    self.browser.time_wait(0.5)
                    self.browser.scroll_to_element(li)
                    date_element = li.find_element(By.XPATH, ".//p[@class='promo-timestamp']")
                    within_period = is_within_range(date_element.text, month_range)  # Ajuste se necessário
                    if not within_period:
                        logger.info(f"News out of range interval: {date_element.text}")
                        return news_data

                    try:
                        picture_element = li.find_element(By.XPATH, ".//div[contains(@class, 'promo-media')]//picture")
                    except NoSuchElementException:
                        picture_element = None

                    image_url = None
                    if picture_element:
                        image_url = self.get_image_url_from_picture(picture_element)

                    picture_filename = None
                    if image_url:
                        picture_filename = f"{total_news_count + 1}.jpg"
                        self.download_image(image_url, picture_filename)

                    title_element = li.find_element(By.XPATH, ".//h3[@class='promo-title']//a")
                    description_element = li.find_element(By.XPATH, ".//p[@class='promo-description']")
                    self.browser.scroll_to_element(element=title_element)
                    title = title_element.text
                    self.browser.scroll_to_element(element=description_element)
                    description = description_element.text
                    self.browser.scroll_to_element(element=date_element)
                    date = date_element.text
                    title_word_count = count_words(title)
                    description_word_count = count_words(description)

                    words_count = title_word_count + description_word_count
                    has_money = bool(
                        re.search(r'\$\d+(\.\d+)?|\d+ dollars|\d+ USD', title + description, re.IGNORECASE))

                    news_data.append({
                        "title": title,
                        "date": date,
                        "description": description,
                        "picture_filename": picture_filename,
                        "words-counts_title-description": words_count,
                        "has_money": has_money
                    })

                    total_news_count += 1  # Incrementa o contador global de notícias

                    logger.info(f"News {total_news_count}: {title}")
                    print(f"News: {total_news_count}:")
                    print(f"Date: {date}")
                    print(f"Title: {title}")
                    print(f"Title Word Count: {title_word_count}")
                    print(f"Image: {picture_filename}")
                    print(f"Description: {description}")
                    print(f"Description Word Count: {description_word_count}")
                    print(f"Total Word Counts: {words_count}")
                    print("-" * 30)

                    if index == last_index:
                        try:
                            next_page_icon = self.browser.wait_for_element(by=By.CSS_SELECTOR,
                                                                           selector=".search-results-module-next-page a",
                                                                           selector_name="Next Page Button")
                            self.browser.scroll_to_element(next_page_icon)
                            self.browser.click(next_page_icon)
                            self.browser.time_wait(2)
                        except NoSuchElementException:
                            logger.info("No more pages to navigate.")
                            return news_data

            except Exception as e:
                self.browser.take_screenshot("get_news_error")
                logger.error(f"An error occurred while getting news: {e}", exc_info=True)
                logger.error(f"Image of state of browser during get news error saved in get_news_error.png",
                             exc_info=True)

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
                        self.browser.scroll_to_element(close_modal)
                        self.browser.click(close_modal)
                        self.browser.time_wait(1)

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
            self.browser.scroll_to_element(sort_by_relevance_button)
            self.browser.click(sort_by_relevance_button)
            select_newest_relevance = self.browser.wait_for_element(by=By.XPATH, selector="//option[text()='Newest']", selector_name="Ascending Sorting")
            self.browser.click(select_newest_relevance)
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

    def filter_by_category(self, category_name):

        try:
            see_all_categories_button = self.browser.wait_for_element_be_clickable(by=By.CSS_SELECTOR, selector="button.button.see-all-button", selector_name="Expand category button")
            self.browser.time_wait(1)
            self.browser.click(see_all_categories_button)

            filter_menu = self.browser.wait_for_element(
                by=By.CSS_SELECTOR,
                selector=".search-filter-menu",
                selector_name="Search Filter Menu"
            )

            categories = filter_menu.find_elements(By.CSS_SELECTOR, ".search-filter-input")
            for category in categories:
                category_name_element = category.find_element(By.CSS_SELECTOR, "span")
                if category_name_element.text.strip() == category_name:
                    checkbox = category.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                    self.browser.scroll_to_element(checkbox)
                    if not checkbox.is_selected():
                        self.browser.click(checkbox)
                        logger.info(f"Filtered by category: {category_name}")
                        return True
            logger.info(f"Category '{category_name}' not found.")
            return False
        except NoSuchElementException:
            logger.error("Filter menu or category elements not found.")
            return False

    def download_image(self, url, filename):
        try:
            response = requests.get(url)
            os.makedirs(os.path.dirname(f"output/{filename}"), exist_ok=True)
            with open(f"output/{filename}", 'wb') as file:
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

    def scrap_news(self, filter=filter, month_range=0):
        category_to_filter = filter
        self.sort_news()
        subscription_closed = self.check_if_subscribe_popup_is_open()
        self.filter_by_category(category_to_filter)
        news_data = self.get_news(month_range=month_range, subscription_closed=subscription_closed)
        self.save_to_excel(news_data)
