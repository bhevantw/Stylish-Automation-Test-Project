#Standard library imports.
import logging

#Related third party imports.

#Local application/library specific imports.  
from utils.page_base import *
from page_objects.product_page  import ProductPage
from page_objects.profile_page import ProfilePage
from page_objects.index_page import IndexPage
from page_objects.shopping_cart_page import CartPage
from page_objects.thankyou_page import ThankyouPage
from page_objects.admin_page import AdminPage
from page_objects.new_product_page import NewProductPage


class PageMgr:

    def __init__(self, driver):
        self.driver = driver
        self.index_page_obj = None
        self.product_page_obj = None
        self.profile_page_obj = None
        self.cart_page_obj = None
        self.thankyou_page_obj = None
        self.admin_page_obj = None
        self.new_product_page_obj = None

    @print_function_info
    def get_index_page(self):
        if self.index_page_obj == None:           
           self.index_page_obj = IndexPage(self.driver)
           logging.info("Create index page object")
           return self.index_page_obj
        else:
           return self.index_page_obj 
    @print_function_info
    def get_profile_page(self):
        if self.profile_page_obj == None:
           self.profile_page_obj = ProfilePage(self.driver)
           logging.info("Create profile page object")
           return self.profile_page_obj
        else:
           return self.profile_page_obj 
        
    @print_function_info
    def get_product_page(self):
        if self.product_page_obj == None:
           self.product_page_obj = ProductPage(self.driver)
           logging.info("Create product page object")
           return self.product_page_obj
        else:
           return self.product_page_obj 
    
    @print_function_info
    def get_cart_page(self):
        if self.cart_page_obj == None:
           self.cart_page_obj = CartPage(self.driver)
           logging.info("Create shopping cart page object")
           return self.cart_page_obj
        else:
           return self.cart_page_obj 
    
    @print_function_info
    def get_thankyou_page(self):
        if self.thankyou_page_obj == None:
           self.thankyou_page_obj = ThankyouPage(self.driver)
           logging.info("Create thankyou page object")
           return self.thankyou_page_obj
        else:
           return self.thankyou_page_obj  
        
    @print_function_info
    def get_admin_page(self):
        if self.admin_page_obj == None:
           self.admin_page_obj = AdminPage(self.driver)
           logging.info("Create admin page object")
           return self.admin_page_obj
        else:
           return self.admin_page_obj  
        
    @print_function_info
    def get_new_product_page(self):
        if self.new_product_page_obj == None:
           self.new_product_page_obj = NewProductPage(self.driver)
           logging.info("Create new product page object")
           return self.new_product_page_obj
        else:
           return self.new_product_page_obj  