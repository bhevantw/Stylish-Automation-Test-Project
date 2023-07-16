#Standard library imports.
import logging

#Related third party imports.
from allure_commons.types import AttachmentType
import allure
import pytest

#Local application/library specific imports.   
from page_objects.index_page import IndexPage
from page_objects.page_mgr import PageMgr
from utils.db_data import get_product_name_list


@allure.step("test_click_category")
@pytest.mark.parametrize("category", ['women', 'men', 'accessories'])
def test_click_category(driver, category, query_products_from_db):
    page_mgr = PageMgr(driver)
    index_page_obj = page_mgr.get_index_page()
    click_result = index_page_obj.click_category(category)
    assert click_result == True
    logging.info("Category click assert : PASS")
    result_list = index_page_obj.get_all_products_on_page()    
    expected_list = get_product_name_list(category, query_products_from_db)
    assert set(result_list) == set(expected_list)
    assert len(result_list) == len(expected_list)
    logging.info("Products assert: PASS")
 