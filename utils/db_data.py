#Standard library imports.
import logging
import json

#Related third party imports.
import allure
import pytest
import pymysql
from dotenv import dotenv_values
from dotenv import load_dotenv


#Local application/library specific imports.  
from utils.utils import *


@allure.step("get_product_name_list")
@print_function_info
def get_product_name_list(category, product_list):   
    if category == '':
        result = [item['title'] for item in product_list]
        logging.info(f"category={category}(all) \nresult={result}")
        return result
    else:        
        result = [item['title'] for item in product_list if item['category'] == category]
        logging.info(f"category={category} \nresult={result}")
        return result

@allure.step("get_product_name_list_by_keyword")
@print_function_info
def get_product_name_list_by_keyword(keyword, product_list):
    if keyword == '':
        result = [item['title'] for item in product_list]
        logging.info(f"keyword={keyword}(all) \nresult={result}")
        return result
    else:
        result = [item['title'] for item in product_list if keyword in item['title']] 
        logging.info(f"keyword={keyword} \nresult={result}")
        return result
    
@allure.step("get_product_info_list")
@print_function_info    
def get_product_info_list(category, product_list):
    result = []
    if category == "all":
        return product_list
    elif category == "men" or category == "women" or category == "accessories":
        for p in product_list:        
            if p['category'] == category:  
               result.append(p) 
    else:
        logging.info(f"{category} is not defined category")    
    logging.info(f"Return product info list = {result}")    
    return result

@allure.step("get_product_info_list")
@print_function_info    
def get_product_info_list_by_keyword(keyword, product_list):
    result = []
    for p in product_list:        
        if keyword in p['title']:  
            result.append(p) 
    logging.info(f"Return product info list = {result}, keyword={keyword}")    
    return result
            

@allure.step("get_product_info_list_by_id")
@print_function_info    
def get_product_info_list_by_id(id, product_list):    
    for p in product_list:        
        if p['id'] == id:  
            logging.info(f"Found product with id= {id}")
            return p
    logging.info(f"Not found product with id= {id}")   
    return None

@allure.step("get_order_by_id")
@print_function_info    
def get_order_by_id(id, order_list):    
    for o in order_list:        
        if o['id'] == id:  
            logging.info(f"Found order with id= {id}")
            return o
    logging.info(f"Not found order with id= {id}")   
    return None

def query_order_from_db_by_order_num(db_conn, onum):    
    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)    
    sql_query_product = f"SELECT * FROM order_table WHERE number={onum}"
    cursor.execute(sql_query_product)
    result = cursor.fetchall()    
    logging.info(f"get order list from db ,type = {type(result)}\n{result}")     
    return result


def query_products_from_db_by_id(db_conn, id):    
    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)    
    sql_query_product = f'''
    SELECT p.*, m1.images, m2.variant FROM stylish_backend.product AS p
	LEFT JOIN (			
    
			SELECT pi.product_id as id, GROUP_CONCAT(pi.image) AS images
			FROM stylish_backend.product AS p
			LEFT JOIN stylish_backend.product_images AS pi ON p.id = pi.product_id
			GROUP BY pi.product_id
            
			) m1 on p.id = m1.id

	LEFT JOIN (
    
			SELECT v.product_id as id, JSON_ARRAYAGG(JSON_OBJECT('color_code', c.code, 'size', v.size, 'stock', v.stock)) AS variant 
			FROM stylish_backend.product AS p
			LEFT JOIN  stylish_backend.variant AS v ON p.id = v.product_id
			LEFT JOIN stylish_backend.color AS c ON v.color_id = c.id
			GROUP BY v.product_id 
            
            ) m2 on  p.id = m2.id
    WHERE p.id = {id}
    '''
    cursor.execute(sql_query_product)
    result = cursor.fetchall()    #ex.[{'id':123,'category':woman,'title':女生上衣},{'id':123,'category':man,'title':男生上衣}]     
    logging.info(f"get product from db ,id = {id}\n{result}")    
    return result[0]