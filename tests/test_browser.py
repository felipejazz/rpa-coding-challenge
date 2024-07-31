import pytest
from unittest.mock import MagicMock, patch
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from src.models.browser import Browser


@pytest.fixture
def mock_browser():
    with patch.object(Browser, 'set_chrome_options', return_value=MagicMock()):
        with patch.object(Browser, 'set_webdriver', return_value=None):
            browser = Browser()
            browser.driver = MagicMock()
            browser.wait = MagicMock(return_value=MagicMock())
            yield browser


def test_navigate(mock_browser):
    mock_browser.driver.get = MagicMock()
    mock_browser.navigate("https://example.com")
    mock_browser.driver.get.assert_called_once_with("https://example.com")


def test_wait_for_element(mock_browser):
    mock_element = MagicMock()
    mock_browser.wait().until = MagicMock(return_value=mock_element)
    element = mock_browser.wait_for_element("selector", By.CSS_SELECTOR)
    mock_browser.wait().until.assert_called_once()
    assert element == mock_element


def test_retry_action_success(mock_browser):
    def action():
        return "Success"

    result = mock_browser.retry_action(action)
    assert result == "Success"


def test_retry_action_failure(mock_browser):
    attempt = [0]

    def action():
        if attempt[0] < 2:
            attempt[0] += 1
            raise StaleElementReferenceException()
        return "Success"

    result = mock_browser.retry_action(action, retries=3)
    assert result == "Success"


def test_wait_for_element_in_shadow(mock_browser):
    mock_shadow_host = MagicMock()
    mock_element = MagicMock()
    mock_browser.wait().until = MagicMock(return_value=mock_shadow_host)
    mock_browser.driver.execute_script = MagicMock(
        return_value=MagicMock(find_element=MagicMock(return_value=mock_element)))

    element = mock_browser.wait_for_element_in_shadow("shadow-host-selector", "element-selector", By.CSS_SELECTOR)
    mock_browser.wait().until()
    assert element == mock_element


def test_scroll_to_element(mock_browser):
    mock_element = MagicMock()
    mock_browser.driver.execute_script = MagicMock()
    mock_browser.scroll_to_element(mock_element)
    mock_browser.driver.execute_script.assert_called_once_with("arguments[0].scrollIntoView(true);", mock_element)


def test_take_screenshot(mock_browser):
    mock_browser.driver.save_screenshot = MagicMock()
    mock_browser.take_screenshot("test_screenshot")
    mock_browser.driver.save_screenshot.assert_called_once_with("test_screenshot.png")


def test_full_page_screenshot(mock_browser):
    mock_browser.driver.execute_script = MagicMock(side_effect=[1000, 2000])
    mock_browser.driver.set_window_size = MagicMock()
    mock_browser.driver.save_screenshot = MagicMock()
    mock_browser.full_page_screenshot("https://example.com")
    mock_browser.driver.set_window_size.assert_called_once_with(1000, 2000)
    mock_browser.driver.save_screenshot.assert_called_once_with('screenshot.png')
