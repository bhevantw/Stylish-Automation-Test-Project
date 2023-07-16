#Standard library imports.
import logging

#Related third party imports.
import allure

#Local application/library specific imports.  
from api_objects.login_api import *
from api_objects.logout_api import *
from utils.utils import *



@allure.story("test api logout success")
def test_api_logout_success(api_login_success):  
    session = api_login_success.session
    logout_api_obj = LogoutAPI(session)
    logout_api_obj.send()
    assert logout_api_obj.get_status_code() == 200
    assert logout_api_obj.get_message() == "Logout Success"
    logging.info("Assert API logout success : PASS")


@allure.story("test api logout failed without token")
def test_api_logout_without_token(api_login_success):  
    session = api_login_success.session
    logout_api_obj = LogoutAPI(session)
    logout_api_obj.modify_token("")
    logout_api_obj.send()
    assert logout_api_obj.get_status_code() == 401
    assert logout_api_obj.get_error_msg() == "Unauthorized"
    logging.info("Assert API logout failed without token : PASS")

@allure.story("test api logout failed with invalid token")
def test_api_logout_without_invalid_token(api_login_success):  
    session = api_login_success.session
    logout_api_obj = LogoutAPI(session)
    logout_api_obj.modify_token("abcde")
    logout_api_obj.send()
    assert logout_api_obj.get_status_code() == 403
    assert logout_api_obj.get_error_msg() == "Forbidden"
    logging.info("Assert API logout failed with invalid token : PASS")