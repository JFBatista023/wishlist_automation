import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def handle_timeout(driver, value):
    print(f"--------------- TIMEOUT {value} -------------")
    driver.refresh()
    time.sleep(4)


def get_element_text(driver, by, value, retry=2, wait_time=30, visibility=False):
    for attempt in range(retry):
        try:
            wait = WebDriverWait(driver, wait_time)
            if visibility:
                wait.until(EC.visibility_of_element_located((by, value)))
                time.sleep(2)
                element = driver.find_element(by, value)
                return element.text

            wait.until(EC.presence_of_element_located((by, value)))
            time.sleep(2)
            element = driver.find_element(by, value)
            return element.text
        except TimeoutException as e:
            handle_timeout(driver, value)
    raise TimeoutException()


def get_element(driver, by, value, retry=2, wait_time=30):
    for attempt in range(retry):
        try:
            wait = WebDriverWait(driver, wait_time)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException as e:
            handle_timeout(driver, value)
    return None
