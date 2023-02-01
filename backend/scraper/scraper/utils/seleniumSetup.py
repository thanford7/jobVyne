import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, \
    NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

MISSING_DOM_EL_ERRORS = (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)

WEBDRIVER_WAIT_SECONDS = 3


def get_selenium(is_debug=False):
    chrome_options = Options()
    if not is_debug:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


def retry_click(parent_el, css_selector, is_allow_not_found=False):
    try:
        el = parent_el.find_element(By.CSS_SELECTOR, css_selector)
        el.click()
        return el
    except MISSING_DOM_EL_ERRORS:
        try:
            el = parent_el.find_element(By.CSS_SELECTOR, css_selector)
            el.click()
            return el
        except MISSING_DOM_EL_ERRORS as e:
            if is_allow_not_found:
                return None
            else:
                raise e


def get_dom_el_or_none(driver, parent_el, css_selector):
    try:
        return WebDriverWait(driver, WEBDRIVER_WAIT_SECONDS).until(lambda d: parent_el.find_element(By.CSS_SELECTOR, css_selector))
    except MISSING_DOM_EL_ERRORS:
        return None


def get_web_element_html(driver, web_el):
    return driver.execute_script("return arguments[0].innerHTML;", web_el)


def get_web_element_wait(driver, css_selector, parent_el=None):
    return WebDriverWait(driver, WEBDRIVER_WAIT_SECONDS)\
        .until(lambda d: (parent_el or d).find_element(By.CSS_SELECTOR, css_selector))
