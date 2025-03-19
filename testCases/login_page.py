from selenium.webdriver.remote.webdriver import WebDriver
from pageObjects.Login import Login
import pytest


class Test_login:
    def test_TC_01(self, setup):
        # Login with valid credentials
        driver : WebDriver = setup
        username = "student"
        password = "Password123"
        login = Login(driver=driver)
        login.set_username(username)
        login.set_password(password)
        login.click_submit()
        current_url = driver.current_url
        assert "logged-in-successfully" in current_url, "User login failed in valid credentials"
    
    def test_TC_02(self, setup):
        # Login with case-insensitive username 
        driver = setup
        username = "STUDENT"
        password = "Password123"
        login = Login(driver=driver)
        login.set_username(username)
        login.set_password(password)
        login.click_submit()
        validation_message = login.get_validation_message()
        assert "username" in validation_message and "invalid" in validation_message, "Validation message is not present"
    
    pytest.mark.skip("Remember me functionality is not present")
    def test_TC_03(self):
        pass
    
    def test_TC_04(self, setup):
        # Verify session timeout after inactivity
        driver : WebDriver= setup
        username = "student"
        password = "Password123"
        login = Login(driver=driver)
        login.set_username(username)
        login.set_password(password)
        login.click_submit()
        driver.implicitly_wait(600) # Wait for 10 minutes
        driver.refresh()
        current_url = driver.current_url
        assert "practice-test-login" in current_url, "Session is not expired after 10 minutes of inactivity"
    
    def test_TC_05(self, setup):
        # Login with invalid username
        driver : WebDriver = setup
        username = "incorrect username"
        password = "Password123"
        login = Login(driver=driver)
        login.set_username(username)
        login.set_password(password)
        login.click_submit()
        validation_message = login.get_validation_message()
        assert "username" in validation_message and "invalid" in validation_message, "Validation message is not present"
    
    def test_TC_06(self, setup):
        # Login with invalid password
        driver : WebDriver = setup
        username = "student"
        password = "incorrect password"
        login = Login(driver=driver)
        login.set_username(username)
        login.set_password(password)
        login.click_submit()
        validation_message = login.get_validation_message()
        assert "password" in validation_message and "invalid" in validation_message, "Validation message is not present"
    
    def test_TC_07(self, setup):
        # Login with empty username and password
        driver : WebDriver = setup
        login = Login(driver=driver)
        login.click_submit()
        validation_message = login.get_validation_message()
        assert "username" in validation_message and "invalid" in validation_message, "Validation message is not present"
    
    def test_TC_08(self, setup):
        # Login with empty username but a valid password
        driver : WebDriver = setup
        password = "Password123"
        login = Login(driver=driver)
        login.set_password(password)
        login.click_submit()
        validation_message = login.get_validation_message()
        assert "username" in validation_message and "invalid" in validation_message, "Validation message is not present"
        
    def test_TC_09(self, setup):
        # Login with empty password but a valid username
        driver : WebDriver = setup
        username = "student"
        login = Login(driver=driver)
        login.set_username(username)
        login.click_submit()
        validation_message = login.get_validation_message()
        assert "password" in validation_message and "invalid" in validation_message, "Validation message is not present"
    
    def test_TC_10(self, setup):
        # Login with multiple incorrect attempts (Account Lockout)
        driver : WebDriver = setup
        username = "invalid"
        password = "invalid"
        login = Login(driver=driver)
        for i in range(10):
            login.set_username(username)
            login.set_password(password)
            login.click_submit()
        validation_message = login.get_validation_message()
        assert "locked" in validation_message or "blocked" in validation_message, "Login with multiple incorrect attempts did not lock the account"
    
