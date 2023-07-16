#Standard library imports.
import logging
import os.path

#Related third party imports.
from allure_commons.types import AttachmentType
import allure
import pandas as pd

#Local application/library specific imports.   


@allure.step("TestDataFromExcel.get_data_dict")
def get_data(sheet_name):    
    filename = 'Stylish_TestCase.xlsx'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '../test_data', filename)
    df = pd.read_excel(data_path, sheet_name=f"{sheet_name}", dtype=str)        
    df = df.fillna("")    
    raw_data = df.to_dict(orient='records')
    result = []
    for row in raw_data:           
        result.append(modify_data(row))    
    logging.info(f"Get data from excel\n{result}")
    return result

def modify_data(data_row):  
    result = {}        
    for key,value in data_row.items():            
        if " chars" in value:            
           result[key] = int(value.replace(" chars","")) * 'f' 
        else:          
           result[key] = value
    return result


# list = get_data("Create Product Success")
# for x,y in enumerate(list):
#     print(f"key={x}\n{y}")
# get_data("Create Product Success")