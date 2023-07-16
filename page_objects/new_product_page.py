#Standard library imports.
import logging
import time
import os

#Related third party imports.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure

#Local application/library specific imports.  
from utils.page_base import *
from utils.page_header import *
from utils.utils import print_function_info


class NewProductPage(PageBase,PageHeader):

    categoty_option = (By.XPATH, "//select[@name='category']")
    title_input = (By.XPATH, "//input[@name='title']")
    desc_textarea = (By.XPATH, "//textarea[@name='description']")
    price_input = (By.XPATH, "//input[@name='price']")
    texture_input = (By.XPATH, "//input[@name='texture']")
    wash_input = (By.XPATH, "//input[@name='wash']")
    place_input = (By.XPATH, "//input[@name='place']")
    note_input = (By.XPATH, "//input[@name='note']")    
    all_colors_input = (By.XPATH, "//input[@name='color_ids']")
    all_sizes_input = (By.XPATH, "//input[@name='sizes']")
    story_input = (By.XPATH, "//input[@name='story']")
    main_image_input = (By.XPATH, "//input[@name='main_image']")
    other_image1_input = (By.XPATH, "//input[@name='main_image']/following-sibling::input[1]")
    other_image2_input = (By.XPATH, "//input[@name='main_image']/following-sibling::input[2]")
    create_product_btn = (By.XPATH, "//input[@value='Create']")
        
    def get_size_input(self, size):
        return (By.XPATH, f"//input[@value='{size}']")

    def get_color_input(self, color):
        return (By.XPATH, f"//label[text()=' {color} ']/preceding-sibling::input")

    def __init__(self, driver):
        super().__init__(driver)
        driver.get(f"{os.getenv('WEB_DOMAIN')}/admin/product_create.html")        

    def create_new_product(self, data_row):
        category = data_row['Category']
        title = data_row['Title']
        desc = data_row['Description']
        price = data_row['Price']
        texture = data_row['Texture']
        wash = data_row['Wash']
        place = data_row['Place of Product']
        note = data_row['Note']
        colors = data_row['Colors']
        sizes = data_row['Sizes']
        story = data_row['Story']
        main_image = data_row['Main Image']
        other_image1 = data_row['Other Image 1']
        other_image2 = data_row['Other Image 2']
        logging.info(data_row)
        
        #Select category
        self.set_option(self.categoty_option, category)

        #Fill title
        self.input(self.title_input, title)

        #Fill description
        self.input(self.desc_textarea, desc)

        #Fill price
        self.input(self.price_input, price)

        #Fill texture
        self.input(self.texture_input, texture)

        #Fill wash
        self.input(self.wash_input, wash)

        #Fill place
        self.input(self.place_input, place)

        #Fill note
        self.input(self.note_input, note)

        #Select colors        
        if colors != '':
           color_list = colors.split(',')
           for c in color_list:
              if c != "全選":
                locator = self.get_color_input(c.strip())
                self.find_element(locator, True).click() 
              else:
                all_colors_inputs = self.find_elements(self.all_colors_input)
                for elem in all_colors_inputs:
                    elem.click()
        
        #Select sizes        
        if sizes != '':
           size_list = sizes.split(',')
           for s in size_list:
              if s != "全選":
               locator =  self.get_size_input(s.strip())
               self.find_element(locator, True).click() 
              else:
                all_size_inputs = self.find_elements(self.all_sizes_input)    
                for elem in all_size_inputs:
                    elem.click()
            
        #Fill story
        self.input(self.story_input, story)

        current_dir = os.path.dirname(os.path.abspath(__file__))   
        #Upload main image
        if main_image != '':                                          
           main_image_path = os.path.join(current_dir, "mainImage.jpg")                             
           file_upload2 = self.find_element(self.main_image_input, True)
           file_upload2.send_keys(main_image_path)
           logging.info(f"Main image file path = {main_image_path}")

        #Upload other image1        
        if other_image1 != '':                           
           other_image1_path = os.path.join(current_dir, "otherImage0.jpg")                             
           file_upload2 = self.find_element(self.other_image1_input, True)
           file_upload2.send_keys(other_image1_path)
           logging.info(f"Other image1 file path = {other_image1_path}")

        #Upload other image2
        if other_image2 != '':   
           other_image2_path = os.path.join(current_dir, "otherImage1.jpg")  
           file_upload3 = self.find_element(self.other_image2_input, True)
           file_upload3.send_keys(other_image2_path)
           logging.info(f"Other image2 file path = {other_image2_path}")

        #Click create button
        self.find_element(self.create_product_btn, True).click()
        logging.info(f"Product [{title}] is created")

