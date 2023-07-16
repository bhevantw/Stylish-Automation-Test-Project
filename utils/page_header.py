#Standard library imports.
import logging
import time

#Related third party imports.
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import allure

#Local application/library specific imports.  
from utils.utils import print_function_info                                   
    

class PageHeader:

    cart_number = (By.CLASS_NAME, "header__link-icon-cart-number")
    profile_link = (By.XPATH, "//a[@href='./profile.html']")
    cart_link = (By.XPATH, "//a[@href='./cart.html']")
    home_link = (By.XPATH, "//a[@href='./index.html']")

 

    @allure.step("get_cart_number")
    @print_function_info
    def get_cart_number(self):
        cart_number = self.find_element(self.cart_number).text
        logging.info(f"Get cart number = {cart_number}")
        return int(cart_number)

    @allure.step("click_shopping_cart")
    @print_function_info
    def click_shopping_cart(self):        
        cart_link = self.find_element(self.cart_link, True)
        cart_link.click()
        logging.info("Go to shopping cart page")

    @allure.step("click_home_page")
    @print_function_info
    def click_home_page(self):        
        self.find_element(self.home_link, True).click()
        logging.info("Go to home page")

    @allure.step("click_profile")
    @print_function_info
    def click_profile(self):        
        profile_link = self.find_element(self.profile_link, True)
        profile_link.click()
        logging.info("Go to profile page")