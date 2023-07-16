#Standard library imports.
import logging

#Related third party imports.
import pymysql
import pytest
from dotenv import dotenv_values
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


#Local application/library specific imports.  
from utils.utils import *
from test_data.test_data_from_excel import *


if 'ENV_FILE' in os.environ:
    env_file = os.environ['ENV_FILE']
    load_dotenv(env_file)
else:
    load_dotenv()  

@pytest.fixture(scope = "session")
def db_conn():
    logging.info("start db connect")          
    db_settings = {
        'host' : os.getenv('DB_HOST'),
        'user' : os.getenv('DB_USER'),
        'password' : os.getenv('DB_PASSWORD'),
        'db' : os.getenv('DB'),
        'charset' : os.getenv('DB_CHARSET')
    }
    
    logging.info(f"DB settings = {db_settings}")
    db_conn = pymysql.connect(**db_settings)
    yield db_conn
    db_conn.close()
    logging.info("end db connect")

@pytest.fixture(scope = "module")
def query_products_from_db(db_conn):    
    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)    
    sql_query_product = '''
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
    '''
    cursor.execute(sql_query_product)
    result = cursor.fetchall()    #ex.[{'id':123,'category':woman,'title':女生上衣},{'id':123,'category':man,'title':男生上衣}]     
    logging.info(f"get product list from db \n{result}")    
    return result

@pytest.fixture(scope='module')
def get_account(worker_id):
    account = os.getenv(f"{worker_id}_STYLISH_ACCOUNT")
    logging.info(f"Get account = {account}")
    return account

@pytest.fixture(scope='module')
def get_password():
    password = os.getenv("STYLISH_PASSWORD")
    logging.info(f"Get password = {password}")
    return password