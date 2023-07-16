#Standard library imports.
import logging
import os

#Related third party imports.

from dotenv import dotenv_values
from dotenv import load_dotenv


#Local application/library specific imports.  
from utils.api_base import *


class DetailsAPI(APIBase):
    def __init__(self, session, id):
        url = f"{os.getenv('API_URL')}/products/details?id={id}"
        super().__init__(session, url)
    
    def send(self):
        self.api_request("get")

    def get_rsp_product(self):
        json_body = self.response.json()        
        product_list = json_body["data"]       
        logging.info(product_list)
        return product_list 