#Standard library imports.
import logging

#Related third party imports.
import allure
import pytest

#Local application/library specific imports.  
from api_objects.search_api import *
from test_data.test_data_from_excel import *
from utils.utils import *
from utils.db_data import *


@allure.story("test api search success")
@pytest.mark.parametrize("keyword,paging",[('洋裝',0) ,('',0),('HELLO',0)])
def test_api_search_success(get_session, query_products_from_db, keyword, paging):
    search_api_obj = SearchAPI(get_session, keyword, paging)
    search_api_obj.send()
    response_list = search_api_obj.get_rsp_product()
    expected_list = get_product_info_list_by_keyword(keyword, query_products_from_db)
    start = 6 * paging    
    key_list = ['id', 'category', 'description', 'price', 'texture', 'wash', 'place', 'note', 'story']
    logging.info(f"Response list len = {len(response_list)}")
    logging.info(f"Expected list len = {len(expected_list)}")
    for i in range(0,len(response_list)):
        logging.info(f"Assert [{i}] and [{start+i}]")
        assert compare_two_dicts(response_list[i], expected_list[start+i], key_list) == True
        if i == (len(response_list) - 1) and i != (len(expected_list) - 1):
           assert  search_api_obj.get_next_paging() == paging + 1
           logging.info("Assert next paging number: PASS")  
    logging.info(f"Assert search API success : PASS")  


@pytest.mark.parametrize("keyword,paging",[('',0)])
def test_api_search_fail_empty_keyword(get_session, keyword, paging):  
    search_api_obj = SearchAPI(get_session, keyword, paging)
    search_api_obj.send()    
    assert search_api_obj.get_status_code() == 400
    assert search_api_obj.get_error_msg() == "Search Keyword is required."
    logging.info(f"Assert search API fail empty keyword : PASS")  


@pytest.mark.parametrize("keyword,paging",[('洋裝',"")])
def test_api_search_fail_incorrect_paging(get_session, keyword, paging):  
    search_api_obj = SearchAPI(get_session, keyword, paging)
    search_api_obj.send()    
    assert search_api_obj.get_status_code() == 400
    logging.info(f"Assert search API fail invalid paging : PASS")  
