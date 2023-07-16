#Standard library imports.
import logging

#Related third party imports.
import pytest
import allure

#Local application/library specific imports.  
from page_objects.index_page import IndexPage
from page_objects.product_page import ProductPage
from utils.db_data import *


@allure.step("test_color_selection")
@pytest.mark.parametrize("product_name,color_index",[("前開衩扭結洋裝",0)])
def test_color_selection(driver, product_name, color_index):
    index_page_obj = IndexPage(driver)
    product_obj = index_page_obj.click_product(product_name)
    color_selector = product_obj.click_color_selection(color_index)
    color_class_value = color_selector.get_attribute('class')    
    logging.info(f"selection class = {color_class_value}, color={color_selector.get_attribute('data_id')}")
    assert color_class_value.endswith("--selected")    
    logging.info(f"Color selection assert: PASS")

@allure.step("test_size_selection")
@pytest.mark.parametrize("product_name,size_index",[("活力花紋長筒牛仔褲",1)])
def test_size_selection(driver, product_name, size_index):
    index_page_obj = IndexPage(driver)
    product_obj = index_page_obj.click_product(product_name)
    size_selector = product_obj.click_size_selection(size_index)
    size_vlass_value = size_selector.get_attribute('class')    
    logging.info(f"selection class = {size_vlass_value}, size={size_selector.text}")
    assert size_vlass_value.endswith("--selected")    
    logging.info(f"Size selection assert: PASS")

@allure.step("test_quantity_editor_disabled")
@pytest.mark.parametrize("product_name",["透肌澎澎防曬襯衫"])
def test_quantity_editor_disabled(driver, product_name):
    index_page_obj = IndexPage(driver)
    product_obj = index_page_obj.click_product(product_name)
    product_obj.click_add_quantity(1)
    quantity = product_obj.get_current_quantity()
    assert quantity == 1
    logging.info(f"Quantity editor disabled with Add assert: PASS")
    product_obj.click_minus_quantity(1)
    assert quantity == 1
    logging.info(f"Quantity editor disabled with Minus assert: PASS")

@allure.step("test_quantity_editor_increase")
@pytest.mark.parametrize("product_name,color_index,size_index",[("純色輕薄百搭襯衫",0,0)])
def test_quantity_editor_increase(driver, product_name, color_index, size_index):
    index_page_obj = IndexPage(driver)
    product_obj = index_page_obj.click_product(product_name)
    product_obj.click_color_selection(color_index)
    product_obj.click_size_selection(size_index)
    product_obj.click_add_quantity(8)
    quantity = product_obj.get_current_quantity()
    assert quantity == 9
    logging.info(f"Quantity editor increase (1+8=9) assert: PASS")
    product_obj.click_add_quantity(2)
    quantity = product_obj.get_current_quantity()
    assert quantity == 9
    logging.info(f"Quantity editor increase (9+2=>9) assert: PASS")

@allure.step("test_quantity_editor_decrease")
@pytest.mark.parametrize("product_name,color_index,size_index",[("純色輕薄百搭襯衫",0,0)])
def test_quantity_editor_decrease(driver, product_name, color_index, size_index):
    index_page_obj = IndexPage(driver)
    product_obj = index_page_obj.click_product(product_name)
    product_obj.click_color_selection(color_index)
    product_obj.click_size_selection(size_index)
    product_obj.click_add_quantity(8)
    product_obj.click_minus_quantity(8)
    quantity = product_obj.get_current_quantity()
    assert quantity == 1
    logging.info(f"Quantity editor decrease (1+8-8=>1) assert: PASS")

@allure.step("test_add_to_cart_success")
@pytest.mark.parametrize("product_name,color_index,size_index",[("純色輕薄百搭襯衫",0,0)])
def test_add_to_cart_success(driver, product_name, color_index, size_index):
    index_page_obj = IndexPage(driver)
    product_obj = index_page_obj.click_product(product_name)
    product_obj.click_color_selection(color_index)
    product_obj.click_size_selection(size_index)
    alert_text = product_obj.add_to_cart()
    assert alert_text == "已加入購物車"
    logging.info(f"Add to cart (success) assert: PASS")

@allure.step("test_add_to_cart_fail")
@pytest.mark.parametrize("product_name,color_index,size_index",[("純色輕薄百搭襯衫",0,0)])
def test_add_to_cart_fail(driver, product_name, color_index, size_index):
    index_page_obj = IndexPage(driver)
    product_obj = index_page_obj.click_product(product_name)        
    alert_text = product_obj.add_to_cart()
    assert alert_text == "請選擇尺寸"
    logging.info(f"Add to cart (fail) assert: PASS")