#Standard library imports.
import logging
import time

#Related third party imports.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure

#Local application/library specific imports.  
from utils.page_base import *
from utils.page_header import *
from utils.utils import print_function_info



class ProfilePage(PageBase,PageHeader):

    email_input = (By.ID, "email")
    password_input = (By.ID, "pw")
    login_btn = (By.XPATH, "//button[text()='Login']")
    logout_btn = (By.XPATH, "//div[@class='profile__content']/button[text()='登出']")


    @allure.step("login")
    @print_function_info
    def login(self, email, password):
        logging.info(f"Login with email={email},pw={password}")
        email_input = self.find_element(self.email_input, True)
        email_input.send_keys(email)
        password_input = self.find_element(self.password_input, True)
        password_input.send_keys(password)
        login_btn = self.find_element(self.login_btn, True)
        login_btn.click()        
        self.alert_text = self.get_alert_text()        
        # self.jwt_token = self.execute_script("return window.localStorage.getItem('jwtToken');") 
        self.jwt_token = self.driver.execute_script("return window.localStorage.getItem('jwtToken');") 
        logging.info(f"jwt={self.jwt_token}")
        
    @allure.step("logout")
    @print_function_info
    def logout(self):
        logging.info("Logout start")
        logout_btn = self.find_element(self.logout_btn, True)
        logout_btn.click()
        self.alert_text = self.get_alert_text() 

    
    @allure.step("wait for login page")
    @print_function_info
    def wait_for_login_page(self):
        self.find_element(self.logout_btn, True)
