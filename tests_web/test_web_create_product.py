#Standard library imports.
import logging
import time

#Related third party imports.
from allure_commons.types import AttachmentType
import allure
import pytest

#Local application/library specific imports.   
from page_objects.page_mgr import PageMgr
from test_data.test_data_from_excel import *


@allure.testcase("Scenario: Create Product Success (3 Test Cases)")
@pytest.mark.parametrize("data_row", get_data("Create Product Success"))
def test_create_product_success(auto_login, data_row):
    logging.info(f"Data row = {data_row}")
    page_mgr = auto_login
    new_product_object = page_mgr.get_new_product_page()  
    data_row['Title'] = data_row['Title']
    try:
      new_product_object.create_new_product(data_row)
      assert new_product_object.get_alert_text() == "Create Product Success"
      logging.info("alert message 'Create Product Success' should be shown : PASS")

      admin_page_object = page_mgr.get_admin_page()
      id = admin_page_object.get_id_by_title(data_row['Title'])    
      assert id != None 
      assert admin_page_object.get_category_by_title(data_row['Title']).text == data_row['Category'].lower()
      logging.info("Create Product Success : PASS")
    finally:
      admin_page_object.delete_product_by_id(id.text)
      assert admin_page_object.get_alert_text() == "Delete Product Success"
      logging.info(f"Delete product [{data_row['Title']}")


@allure.testcase("Scenario: Create Product with Invalid Value (20 Test Cases)")
@pytest.mark.parametrize("data_row", get_data("Create Product Failed"))
def test_create_product_with_invalid_value(auto_login, data_row):
    logging.info(f"Data row = {data_row}")
    page_mgr = auto_login
    new_product_object = page_mgr.get_new_product_page()       
    try:
      new_product_object.create_new_product(data_row) 
      alert_text = new_product_object.get_alert_text()   
      logging.info(f"alert_text={alert_text},expected text={data_row['Alert Msg']}")
      assert alert_text == data_row['Alert Msg']
      logging.info("Related alert message  should be shown : PASS")
    except:
      admin_page_object = page_mgr.get_admin_page()
      id = admin_page_object.get_id_by_title(data_row['Title'])
      admin_page_object.delete_product_by_id(id.text) 
      logging.info(f"Delete product [{data_row['Title']}]")


@allure.testcase("Scenario: Create Product without login")
@pytest.mark.parametrize("data_row", get_data("Create Product Success"))
def test_create_product_without_login(driver, data_row):
    page_mgr = PageMgr(driver)
    new_product_object = page_mgr.get_new_product_page() 
    new_product_object.create_new_product(data_row)
    assert new_product_object.get_alert_text() == "Please Login First"
    logging.info("alert message 'Please Login First' should be shown : PASS")
    page_mgr.get_profile_page().wait_for_login_page()
    assert driver.current_url == f"{os.getenv('WEB_DOMAIN')}/login.html"
    logging.info("redirected to login page : PASS")