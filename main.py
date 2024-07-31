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


# Criação de um logger
logger = logging.getLogger("RPA-MAIN")


def main():
    logger.info("Initializing Web Browser")
    navigator = Browser(headless=True)
    navigator.navigate(url="https://www.latimes.com/")

    la_landing_page = LALandingPage(browser=navigator)
    la_landing_page.search("corinthians")

    la_search_page = LASearchPage(la_landing_page)
    la_search_page.scrap_news()



if __name__ == "__main__":
    main()
