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


def create_variant(color_id_list, size_list):
    color_code_mapping ={
        "1": "FFFFFF",
        "2": "DDFFBB",
        "3": "CCCCCC",
        "4": "BB7744",
        "5": "DDF0FF",
        "6": "334455",
        "7": "FFDDDD"
    }
    vaiant = []
    for id in color_id_list:
        for size in size_list:
            v = {}
            v['size'] = size
            v['color_code'] = color_code_mapping[id]
            v['stock'] = 9
            vaiant.append(v)
    logging.info(f"Create variant = {vaiant}")
    return vaiant


@allure.story("test_api_add_product_success")
@pytest.mark.parametrize("data_row", get_data("API Create Product Success"))
def test_api_add_product_success(api_login_success, data_row , db_conn):
    payload = {
        'category': data_row['Category'],
        'title': data_row['Title'],
        'description': data_row['Description'],
        'price': int(data_row['Price']),
        'texture': data_row['Texture'],
        'wash': data_row['Wash'],
        'place': data_row['Place of Product'],
        'note': data_row['Note'],
        'color_ids': data_row['ColorIDs'].split(","),
        'sizes': data_row['Sizes'].split(","),
        'story': data_row['Story'],
        'main_image': data_row['Main Image'],
        'other_images': [data_row['Other Image 1'], data_row['Other Image 2']]
    }
    try:
        add_product_obj = AddProduct(api_login_success.session, payload)
        add_product_obj.send()
        id = add_product_obj.get_rsp_product_id() 
        product = query_products_from_db_by_id(db_conn, id)
        assert add_product_obj.get_status_code() == 200
        assert product['id'] == id
        assert product['category'] == payload['category']
        assert product['title'] == payload['title']
        assert product['description'] == payload['description']
        assert product['price'] == payload['price']
        assert product['wash'] == payload['wash']
        assert product['place'] == payload['place']
        assert product['note'] == payload['note']    
        assert product['variant'] == create_variant(payload['color_ids'],payload['sizes'])
        assert product['story'] == payload['story']
        assert product['main_image'] == payload['main_image']
        assert product['images'].split(",") == payload['other_images']
        logging.info("Assert send add product API : PASS")
    except:
        logging.info("Get exception with assertion")
    finally:
        # delete test data
        delete_product_obj = DeleteProduct(api_login_success.session, id)
        delete_product_obj.send()
        assert delete_product_obj.get_status_code() == 200
        logging.info("Delete test data completed")
        




@allure.story("test_api_add_product_fail")
@pytest.mark.parametrize("data_row", get_data("API Create Product Failed"))
def test_api_add_product_fail(api_login_success, data_row , db_conn):
    payload = {
        'category': data_row['Category'],
        'title': data_row['Title'],
        'description': data_row['Description'],
        'price': data_row['Price'],
        'texture': data_row['Texture'],
        'wash': data_row['Wash'],
        'place': data_row['Place of Product'],
        'note': data_row['Note'],
        'color_ids': data_row['ColorIDs'].split(","),
        'sizes': data_row['Sizes'].split(","),
        'story': data_row['Story'],
        'main_image': data_row['Main Image'],
        'other_images': [data_row['Other Image 1'], data_row['Other Image 2']]
    }
    add_product_obj = AddProduct(api_login_success.session, payload)
    try:        
        add_product_obj.send()
        assert add_product_obj.get_status_code() == 400
        assert add_product_obj.get_error_msg() == data_row['Alert Msg']
    except:
        logging.info("Get exception with assertion")
    finally:
        if add_product_obj.get_rsp_product_id()!= None:
           # delete test data
           delete_product_obj = DeleteProduct(api_login_success.session, id)
           delete_product_obj.send()
           assert delete_product_obj.get_status_code() == 200
           logging.info("Assert send add product API : PASS")
