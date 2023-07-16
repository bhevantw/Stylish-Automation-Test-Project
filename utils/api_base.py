#Standard library imports.
import logging
import json

#Related third party imports.


#Local application/library specific imports.  




class APIBase:
    def __init__(self, session, url):
        self.response = None
        self.session = session   
        self.url = url     
        self.response_json = None
        self.token = None

    def api_request(self, method, **kwargs):
        self.response = self.session.request(method, self.url,  **kwargs)
        logging.info(f"Request method={method} url={self.url}")
        json_body = kwargs.get("json", None)
        data_body = kwargs.get("data", None)
        file_body = kwargs.get("files", None)
        logging.info(f'Request Json body: {json.dumps(json_body, indent=4, ensure_ascii=False)}')        
        logging.info(f'Request data body: {json.dumps(data_body, indent=4, ensure_ascii=False)}')    
        logging.info(f'Request file body: {file_body}')   
        logging.info(f'Request headers: {self.session.headers}')
        logging.info(f"Response header={self.response.headers}")
        logging.info(f"Response status={self.response.status_code}")        
        try:
            self.response_json = self.response.json()
            logging.info(f'Response: {json.dumps(self.response_json, indent=4, sort_keys=True, ensure_ascii=False)}')
        except Exception as ex:
            print(f"Get exception {ex}")
        
    def get_status_code(self):
        status_code = self.response.status_code
        logging.info(f"Return status code = {status_code}")
        return status_code

    def get_error_msg(self):
        try:            
            error_msg = self.response_json["errorMsg"]
        except Exception as ex:
            print(ex)
        logging.info(f"Return error = {error_msg}")
        return error_msg
    
    def modify_token(self, token):                
        logging.info(f"Modify token from \n{self.session.headers['Authorization']}\nto\n{token}")
        self.session.headers["Authorization"] = token

    def get_message(self):
        try:
            json_body = self.response.json()        
            msg = json_body["message"]            
            logging.info(f"Return msg = {msg}")
        except:
            logging.info("Exception in getting json message")    
            return None  
        return msg
    

    def get_next_paging(self):
        try:
            json_body = self.response.json() 
            next = json_body['next_paging']
            logging.info(f"Return next paging = {next}")
        except:
            logging.info("Exception in getting json message")
            return None
        return next
        