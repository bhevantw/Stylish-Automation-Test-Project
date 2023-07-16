#Standard library imports.
import logging
import os

#Related third party imports.
import allure
import pytest

#Local application/library specific imports.  
from api_objects.login_api import *
from test_data.test_data_from_excel import *
from utils.utils import *


@pytest.mark.parametrize("data_row", get_data("API Login Success"))
@allure.story("test api login success")
def test_api_login_success(get_session, data_row):
    logging.info(f"Data row = {data_row}")
    email = data_row['Email']
    password = data_row['Password']
    login_api_obj = LoginAPI(get_session, email, password)    
    login_api_obj.send()
    assert login_api_obj.get_status_code() == 200
    assert login_api_obj.get_rsp_data("id") == int(data_row['Id'])
    assert login_api_obj.get_rsp_data("provider") == data_row['Provider']
    assert login_api_obj.get_rsp_data("name") == data_row['Name']
    assert login_api_obj.get_rsp_data("email") == data_row['Email']
    assert login_api_obj.get_rsp_data("picture") == data_row['Picture']
    logging.info("API login with correct info : PASS")


@pytest.mark.parametrize("data_row", get_data("API Login Failed"))
@allure.story("test api login failed with incorrect info")
def test_api_login_failed_with_incorrect_info(get_session, data_row):    
    login_api_obj = LoginAPI(get_session, data_row['Email'], data_row['Password'])
    login_api_obj.send()
    assert login_api_obj.get_status_code() == int(data_row['Ststus Code'])
    assert login_api_obj.get_error_msg() == data_row['Error Msg']
    logging.info(f"Login failed with incorrect info : PASS")
