#Standard library imports.
import logging
import time
import os

#Related third party imports.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure

#Local application/library specific imports.  
from utils.page_base import *
from utils.page_header import *
from page_objects.index_page import IndexPage
from page_objects.product_page import ProductPage
from utils.utils import print_function_info


class AdminPage(PageBase,PageHeader):

    create_product_btn = (By.XPATH, "//button[text()='Create New Product']")
    
    def get_category_locator(self, title):
        return (By.XPATH, f"//td[text()='{title}']/following-sibling::td")
    
    def get_id_locator(self, title):
        return (By.XPATH, f"//td[text()='{title}']/preceding-sibling::th")
    
    def get_delete_btn(self, id):
        return (By.XPATH, f"//button[@onclick='delete_product({id})']")

    def __init__(self, driver):
        super().__init__(driver)
        driver.get(f"{os.getenv('WEB_DOMAIN')}/admin/products.html")


    def create_new_product(self):
        create_product_btn = self.find_element(self.create_product_btn, True)
        create_product_btn.click()

    def get_id_by_title(self, title):
        return self.find_element(self.get_id_locator(title), False)
    
    def get_category_by_title(self, category):
        return self.find_element(self.get_category_locator(category), False)
    
    def delete_product_by_id(self, id):
        locator = self.get_delete_btn(id)
        logging.info(f"delete button id={id}, locator={locator}")        
        delete_btn = self.find_element(locator, True)
        delete_btn.click()