#Standard library imports.
import logging
import requests
import os

#Related third party imports.
from dotenv import dotenv_values

#Local application/library specific imports.  
from utils.api_base import *



class DeleteProduct(APIBase):

    def __init__(self, session, product_id):
        url = f"{os.getenv('API_URL')}/admin/product/{product_id}"
        super().__init__(session, url)                

    def send(self):
        self.api_request("delete")

