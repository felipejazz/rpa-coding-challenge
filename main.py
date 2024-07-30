from src.models.browser import Browser
from src.utils.logging_configuration import logger


def main():
    logger.info("Initializing Web Browser")
    navigator = Browser(headless=True)
    # "https://reuters.com/"
    navigator.navigate(url="https://www.latimes.com/")
    navigator.search("corinthians")
    navigator.take_screenshot()





if __name__ == "__main__":
    main()