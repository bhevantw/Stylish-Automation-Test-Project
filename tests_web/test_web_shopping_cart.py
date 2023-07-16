#Standard library imports.
import logging
import random

#Related third party imports.
import pytest
import allure

#Local application/library specific imports.  
from page_objects.index_page import IndexPage
from page_objects.product_page import ProductPage
from page_objects.shopping_cart_page import CartPage
from page_objects.page_mgr import PageMgr
from utils.db_data import *


@allure.step("test_shopping_cart_info_correct")
@pytest.mark.parametrize("product_name,color_index,size_index",[("純色輕薄百搭襯衫",0,0)])
def test_shopping_cart_info_correct(driver, product_name, color_index, size_index):
    page_mgr = PageMgr(driver)
    index_page_obj = page_mgr.get_index_page()
    index_page_obj.click_product(product_name)
    product_obj = page_mgr.get_product_page()
    product_obj.click_color_selection(color_index)
    product_obj.click_size_selection(size_index)
    product_data_to_the_cart = product_obj.get_product_data()
    product_obj.add_to_cart()

    index_page_obj.click_shopping_cart()
    cart_page_obj = page_mgr.get_cart_page()
    product_data_in_the_cart = cart_page_obj.get_cart_item_data()

    logging.info(f"Product data = \n{product_data_to_the_cart}")
    logging.info(f"Product data in cart = \n{product_data_in_the_cart}")

    assert product_data_to_the_cart['name'] == product_data_in_the_cart[0]['name']
    assert product_data_to_the_cart['pid'] == product_data_in_the_cart[0]['pid']
    assert product_data_to_the_cart['size'] == product_data_in_the_cart[0]['size']
    assert product_data_to_the_cart['price'] == product_data_in_the_cart[0]['price']
    assert product_data_to_the_cart['quantity'] == product_data_in_the_cart[0]['quantity']
    logging.info(f"Shopping cart info correct : PASS")

@allure.step("test_remove_product_from_cart")
@pytest.mark.parametrize("product_name1,product_name2,color_index,size_index",[("前開衩扭結洋裝","時尚輕鬆休閒西裝",0,0)])
def test_remove_product_from_cart(driver, product_name1, product_name2, color_index, size_index):
    page_mgr = PageMgr(driver)
    index_page_obj = page_mgr.get_index_page()
    index_page_obj.click_product(product_name1)
    product_obj = page_mgr.get_product_page()

    #Add first product to cart
    product_obj.click_color_selection(color_index)
    product_obj.click_size_selection(size_index)    
    product_obj.add_to_cart()

    #Add second product to cart
    index_page_obj.click_home_page()
    index_page_obj.click_product(product_name2)
    product_obj.click_color_selection(color_index)
    product_obj.click_size_selection(size_index)    
    product_obj.add_to_cart()

    #Delete a random item in the cart
    index_page_obj.click_shopping_cart()
    cart_page_obj = page_mgr.get_cart_page()    
    list_before_del = cart_page_obj.get_cart_item_data()
    index_to_del = random.randint(0, 1)
    
    cart_page_obj.delete_from_cart(index_to_del)
    alert_text = cart_page_obj.get_alert_text()

    # remove the deleted item
    del list_before_del[index_to_del]
   
    #get current cart items
    list_after_del = cart_page_obj.get_cart_item_data()

    logging.info(f"Cart list before deleting\n{list_before_del}")
    logging.info(f"Cart list after deleting\n{list_after_del}")

    assert alert_text == "已刪除商品"
    logging.info("Alert message '已刪除商品' should be shown : PASS")
    assert list_after_del == list_before_del
    logging.info("New cart info should be updated correctly : PASS")
    item_len = len(cart_page_obj.get_cart_item_data())
    assert item_len == 1
    logging.info("New cart info should be updated correctly : PASS")
    assert cart_page_obj.get_cart_number() == 1
    logging.info("Cart icon number is updated correctly : PASS")

@allure.step("test_edit_quantity_in_cart")
@pytest.mark.parametrize("product_name,color_index,size_index",[("活力花紋長筒牛仔褲",1,1)])
def test_edit_quantity_in_cart(driver, product_name, color_index, size_index):
    page_mgr = PageMgr(driver)
    index_page_obj = page_mgr.get_index_page()
    index_page_obj.click_product(product_name)
    product_obj = page_mgr.get_product_page()

    #Add a product to cart
    product_obj.click_color_selection(color_index)
    product_obj.click_size_selection(size_index)    
    product_obj.add_to_cart()

    #edit the quantity
    cart_page_obj = page_mgr.get_cart_page()
    cart_page_obj.click_shopping_cart()
    cart_page_obj.edit_quantity(0,"2")    #quantity to 2 with first item in cart
    alert_text = cart_page_obj.get_alert_text()
    assert alert_text == "已修改數量"
    logging.info("Then alert message '已修改數量' should be shown : PASS")

    #check subtotal
    items = cart_page_obj.get_cart_item_data()
    logging.info(f"subtotal = {items[0]['subtotal']}")
    assert items[0]['subtotal'] == "2598"
    logging.info("Subtotal should be updated correctly : PASS")