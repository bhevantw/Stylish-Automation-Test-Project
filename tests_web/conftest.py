#Standard library imports.
import logging


#Related third party imports.
import pymysql
import pytest
from dotenv import dotenv_values
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Local application/library specific imports.  
from utils.utils import *
from test_data.test_data_from_excel import *
from page_objects.page_mgr import PageMgr

if 'ENV_FILE' in os.environ:
    env_file = os.environ['ENV_FILE']
    load_dotenv(env_file)
else:
    load_dotenv()  

@pytest.fixture
def driver():
    chrome_options = Options() 
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get(f"{os.getenv('WEB_DOMAIN')}")
    driver.maximize_window() 
    yield driver
    driver.quit()


@pytest.fixture
def auto_login(driver, worker_id):                   
    email = os.getenv(worker_id+"_STYLISH_ACCOUNT")    
    password = os.getenv('STYLISH_PASSWORD')
    logging.info(f"Login with email={email}, worker id={worker_id} ,password={password}")
    
    page_mgr = PageMgr(driver)
    page_mgr.get_index_page().click_profile() 
    page_mgr.get_profile_page().login(email, password)
    logging.info(f"Login in fixture")
    return page_mgr
