#Standard library imports.
import logging
import os

#Related third party imports.

from dotenv import dotenv_values
from dotenv import load_dotenv


#Local application/library specific imports.  
from utils.api_base import *

class ProfileAPI(APIBase):

    def __init__(self, session):
        url = f"{os.getenv('API_URL')}/user/profile"
        super().__init__(session, url)

    def send(self):        
        self.api_request("get")
        logging.info(f"Send profile API")

    def get_rsp_data(self, key):
        json_body = self.response.json()        
        value = json_body['data'][key]
        if value == None:
           value = ""
        logging.info(f"Return data={value}")
        return value

    
    

