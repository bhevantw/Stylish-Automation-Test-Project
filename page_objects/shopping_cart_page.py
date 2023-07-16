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


class CartPage(PageBase,PageHeader):

    #cart related locator
    cart_item = (By.XPATH, "//div[@class='cart__item']")
    cart_item_name = (By.CLASS_NAME, "cart__item-name")
    cart_item_id = (By.CLASS_NAME, "cart__item-id")
    cart_item_color = (By.CLASS_NAME, "cart__item-color")
    cart_item_size = (By.CLASS_NAME, "cart__item-size")
    cart_item_quantity = (By.XPATH, "//select[@class='cart__item-quantity-selector']")
    cart_item_price = (By.CLASS_NAME, "cart__item-price")
    cart_item_subtotal = (By.CLASS_NAME,"cart__item-subtotal")
    cart_delete_btn = (By.CLASS_NAME, "cart__delete-button")
    cart_check_out_btn = (By.XPATH, "//button[@class='checkout-button']")

    #info related locator
    info_receiver_input = (By.XPATH, "//div[@class='form__field-name' and text()='收件人姓名']/following-sibling::input[@class='form__field-input']")
    info_email_input = (By.XPATH, "//div[@class='form__field-name' and text()='Email']/following-sibling::input[@class='form__field-input']")
    info_mobile_input = (By.XPATH, "//div[@class='form__field-name' and text()='手機']/following-sibling::input[@class='form__field-input']")
    info_address_input = (By.XPATH, "//div[@class='form__field-name' and text()='地址']/following-sibling::input[@class='form__field-input']")
    
    #billing related locator
    bill_card_no_iframe = (By.XPATH, "//div[@id='card-number']/iframe")                          
    bill_card_no_input = (By.XPATH, "//input[@id='cc-number']")    
    bill_exp_date_iframe = (By.XPATH, "//div[@id='card-expiration-date']/iframe")
    bill_exp_date_input = (By.XPATH, "//input[@id='cc-exp']")
    bill_ccv_iframe = (By.XPATH, "//div[@id='card-ccv']/iframe")
    bill_ccv_input = (By.XPATH, "//input[@id='cc-ccv']")
    
    def get_info_deliver_time_input(self, time):
        if time == "Anytime":
           return (By.XPATH, "//input[@type='radio']/parent::label[@class='form__field-radio' and text()='不指定']")
        elif time == 'Morning':
           return (By.XPATH, "//input[@type='radio']/parent::label[@class='form__field-radio' and text()='08:00-12:00']")
        elif time == 'Afternoon':
            return (By.XPATH, "//input[@type='radio']/parent::label[@class='form__field-radio' and text()='14:00-18:00']")

    def get_cart_quantity_select(self, index):
        return (By.XPATH, f"(//select[@class='cart__item-quantity-selector'])[{index+1}]")

    @allure.step("get_cart_item_data")
    def get_cart_item_data(self):       
        cart_items = self.find_elements(self.cart_item)
        self.cart_items_list = []
        for item in cart_items :
            name = self.find_element_from_element(item,self.cart_item_name).text                                    
            pid = self.find_element_from_element(item,self.cart_item_id).text     
            color = self.find_element_from_element(item,self.cart_item_color).text.replace("顏色｜","")     
            size = self.find_element_from_element(item,self.cart_item_size).text.replace("尺寸｜","")             
            quantity = int(self.get_selected_option(self.cart_item_quantity))
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
        logging.info(f"Current shopping cart : {self.cart_items_list}")
        return self.cart_items_list
    
    @allure.step("get_cart_items")
    def get_cart_items(self):
        return self.cart_items_list
    
    @allure.step("delete_from_cart")
    def delete_from_cart(self, index):
        cart_items = self.find_elements(self.cart_item)
        cart_delete_btn = self.find_element_from_element(cart_items[index], self.cart_delete_btn)
        cart_delete_btn.click()
        logging.info(f"Delete {index}th item in the shopping cart")

    @allure.step("edit_quantity")
    def edit_quantity(self, item_index, quantity):        
        self.set_option(self.get_cart_quantity_select(item_index), quantity)
        logging.info(f"Edit quantity to {quantity}, item index={item_index}")
    
    @allure.step("check_out")
    def check_out(self):
        check_out_btn = self.find_element(self.cart_check_out_btn,True)
        check_out_btn.click()
        logging.info("Click check out button")

    def fill_receiver_info(self, receiver, email, mobile, address, deliver_time):        
        self.input(self.info_receiver_input, receiver)
        logging.info(f"Fill receiver field : {receiver}")
                
        self.input(self.info_email_input, email)        
        logging.info(f"Fill email field : {email}")
        
        self.input(self.info_mobile_input, mobile)
        logging.info(f"Fill mobile field : {mobile}")
        
        self.input(self.info_address_input, address)
        logging.info(f"Fill address field : {address}")
        
        deliver_time_radio = self.find_element(self.get_info_deliver_time_input(deliver_time), True)
        if deliver_time_radio != None:
           deliver_time_radio.click()
        logging.info(f"Fill deliver_time field : {deliver_time}")
    
    def fill_billing_info(self, card_no, expiry_date, security_code):
        self.switch_to_iframe(self.bill_card_no_iframe)
        self.input(self.bill_card_no_input, card_no)
        self.switch_to_default()
        logging.info(f"Fill card_no field : {card_no}")
        
        self.switch_to_iframe(self.bill_exp_date_iframe)
        self.input(self.bill_exp_date_input, expiry_date)
        self.switch_to_default()
        logging.info(f"Fill expiry_date field : {expiry_date}")

        self.switch_to_iframe(self.bill_ccv_iframe)
        self.input(self.bill_ccv_input, security_code)
        self.switch_to_default()
        logging.info(f"Fill security_code field : {security_code}")