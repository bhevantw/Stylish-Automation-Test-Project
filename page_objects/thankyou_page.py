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
from page_objects.index_page import IndexPage
from page_objects.product_page import ProductPage
from utils.utils import print_function_info


class ThankyouPage(PageBase,PageHeader):

    #purchased cart related locator
    cart_item = (By.XPATH, "//div[@class='cart__item']")
    cart_item_name = (By.CLASS_NAME, "cart__item-name")
    cart_item_id = (By.CLASS_NAME, "cart__item-id")
    cart_item_color = (By.CLASS_NAME, "cart__item-color")
    cart_item_size = (By.CLASS_NAME, "cart__item-size")
    cart_item_quantity = (By.XPATH, "//div[@class='cart__item-quantity-title']/following-sibling::div")
    cart_item_price = (By.CLASS_NAME, "cart__item-price")
    cart_item_subtotal = (By.XPATH,"//div[@class='cart__item-subtotal-content']")      

    @allure.step("get_purchased_item_data")
    def get_purchased_item_data(self):       
        purchased_items = self.find_elements(self.cart_item)
        self.cart_items_list = []
        for item in purchased_items :
            name = self.find_element_from_element(item,self.cart_item_name).text                                   
            pid = self.find_element_from_element(item,self.cart_item_id).text     
            color = self.find_element_from_element(item,self.cart_item_color).text.replace("顏色｜","")     
            size = self.find_element_from_element(item,self.cart_item_size).text.replace("尺寸｜","")             
            quantity = int(self.find_element_from_element(item,self.cart_item_quantity).text )
            price = self.find_element_from_element(item,self.cart_item_price).text.replace("NT.", "")            
            subtotal = self.find_element_from_element(item,self.cart_item_subtotal).text.replace("NT.", "") 
            logging.info(f"name:{name},pid:{pid},color:{color},size:{size},quantity:{quantity},price:{price},subtoal:{subtotal}")
            item_to_update = {                 
                 'name' : name, 
                 'pid' : pid, 
                 'color' : color,
                 'size' : size,
                 'quantity' : quantity,
                 'price' : price,       
                 'subtotal' : subtotal         
            }            
            self.cart_items_list.append(item_to_update)
        logging.info(f"Current purchased items : {self.cart_items_list}")
        return self.cart_items_list
