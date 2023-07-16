#Standard library imports.
import logging
import os

#Related third party imports.
import pytest
import allure

#Local application/library specific imports.  
from page_objects.index_page import IndexPage
from page_objects.product_page import ProductPage
from page_objects.profile_page import ProfilePage
from page_objects.page_mgr import PageMgr
from utils.db_data import *


@allure.step("test_web_login")
def test_web_login(auto_login):
    profile_page_obj = auto_login.get_profile_page()
    assert profile_page_obj.alert_text == "Login Success"
    assert profile_page_obj.jwt_token != None
    logging.info("Login success assert: PASS")
    profile_page_obj.logout()
    assert profile_page_obj.alert_text == "Logout Success"
    logging.info("Logout success assert: PASS")

@allure.step("test_web_logout")
def test_web_login_failed(driver):
    page_mgr = PageMgr(driver)
    incorrect_email = "fake@email.com"
    incorrect_password = "fake_password" 
    page_mgr.get_index_page().click_profile()   
    profile_page_obj = page_mgr.get_profile_page()
    profile_page_obj.login(incorrect_email, incorrect_password)
    assert profile_page_obj.alert_text == "Login Failed"
    logging.info("Login with incorrect account and password assert: PASS")

@allure.step("test_web_login_with_invalid_token")
def test_web_login_with_invalid_token(auto_login):
    logging.info(f"Login with invalid token")
    profile_page_obj = auto_login.get_profile_page()
    profile_page_obj.logout()    
    profile_page_obj.execute_script(f"window.localStorage.setItem('jwtToken','{profile_page_obj.jwt_token}');")
    auto_login.get_index_page().click_profile()    
    alert_text = profile_page_obj.get_alert_text()
    logging.info(f"Alert text = {alert_text}")
    assert alert_text == "Invalid Access Token"
    logging.info(f"Web login with invalid token assert: PASS")

