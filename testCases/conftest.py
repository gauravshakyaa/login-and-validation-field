import logging
import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, WebDriverException

@pytest.fixture()
def setup():
    global driver
    browser = "chrome"
    if browser.__eq__("chrome"):
        driver = webdriver.Chrome()
    elif browser.__eq__("edge"):
        driver = webdriver.Edge()
    elif browser.__eq__("firefox"):
        driver = webdriver.Firefox()
    elif browser.__eq__("safari"):
        driver = webdriver.Safari()
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.get("https://practicetestautomation.com/practice-test-login/")
    driver.maximize_window()
    yield driver
    logging.info("All driver quited.")
    driver.quit()

def sendKeys(driver, locator, value, clear_field=True, condition="visible", timeout=3):
    try:
        logging.info(f"Sending keys by locator {locator}")
        waitForElement(driver, locator, timeout=timeout, condition=condition)
        if clear_field:
            driver.find_element(*locator).send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        driver.find_element(*locator).send_keys(value)
    except Exception:
        logging.error(f"An error occured in sendKeys when sending '{value}' in locator {locator}")

def clickElement(driver, locator, by=None, timeout=3, condition="visible"):
    if by is None:
        try:
            logging.info(f"Clicking an element with locator '{locator}'")
            waitForElement(driver, locator, timeout=timeout, condition=condition)
            driver.find_element(*locator).click()
        except Exception:
            logging.error(f"An error occured in clickElement with locator {locator}")
    else:
        try:
            logging.info(f"Clicking an element with locator '{locator}' by {by}")
            waitForElement(driver, locator, by=by, timeout=timeout, condition=condition)
            driver.find_element(by, locator).click() 
        except Exception:
            logging.error(f"An error occured in clickElement with locator {locator}")

def clearInputField(driver, locator):
    try:
        waitForElement(driver, locator, timeout=3)
        driver.find_element(*locator).send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    except Exception:
        logging.error(f"An error occured in clearInputField with locator {locator}")

def getTextFromTextField(driver, locator):
    try:
        waitForElement(driver, locator, timeout=3)
        return driver.find_element(*locator).text
    except Exception:
        logging.error(f"An error occured in getTextFromTextField with locator {locator}")

def waitForElement(driver, locator, condition="visible", timeout=3, text=None):
    wait = WebDriverWait(driver, timeout)
    try:
        conditions = {
        "clickable": EC.element_to_be_clickable(locator),
        "visible": EC.visibility_of_element_located(locator),
        "present": EC.presence_of_element_located(locator),
        "not_visible": EC.invisibility_of_element_located(locator),
        "text": EC.text_to_be_present_in_element(locator, text),
        "all": lambda driver: (
                EC.presence_of_element_located(locator)(driver) and
                EC.visibility_of_element_located(locator)(driver) and
                EC.element_to_be_clickable(locator)(driver)
            )
        }
        if condition not in conditions:
            raise ValueError(f"Invalid condition: {condition}")
        return wait.until(conditions[condition])
    except NoSuchElementException:
        logging.warning(f"No such element found with locator {locator}")
    except TimeoutException:
        logging.warning(f"Timeout exception occurred while waiting for element with locator {locator}")
    except ElementNotInteractableException:
        logging.warning(f"Element not interactable with locator {locator}")
    except StaleElementReferenceException:
        logging.warning(f"Stale element reference exception occurred while waiting for element with locator {locator}")
    except WebDriverException:
        logging.warning(f"Web driver exception occurred while waiting for element with locator {locator}")

def isElementPresent(driver, locator, timeout=3, condition="visible"): 
    try:
        if waitForElement(driver, locator=locator, condition=condition, timeout=timeout):
            return True
        else:
            return False
    except Exception:
        return False