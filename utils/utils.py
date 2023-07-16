#Standard library imports.
import logging
import os


def print_function_info(func):
    # print the function info when entering and exiting
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        module_name = func.__module__
        # logging.debug(f"=> {module_name}.{function_name}")
        result = func(*args, **kwargs)
        # logging.debug(f"<= {module_name}.{function_name}")
        return result
    return wrapper

def compare_two_dicts(dict1, dict2, key_list):
    try:
        for key in key_list:
          assert dict1[key] == dict2[key]
    except:
        print(f"Get exception in {key}")
        return False
    return True