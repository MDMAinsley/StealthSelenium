import random
from selenium.common import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebDriver
from .utils import human_delay, retry_on_exception

@retry_on_exception()
def scroll_to_element(driver: WebDriver, element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    human_delay(0.5, 1.5)

@retry_on_exception()
def dwell_and_hover(driver: WebDriver, element, min_dwell=1.0, max_dwell=3.0):
    scroll_to_element(driver, element)
    ActionChains(driver).move_to_element(element).perform()
    human_delay(min_dwell, max_dwell)

@retry_on_exception()
def safe_click(driver: WebDriver, element):
    dwell_and_hover(driver, element)
    ActionChains(driver).move_to_element(element).pause(random.uniform(0.3, 0.8)).click().perform()
    human_delay()

@retry_on_exception()
def find_and_click(driver: WebDriver, by, value):
    element = driver.find_element(by, value)
    safe_click(driver, element)

def find_element_safe(driver, by, value):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None

def wait_for_element(driver, by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, value)))
    except:
        return None

def random_scroll(driver: WebDriver):
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_pos = random.randint(100, scroll_height)
    driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
    human_delay()
