import json

from robocorp.tasks import task
from src.models.browser import Browser
from src.models.la_landing_page import LALandingPage
from src.models.la_search_page import LASearchPage

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("RPA-MAIN")

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
@task
def main():
    config = load_config('config.json')
    logger.info("Initializing Web Browser")
    navigator = Browser(headless=True)
    navigator.navigate(url=config["url"])

    la_landing_page = LALandingPage(browser=navigator)
    la_landing_page.search(config["search_query"])

    la_search_page = LASearchPage(la_landing_page)
    la_search_page.scrap_news(filter=config["filter"], month_range=config["month_range"])
