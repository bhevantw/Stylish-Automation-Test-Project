#Standard library imports.
import logging
import os

#Related third party imports.
import allure
import pytest

#Local application/library specific imports.  
from api_objects.login_api import *
from api_objects.add_product_api import *
from api_objects.delete_product_api import *
from test_data.test_data_from_excel import *
from utils.utils import *
from utils.db_data import *



@allure.story("test_api_delete_product_success")
def test_api_delete_product_success(api_login_success):
    payload = {
        'category': "women",
        'title': "連身裙",
        'description': "詳細內容",
        'price': 100,
        'texture': "棉質",
        'wash': "手洗",
        'place': "Taiwan",
        'note': "Notes",
        'color_ids': [1],
        'sizes': ["F"],
        'story': "Story Content",
        'main_image': "mainImage.jpg",
        'other_images': ["otherImage0.jpg", "otherImage1.jpg"]
    }
    try:
        add_product_obj = AddProduct(api_login_success.session, payload)
        add_product_obj.send()
        id = add_product_obj.get_rsp_product_id() 
    except:
        logging.info("Get exception when deleting product")
    finally:
        delete_product_obj = DeleteProduct(api_login_success.session, id)
        delete_product_obj.send()
        assert delete_product_obj.get_status_code() == 200
        logging.info("Assert send delete product API : PASS")



@allure.story("test_api_delete_product_fail")
@pytest.mark.parametrize("id", ["", 12345678, "abc"])
def test_api_delete_product_fail(api_login_success, id):
    delete_product_obj = DeleteProduct(api_login_success.session, id)
    delete_product_obj.send()
    assert delete_product_obj.get_status_code() == 400
    assert delete_product_obj.get_error_msg() == "Product ID not found."
    logging.info("Assert send delete product API : PASS")