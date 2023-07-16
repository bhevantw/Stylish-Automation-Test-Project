#Standard library imports.
import logging
import os

#Related third party imports.
import allure
import pytest

#Local application/library specific imports.  
from api_objects.details_api import *
from test_data.test_data_from_excel import *
from utils.utils import *
from utils.db_data import *


@allure.story("test api search success")
@pytest.mark.parametrize("id",[201807202140])
def test_api_details_success(get_session, query_products_from_db, id):
    details_api_obj = DetailsAPI(get_session, id)
    details_api_obj.send()
    response_product = details_api_obj.get_rsp_product()
    expected_product = get_product_info_list_by_id(id, query_products_from_db)

    key_list = ['id', 'category', 'description', 'price', 'texture', 'wash', 'place', 'note', 'story']
    assert compare_two_dicts(response_product, expected_product, key_list)
    logging.info(f"Assert details API success : PASS")


@allure.story("test api search success")
@pytest.mark.parametrize("id",[202306151234,"fake_id",123])
def test_api_details_fail_invalid(get_session, id):
    details_api_obj = DetailsAPI(get_session, id)
    details_api_obj.send()
    
    assert details_api_obj.get_status_code() == 400
    assert details_api_obj.get_error_msg() == "Invalid Product ID"
    
    logging.info(f"Assert details API fail : PASS")