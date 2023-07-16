#Standard library imports.
import logging
import requests
import os

#Related third party imports.
import pymysql
import pytest
from dotenv import dotenv_values
from dotenv import load_dotenv


#Local application/library specific imports.  
from utils.utils import *
from api_objects.login_api import *



if 'ENV_FILE' in os.environ:
    env_file = os.environ['ENV_FILE']
    load_dotenv(env_file)
else:
    load_dotenv()  


@pytest.fixture
def get_session():
    session = requests.session()

    return session

@pytest.fixture
def api_login_success(get_session, get_account, get_password):
    session = get_session
    email = get_account
    password = get_password
    login_api_obj = LoginAPI(session, email, password)
    login_api_obj.send()
    return login_api_obj
    