#Standard library imports.
import logging
import requests
import os

#Related third party imports.
from dotenv import dotenv_values

#Local application/library specific imports.  
from utils.api_base import *



class AddProduct(APIBase):

    def __init__(self, session, product_info):
        url = f"{os.getenv('API_URL')}/admin/product"
        super().__init__(session, url)
        self.body = product_info
                
        self.files = []
        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        logging.info(f"current dir = {current_dir}") 
        if product_info['main_image'] != "":                      
            main_image_path = os.path.join(current_dir, f"../test_data/{product_info['main_image']}")  
            main_image_path = os.path.abspath(main_image_path)
            logging.info(f"main image dir = {main_image_path}")
            self.files.append(('main_image', open(main_image_path, 'rb')))            

        for image in product_info['other_images']: 
            if image != "":                
                image_path = os.path.join(current_dir, f"../test_data/{image}")
                image_path = os.path.abspath(image_path)
                logging.info(f"other image dir = {image_path}")
                self.files.append(('other_images', open(image_path, 'rb')))

    def send(self):
        self.api_request("post", data=self.body, files=self.files)

    def get_rsp_product_id(self):
        json_body = self.response.json()    
        try:    
            product_id = json_body['data']["product_id"]       
            logging.info(f"Return product_id = {product_id}")
        except:
            logging.info("Get exception with rsp product id")
            return None
        return product_id