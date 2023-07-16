#Standard library imports.
import logging

#Related third party imports.
import allure
import pytest

#Local application/library specific imports.  
from api_objects.profile_api import *
from api_objects.logout_api import *
from api_objects.login_api import *
from utils.utils import *
from test_data.test_data_from_excel import *


@pytest.mark.parametrize("data_row", get_data("API Profile Success"))
@allure.story("test api profile success")
def test_api_profile_success(get_session, data_row):      
    email = data_row['Email']
    password = data_row['Password']
    login_api_obj = LoginAPI(get_session, email, password)    
    login_api_obj.send()
    api_profile_obj = ProfileAPI(get_session)
    api_profile_obj.send()
    assert api_profile_obj.get_status_code() == 200
    assert api_profile_obj.get_rsp_data("provider") == data_row['Provider']
    assert api_profile_obj.get_rsp_data("name") == data_row['Name']
    assert api_profile_obj.get_rsp_data("email") == data_row['Email']
    assert api_profile_obj.get_rsp_data("picture") == data_row['Picture']
    logging.info("Assert API profile success : PASS")

@allure.story("test api profile failed without token")
def test_api_profile_failed_without_token(api_login_success):  
    session = api_login_success.session
    api_profile_obj = ProfileAPI(session)
    api_profile_obj.modify_token("")
    api_profile_obj.send()
    assert api_profile_obj.get_status_code() == 401    
    assert api_profile_obj.get_error_msg() == "Unauthorized"
    logging.info("Assert API profile failed without token : PASS")


@allure.story("test api profile failed with fake token")
def test_api_profile_failed_with_fake_token(api_login_success):  
    session = api_login_success.session
    api_profile_obj = ProfileAPI(session)
    api_profile_obj.modify_token("abc")
    api_profile_obj.send()
    assert api_profile_obj.get_status_code() == 403    
    assert api_profile_obj.get_error_msg() == "Forbidden"
    logging.info("Assert API profile failed with fake token : PASS")

@allure.story("test api profile failed with invalid token")
def test_api_profile_failed_with_invalid_token(api_login_success):  
    session = api_login_success.session    
    api_logout_obj = LogoutAPI(session)
    api_logout_obj.send()

    api_profile_obj = ProfileAPI(session)
    api_profile_obj.send()
    assert api_profile_obj.get_status_code() == 403    
    assert api_profile_obj.get_error_msg() == "Invalid Access Token"
    logging.info("Assert API profile failed with invalid token : PASS")