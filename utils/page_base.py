#Standard library imports.
import logging
import time

#Related third party imports.
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import allure

#Local application/library specific imports.  
from utils.utils import print_function_info


class PageBase:
        
    def __init__(self, driver):
        self.driver = driver
    
    
    def find_element(self, locator, clickable=False):  
        logging.debug(f"find element with selector={locator}, clickable={clickable}")      
        try:
            if clickable == True :
                elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
                if elem == None:
                   logging.debug(f"locator = [{locator}](clickable) is not found")
                return elem
            else:         
                elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator)) 
                if elem == None:
                   logging.debug(f"locator = [{locator}](unclickable) is not found") 
                return elem
        except Exception as ex:
            print("Exception type:", type(ex).__name__)
            print("Exception msg:", str(ex))                  
    
    
    def find_elements(self, locator):
        logging.debug(f"find element with locator={locator}")    
        try:            
            elems = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(locator))
            if elems == None:
                logging.debug(f"locator = [{locator}](unclickable) is not found") 
            return elems
        except Exception as ex:
            print("Exception type:", type(ex).__name__)
            print("Exception msg:", str(ex))  

    
    def find_element_from_element(self, element, locator):
        logging.debug(f"find child element = {element.text}, locator={locator}")    
        try:
            child_element = element.find_element(*locator)
            if child_element == None:
               logging.debug(f"child element with locator = [{locator}] is not found") 
            return child_element
        except Exception as ex:
            print("Exception type:", type(ex).__name__)
            print("Exception msg:", str(ex))  
            

    def execute_script(self, script):        
        self.driver.execute_script(script)
        logging.info(f"execute script = {script}")


    def input(self, locator, keyword):
        logging.debug(f"input = {keyword}, locator={locator}") 
        try:   
            input_bar = self.find_element(locator, True) 
            input_bar.clear()        
            input_bar.send_keys(keyword)
            input_bar.send_keys(Keys.RETURN)
        except Exception as ex:
            print("Exception type:", type(ex).__name__)
            print("Exception msg:", str(ex))  
    

    def switch_to_iframe(self, locator):        
        iframe = self.find_element(locator, False)
        self.driver.switch_to.frame(iframe)        
        logging.info(f"switch to iframe, locator={locator}")
    

    def switch_to_default(self):
        self.driver.switch_to.default_content()
        logging.info(f"switch to default")


    @allure.step("get_alert_text")
    @print_function_info
    def get_alert_text(self):
        time.sleep(1.5)
        alert = Alert(self.driver)
        alert_text = alert.text
        logging.info(f"Alert text = {alert_text}")
        alert.accept()
        return alert_text


    @allure.step("set_option")
    @print_function_info
    def set_option(self, locator, option_text): 
        logging.info(f"Set option locator = {locator}")
        selector = self.find_element(locator, True)       
        option = Select(selector)
        option.select_by_visible_text(option_text)
        logging.info(f"Set option to {option_text}")


    @allure.step("get_selected_option")
    @print_function_info
    def get_selected_option(self, locator):
        selector = self.find_element(locator, True)
        option = Select(selector)
        selected_option = option.first_selected_option        
        logging.info(f"Get selected option = {selected_option.text}")
        return selected_option.text