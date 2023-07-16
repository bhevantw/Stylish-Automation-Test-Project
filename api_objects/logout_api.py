#Standard library imports.
import logging
import requests
import os

#Related third party imports.

from dotenv import dotenv_values
from dotenv import load_dotenv


#Local application/library specific imports.  
from utils.api_base import *


class LogoutAPI(APIBase):

    def __init__(self, session):
        url = f"{os.getenv('API_URL')}/user/logout"
        super().__init__(session, url)

    def send(self):                
        self.api_request("post")

    