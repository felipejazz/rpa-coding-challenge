import pytest
from unittest.mock import MagicMock

from selenium.webdriver.common.by import By

from src.models.la_landing_page import LALandingPage


@pytest.fixture
def search_page():
    mock_browser = MagicMock()
    return LALandingPage(browser=mock_browser)


def test_find_make_search_visible_button(search_page):
    search_page.browser.wait_for_element.return_value = MagicMock()

    result = search_page.find_make_search_visible_button()

    assert result is not None
    search_page.browser.wait_for_element.assert_called_once_with(by=By.XPATH,
                                                                 selector="/html/body/ps-header/header/div[2]/button")


def test_make_search_field_visible(search_page):
    mock_button = MagicMock()
    search_page.find_make_search_visible_button = MagicMock(return_value=mock_button)

    search_page.make_search_field_visible()

    search_page.browser.scroll_to_element.assert_called_once_with(mock_button)
    mock_button.click.assert_called_once()


def test_find_search_input_field(search_page):
    search_page.browser.wait_for_element.return_value = MagicMock()

    result = search_page.find_search_input_field()

    assert result is not None
    search_page.browser.wait_for_element.assert_called_once_with(by=By.XPATH,
                                                                 selector="/html/body/ps-header/header/div[2]/div[2]/form/label/input")


def test_find_search_submit_button(search_page):
    search_page.browser.wait_for_element.return_value = MagicMock()

    result = search_page.find_search_submit_button()

    assert result is not None
    search_page.browser.wait_for_element.assert_called_once_with(by=By.XPATH,
                                                                 selector="/html/body/ps-header/header/div[2]/div[2]/form/button")


def test_submit_search_form(search_page):
    mock_button = MagicMock()
    search_page.find_search_submit_button = MagicMock(return_value=mock_button)

    search_page.submit_search_form()

    search_page.browser.scroll_to_element.assert_called_once_with(mock_button)
    mock_button.click.assert_called_once()
    assert search_page.browser.scroll_to_element.call_count == 1


def test_search_for_keyword(search_page):
    mock_search_box = MagicMock()
    search_page.find_search_input_field = MagicMock(return_value=mock_search_box)

    search_page.search_for_keyword("test")

    search_page.browser.scroll_to_element(mock_search_box)
    assert mock_search_box.send_keys.call_count == 4  # Assuming keyword length is 4
    assert search_page.browser.time_wait.call_count == 4


def test_search(search_page):
    search_page.search_for_keyword = MagicMock()
    search_page.submit_search_form = MagicMock()

    search_page.search("test")

    search_page.search_for_keyword.assert_called_once_with("test")
    search_page.submit_search_form.assert_called_once()

