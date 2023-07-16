#Standard library imports.
import logging

#Related third party imports.
import pytest
import allure

#Local application/library specific imports.  
from page_objects.index_page import IndexPage
from utils.db_data import *


@allure.step("test_search_by_keyword")
@pytest.mark.parametrize("keyword",['洋裝','','HELLO'])
def test_search_by_keyword(driver, keyword, query_products_from_db):
    index_page_obj = IndexPage(driver)
    result_list = index_page_obj.search_on_page_with_keyword(keyword)
    logging.info(f"Assert search result={result_list}")
    expected_list = get_product_name_list_by_keyword(keyword, query_products_from_db)
    logging.info(f"Assert expected result={expected_list}")
    assert set(result_list) == set(expected_list)
    assert len(result_list) == len(expected_list)
    