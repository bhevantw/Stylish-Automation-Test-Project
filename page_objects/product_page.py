#Standard library imports.
import logging

#Related third party imports.
from selenium.webdriver.common.by import By
import allure

#Local application/library specific imports.  
from utils.page_base import *
from utils.page_header import *


class ProductPage(PageBase,PageHeader):

    product_title = (By.CLASS_NAME, "product__title")
    product_id = (By.CLASS_NAME, "product__id")
    product_price = (By.CLASS_NAME, "product__price")
    color_selection = (By.XPATH, "//div[@class='product__color-selector']/div")    
    color_selected = (By.XPATH, "//div[@class='product__color product__color--selected']")
    size_selection = (By.XPATH,"//div[@class='product__size-selector']/div")      
    size_selected = (By.XPATH, "//div[@class='product__size product__size--selected']")    
    quantity_add_btn = (By.CLASS_NAME, "product__quantity-add")
    quantity_minus_btn = (By.CLASS_NAME, "product__quantity-minus")
    current_quantity_text = (By.CLASS_NAME, "product__quantity-value")
    add_to_cart_btn = (By.CLASS_NAME, "product__add-to-cart-button")
    subtotal = (By.CLASS_NAME, "cart__item-subtotal-content")
   
    @allure.step("click_color_selection")
    @print_function_info
    def click_color_selection(self, index):
        color_selectors = self.find_elements(self.color_selection)        
        color_selectors[index].click()
        return color_selectors[index]    

    @allure.step("click_size_selection")
    @print_function_info
    def click_size_selection(self, index):
        size_selectors = self.find_elements(self.size_selection)
        size_selectors[index].click()
        return size_selectors[index]
    
    @allure.step("click_add_quantity")
    @print_function_info
    def click_add_quantity(self, times):
        logging.info(f"click add quantity with {times} times")
        add_btn = self.find_element(self.quantity_add_btn)
        for i in range(0, times):
            add_btn.click()
    
    @allure.step("click_minus_quantity")
    @print_function_info
    def click_minus_quantity(self, times):
        logging.info(f"click minus quantity with {times} times")
        minus_btn = self.find_element(self.quantity_minus_btn)     
        for i in range(0, times):   
            minus_btn.click()

    @allure.step("get_current_quantity")
    @print_function_info
    def get_current_quantity(self):        
        elem = self.find_element(self.current_quantity_text)
        return int(elem.text)
    
    @allure.step("add_to_cart")
    @print_function_info
    def add_to_cart(self):
        add_to_cart_btn = self.find_element(self.add_to_cart_btn)
        add_to_cart_btn.click()                
        logging.info(f"Click add to cart button")
        return self.get_alert_text()
    
    @allure.step("get_product_data")
    def get_product_data(self):
        name = self.find_element(self.product_title, False).text
        pid = self.find_element(self.product_id, False).text
        price = self.find_element(self.product_price, False).text.replace("TWD.", "")
        color = self.find_element(self.color_selected, False).get_attribute('data_id').replace("color_code_","")  #selected color
        size = self.find_element(self.size_selected, False).text     #selected size
        quantity = self.get_current_quantity()   #currtent 
        # subtotal = self.find_element(self.subtotal, False).text.replace("NT.","")
        product_data = {
            'name' : name, 
            'pid' : pid, 
            'color' : color,
            'size' : size,
            'quantity' : quantity,
            'price' : price
            # 'subtotal' : subtotal
        }
        logging.info(f"Current product data = \n {product_data}")
        return product_data


