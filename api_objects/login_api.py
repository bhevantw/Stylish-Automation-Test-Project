#Standard library imports.
import logging
import requests
import os

#Related third party imports.
from dotenv import dotenv_values
from dotenv import load_dotenv


#Local application/library specific imports.  
from utils.api_base import *


class LoginAPI(APIBase):

    def __init__(self, session, email=None, password=None):
        url = f"{os.getenv('API_URL')}/user/login"
        super().__init__(session, url)
        self.payload = {
            "provider": "native",
            "email": email,
            "password": password
        }
        self.token = None
        

    def send(self):
        self.api_request("post", json=self.payload)
        logging.info(f"Send login api , json = {self.payload}")
        if self.get_status_code() == 200:
            self.token = f"Bearer {self.get_basic_token()}"
            self.session.headers["Authorization"] = self.token
            logging.info(f"LoginAPI send and toekn=Bearer {self.token}")
 
    def get_basic_token(self):
        json_body = self.response.json()        
        token = json_body["data"]["access_token"]
        logging.info(f"token={token}")
        return token
    
    def get_bearer_token(self):
        return self.token
    
    def get_rsp_data(self, key):
        json_body = self.response.json()        
        value = json_body["data"]["user"][key]
        if value == None:
           value = str(value or "")
        logging.info(f"Return value = {value}")
        return value
    