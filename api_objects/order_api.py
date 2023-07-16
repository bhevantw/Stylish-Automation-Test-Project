#Standard library imports.
import logging
import os

#Related third party imports.
from dotenv import dotenv_values
from dotenv import load_dotenv

#Local application/library specific imports.  
from utils.api_base import *


class OrderAPI(APIBase):
    def __init__(self, session):
        url = f"{os.getenv('API_URL')}/order"
        super().__init__(session, url)        

    def send(self, method, **kwargs):
        if method == "post":
            payload = kwargs['payload']
            self.api_request("post", json = payload)
        else:
            self.url = self.url+f"/{kwargs['id']}"
            self.api_request("get")
    
    def get_rsp_order_num(self):
        json_body = self.response.json()        
        value = json_body['data']['number']
        logging.info(f"Return order num ={value}")
        return value
        
    def get_rsp_order(self):
        return self.response.json()['data']['details']   