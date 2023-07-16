#Standard library imports.
import logging

#Related third party imports.
from allure_commons.types import AttachmentType
import allure
import pytest

#Local application/library specific imports.   
from page_objects.page_mgr import PageMgr
from utils.db_data import get_product_name_list
from test_data.test_data_from_excel import *



@allure.testcase("Checkout with empty cart")
def test_checkout_with_empty_cart(auto_login):
    page_mgr = auto_login
    cartp_page_obj = page_mgr.get_cart_page()
    cartp_page_obj.click_shopping_cart()
    cartp_page_obj.check_out()
    assert cartp_page_obj.get_alert_text() == "尚未選購商品"
    logging.info("alert message '尚未選購商品' should be shown : PASS")

@allure.testcase("test_checkout_with_invalid_values")
@pytest.mark.parametrize("data_row", get_data("Checkout with Invalid Value"))
def test_checkout_with_invalid_values(auto_login, data_row):
    logging.info(f"Data = {data_row}")    
    # Add a product
    page_mgr = auto_login
    index_page_obj = page_mgr.get_index_page()
    index_page_obj.click_home_page()
    index_page_obj.click_product("前開衩扭結洋裝")
    product_obj = page_mgr.get_product_page()
    product_obj.click_color_selection(0)
    product_obj.click_size_selection(0)    
    product_obj.add_to_cart()

    # logging.info("Start to test checkout")        
    receiver = data_row['Receiver']
    email = data_row['Email']
    mobile = data_row['Mobile']
    address = data_row['Address']
    deliver_time = data_row['Deliver Time']
    card_no = data_row['Credit Card No']
    expiry_date = data_row['Expiry Date']
    security_code = data_row['Security Code']
    alert_msg = data_row['Alert Msg']
    
    cart_page_obj = page_mgr.get_cart_page()
    cart_page_obj.click_shopping_cart()
    cart_page_obj.fill_receiver_info(receiver, email, mobile, address, deliver_time)
    cart_page_obj.fill_billing_info(card_no, expiry_date, security_code)
    cart_page_obj.check_out()

    alert_text = cart_page_obj.get_alert_text()
    assert alert_text == alert_msg
    logging.info(f"checkout_with_invalid_values alert message({alert_msg}) should be shown : PASS")

@allure.testcase("test_checkout_with_valid_values")
@pytest.mark.parametrize("data_row", get_data("Checkout with Valid Value"))
def test_checkout_with_valid_values(auto_login, data_row):
    logging.info(f"Data = {data_row}")    
    # Add a product
    page_mgr = auto_login
    index_page_obj = page_mgr.get_index_page()
    index_page_obj.click_home_page()
    index_page_obj.click_product("前開衩扭結洋裝")
    product_obj = page_mgr.get_product_page()
    product_obj.click_color_selection(0)
    product_obj.click_size_selection(0)    
    product_obj.add_to_cart()    

    receiver = data_row['Receiver']
    email = data_row['Email']
    mobile = data_row['Mobile']
    address = data_row['Address']
    deliver_time = data_row['Deliver Time']
    card_no = data_row['Credit Card No']
    expiry_date = data_row['Expiry Date']
    security_code = data_row['Security Code']
    
    cart_page_obj = page_mgr.get_cart_page()
    cart_page_obj.click_shopping_cart()
    to_buy_list = cart_page_obj.get_cart_item_data()
    cart_page_obj.fill_receiver_info(receiver, email, mobile, address, deliver_time)
    cart_page_obj.fill_billing_info(card_no, expiry_date, security_code)
    cart_page_obj.check_out()

    alert_text = cart_page_obj.get_alert_text()
    assert alert_text == "付款成功"
    logging.info(f"Checkout with valid values : PASS")

    thankyou_page_obj = page_mgr.get_thankyou_page()
    purchased_list = thankyou_page_obj.get_purchased_item_data()
    assert to_buy_list == purchased_list
    logging.info(f"Thankyou page verification : PASS")