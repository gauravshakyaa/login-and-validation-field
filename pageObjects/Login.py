from selenium.webdriver.common.by import By
from testCases import conftest

class Login:
    inputField_username_name = (By.NAME, "username")
    inputField_password_name = (By.NAME, "password")
    button_submit_id = (By.ID, "submit")
    text_validationMessage_id = (By.ID, "error")

    def __init__(self, driver):
        self.driver = driver
    
    def set_username(self, username):
        conftest.sendKeys(driver=self.driver, locator=self.inputField_username_name, value=username)

    def set_password(self, password):
        conftest.sendKeys(driver=self.driver, locator=self.inputField_password_name, value=password)

    def click_submit(self):
        conftest.clickElement(driver=self.driver, locator=self.button_submit_id)
    
    def get_validation_message(self):
        validation_message =  conftest.getTextFromTextField(driver=self.driver, locator=self.text_validationMessage_id)
        return validation_message
    
    