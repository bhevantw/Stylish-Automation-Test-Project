#Standard library imports.
import logging
import os

#Related third party imports.
import allure
import pytest

#Local application/library specific imports.  
from api_objects.login_api import *
from api_objects.category_api import *
from test_data.test_data_from_excel import *
from utils.utils import *
from utils.db_data import *

@allure.story("test_api_category_success")
@pytest.mark.parametrize("category,paging", [('all',0), ('men',0), ('women', 0), ('accessories', 0),('all',1), ('men',1), ('women', 1), ('accessories', 1)])
def test_api_category_success(get_session, query_products_from_db, category, paging):
    category_api_obj = CategoryAPI(get_session, category, paging)
    category_api_obj.send()
    response_list = category_api_obj.get_rsp_product()
    expected_list = get_product_info_list(category, query_products_from_db)    
    start = 6 * paging    
    key_list = ['id', 'category', 'description', 'price', 'texture', 'wash', 'place', 'note', 'story']
    logging.info(f"Response list len = {len(response_list)}")
    logging.info(f"Expected list len = {len(expected_list)}")
    for i in range(0,len(response_list)):
        logging.debug(f"Assert [{i}] and [{start+i}]")
        assert compare_two_dicts(response_list[i], expected_list[start+i], key_list) == True
        if i == (len(response_list) - 1) and (6 * paging + i) != (len(expected_list) - 1):
           assert  category_api_obj.get_next_paging() == paging + 1
           logging.info("Assert next paging number: PASS")    
    logging.info(f"Assert category API success : PASS")

@allure.story("test_api_category_fail_invalid_category")
@pytest.mark.parametrize("category,paging", [("unknown", 0), ("", 0), (0, 0)])
def test_api_category_fail_invalid_category(get_session, category, paging):
    category_api_obj = CategoryAPI(get_session, category, paging)
    category_api_obj.send()           
    assert category_api_obj.get_status_code() == 400
    assert category_api_obj.get_error_msg() == "Invalid Category"
    logging.info(f"Assert category API fail invalid_category:PASS")


@allure.story("test_api_category_fail_invalid_paging")
@pytest.mark.parametrize("category,paging", [("women", "nan"), ("women" , "")])
def test_api_category_fail_incorrect_paging(get_session, category, paging):
    category_api_obj = CategoryAPI(get_session, category, paging)
    category_api_obj.send()           
    assert category_api_obj.get_status_code() == 400
    # return same result with paging = 0
    logging.info(f"Assert category API fail invalid category:PASS")


@allure.story("test_api_category_fail_not_found")
@pytest.mark.parametrize("category,paging", [("", 0)])
def test_api_category_fail_not_found(get_session, category, paging):
    category_api_obj = CategoryAPI(get_session, category, paging)
    category_api_obj.send()           
    assert category_api_obj.get_status_code() == 404    
    logging.info(f"Assert category API fail not found:PASS")