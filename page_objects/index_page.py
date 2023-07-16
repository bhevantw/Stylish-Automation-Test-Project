#Standard library imports.
import logging
import time
import random

#Related third party imports.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import allure

#Local application/library specific imports.  
from utils.page_base import *
from utils.page_header import *
from page_objects.product_page  import ProductPage



class IndexPage(PageBase,PageHeader):

    search_input = (By.CLASS_NAME, "header__search-input")


    def category_link(self, category_c):
        return (By.XPATH,f"//a[text()='{category_c}']")
    
    def product_link(self, product_name):
        return (By.XPATH, f"//a[@class='product']/div[@class='product__title' and text()='{product_name}']")
    
    @allure.step("click_category")
    @print_function_info
    def click_category(self, category):
        mapping_table = {
            "women" : "女裝",
            "men" : "男裝",
            "accessories" : "配件"
        }
        category_c = mapping_table.get(category)        
        logging.info(f"Click {category_c}")
        elem = self.find_element(self.category_link(category_c), False)
        if elem != None:
            elem.click()
        else:
            return False                    
        return True
    
    @allure.step("get_all_products_on_page")
    @print_function_info
    def get_all_products_on_page(self):
        current_num = 0   
        current_product_list = []                    
 
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  
            time.sleep(2)
            new_elem_check = self.find_element((By.XPATH, f"//div[@class='products' and count(a)>{current_num}]"), False)  
            elems = self.find_elements((By.XPATH, f"//div[@class='product__title']"))              
            if new_elem_check == None:  
               if elems == None:
                  return current_product_list
               else:             
                  current_product_list = [ elem.text for elem in elems]
                  return current_product_list        
            else:
               current_num = len(elems)               
                
    @allure.step("get_products_by_page_search_with_keyword")
    @print_function_info
    def search_on_page_with_keyword(self, keyword):
        self.input(self.search_input, keyword)        
        search_result = self.get_all_products_on_page()        
        logging.info(f"Search result = {search_result}")
        return search_result

    @allure.step("click_product")
    @print_function_info
    def click_product(self, product_name):
        logging.info(f"Click product = {product_name}")
        p_link = self.find_element(self.product_link(product_name), True)
        p_link.click()
        return ProductPage(self.driver)

    @allure.step("get_random_product")
    def get_random_product(self, num):
        current_products = self.get_all_products_on_page()
        logging.info(f"Random list = {current_products}")
        random_product = random.choices(current_products, k=num)
        logging.info(f"Random product (num={num})={random_product}")
        return random_product

