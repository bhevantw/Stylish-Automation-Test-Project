#Standard library imports.
import logging
import requests
import os

#Related third party imports.
from dotenv import dotenv_values

#Local application/library specific imports.  
from utils.api_base import *


class CategoryAPI(APIBase):
    def __init__(self, session, category, paging):
        url = f"{os.getenv('API_URL')}/products/{category}?paging={paging}"
        super().__init__(session, url)
    
    def send(self):
        self.api_request("get")

    def get_rsp_product(self):
        json_body = self.response.json()        
        product_list = json_body["data"]       
        return product_list 