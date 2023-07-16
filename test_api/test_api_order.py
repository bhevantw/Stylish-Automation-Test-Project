#Standard library imports.
import logging
import os

#Related third party imports.
import allure
import pytest

#Local application/library specific imports.  
from api_objects.details_api import *
from api_objects.order_api import *
from page_objects.get_prime import *
from tests_web.conftest import *
from test_data.test_data_from_excel import *
from utils.utils import *
from utils.db_data import *

billing_info = {
        'card_no': 4242424242424242,
        'expiry_date': 1269,
        'security_code':123
}

@allure.story("test_api_order_success")
def test_api_order_success(driver, api_login_success, db_conn):    
    get_prime_page_obj = GetPrimePage(driver)
    prime = get_prime_page_obj.get_prime_num(billing_info)    
    pd = {
        "prime": prime,
        "order": {
            "shipping": "delivery",
            "payment": "credit_card",
            "subtotal": 1598,
            "freight": 30,
            "total": 1628,
            "recipient": {
                    "name": "Chan Tai Man",
                    "phone": "1234567890",
                    "email": "abc@abc.com",
                    "address": "台北市中山區 xxxxx",
                    "time": "anytime"
                },
            "list": [
                    {
                        "color": {
                            "code": "FFFFFF",
                            "name": "白色"
                        },
                        "id": "201807201824",
                        "image": "http://54.201.140.239/assets/201807201824/main.jpg",
                        "name": "前開衩扭結洋裝",
                        "price": 799,
                        "qty": 2,
                        "size": "S"
                    }
                ]
        }    
    }

    order_api_obj = OrderAPI(api_login_success.session)
    order_api_obj.send("post", payload = pd)
    order_num = order_api_obj.get_rsp_order_num()
    assert order_api_obj.get_status_code() == 200
    assert order_num != None
    logging.info(f"Assert send order API : PASS")

    expected_result = query_order_from_db_by_order_num(db_conn, order_num)
    expected_result[0]['details'] = json.loads(expected_result[0]['details'])   #This is a string from db
    assert expected_result[0]['details'] == pd['order']
   


@pytest.mark.parametrize("data_row", get_data("API Checkout with Invalid Value"))
@allure.story("test_api_order_fail")
def test_api_order_fail(driver, api_login_success, data_row):
    get_prime_page_obj = GetPrimePage(driver)
    prime = get_prime_page_obj.get_prime_num(billing_info)  
    if data_row['Prime'] != "original":
       prime = data_row['Prime']    
    pd = {
        "prime": prime,
        "order": {
            "shipping": data_row["Shipping"],
            "payment": data_row["Payment"],
            "subtotal": data_row["Subtotal"],
            "freight": data_row["Freight"],
            "total":  data_row["Total"],
            "recipient": {
                    "name": data_row["Receiver"],
                    "phone": data_row["Mobile"],
                    "email": data_row["Email"],
                    "address": data_row["Address"],
                    "time": data_row["Deliver Time"]
                },
            "list": [
                    {
                        "color": {
                            "code": data_row["Color Code 1"],
                            "name": data_row["Color Name 1"]
                        },
                        "id": data_row["Id 1"],
                        "image": data_row["Image 1"],
                        "name": data_row["Name 1"],
                        "price": data_row["Price 1"],
                        "qty": data_row["Qty 1"],
                        "size": data_row["Size 1"]
                    }
                ]
        }    
    }
    if data_row["Cart list"] == "0 item":
       del pd['order']['list']

    order_api_obj = OrderAPI(api_login_success.session)
    order_api_obj.send("post", payload = pd)    
    assert order_api_obj.get_status_code() == 400
    assert order_api_obj.get_error_msg() == data_row['Alert Msg']
    logging.info(f"Assert send order API fail : PASS")


@allure.story("test_api_order_get_success")
@pytest.mark.parametrize("id", [61292210781])
def test_api_order_get_success(api_login_success, db_conn, id):
    order_api_obj = OrderAPI(api_login_success.session)
    order_api_obj.send("get", id = id)       
    expected_result = query_order_from_db_by_order_num(db_conn, id)
    expected_result[0]['details'] = json.loads(expected_result[0]['details'])   #This is a string from db
    assert expected_result[0]['details'] == order_api_obj.get_rsp_order()
    logging.info(f"Assert send order get API success : PASS")



@allure.story("test_api_order_get_fail_not_found")
@pytest.mark.parametrize("id", [123, 10000000000, "abc", ""])
def test_api_order_get_fail_not_found(api_login_success, id):
    order_api_obj = OrderAPI(api_login_success.session)
    order_api_obj.send("get", id = id)       
    assert order_api_obj.get_status_code() == 400
    assert order_api_obj.get_error_msg() == "Order Not Found."
    logging.info(f"Assert send order get API order not found fail : PASS")

