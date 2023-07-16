#Standard library imports.
import logging
import os


#Related third party imports.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import allure

#Local application/library specific imports.  
from utils.page_base import *


class GetPrimePage(PageBase):
    card_num_input = (By.ID, "cc-number")
    expiry_date_input = (By.ID, "cc-exp")
    cvc_input = (By.ID, "cc-cvc")
    get_btn = (By.ID, "checkoutBtn")
    card_num_iframe = (By.XPATH, "//div[@id='card-number']/iframe")
    expiry_date_iframe = (By.XPATH, "//div[@id='card-expiration-date']/iframe")
    cvc_iframe = (By.XPATH, "//div[@id='card-ccv']/iframe")
    

    def __init__(self, driver):
        super().__init__(driver)        
        self.driver.get(f"{os.getenv('WEB_DOMAIN')}/get_prime.html")

    def get_prime_num(self, info):        
        self._input_card_num(info['card_no'])
        self._input_expiry_date(info['expiry_date'])
        self._input_cvc(info['security_code'])
        self._click_get_prime()
        prime = self.get_alert_text()
        logging.info(f"Prime num = {prime}")
        return prime

    def _input_card_num(self, num):
        self.switch_to_iframe(self.card_num_iframe)
        self.input(self.card_num_input,num)
        self.switch_to_default()
        logging.info(f"Input card num = {num}")        
        
    def _input_expiry_date(self, date):
        self.switch_to_iframe(self.expiry_date_iframe)
        self.input(self.expiry_date_input,date)
        self.switch_to_default()
        logging.info(f"Input expiry date = {date}")   
    
    def _input_cvc(self, cvc):
        self.switch_to_iframe(self.cvc_iframe)
        self.input(self.cvc_input,cvc)
        self.switch_to_default()
        logging.info("Input cvc = {cvc}")   
    
    def _click_get_prime(self):
        self.find_element(self.get_btn, True).click()

