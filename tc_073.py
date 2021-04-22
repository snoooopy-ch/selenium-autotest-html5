# -*- coding: cp932 -*-

import time
import sys
import tc_common as qcd
import os
import subprocess
import traceback
import logging
import re

from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as selExceptions
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

class TC073:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_workspace()
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def open_workspace(self):
        try:
            # open
            if (qcd.open_workspace(self.driver) != 1):
                raise Exception('fail to open workspace')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def workflow(self):
        try:
            # load jQuery
            jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"
            with open("js/jquery_load_helper.js") as f:
                load_jquery_js = f.read()

            self.driver.execute_async_script(load_jquery_js, jquery_url)
                
            with open("js/drag_and_drop.js") as f:
                drag_and_drop_js = f.read()
            
            # input 1
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Source", 300, 0)
            input1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))

            if (qcd.open_container(self.driver) != 1):
                input1.click()
                
            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_api_input(self.driver)
            
            python_code = """
            
import requests
import json

 
API_KEY = "d25a07df6199416b87816551ebf80b0744c50b8c2fa385909c0820cfde80a3c5"
PDL_VERSION = "v5"
PDL_URL = "https://dataq-testing-data.s3.amazonaws.com/conversation.json"
 
 
params = {
   "api_key": API_KEY,
   "name": ["sean thorne"],
   "company": ["peopledatalabs.com"]
}
 
json_response = requests.get(PDL_URL, params=params).json()
json_text = json.dumps(json_response)
f = open("/tmp/dq_output_file_name.json", "w")
f.write(json_text)
f.close()   """
            
            qcd.add_python_code_api_input(self.driver, python_code)

            element = self.driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/div/div[2]/label/span[1]/input')
                                                         
            absolute_file_path = os.path.abspath("files/conversation_073.json")
            element.send_keys(absolute_file_path)
            time.sleep(qcd.WAIT1)
            
            qcd.check_flatten_data(self.driver)
            # qcd.add_columns_api_input(self.driver, "data_education_school_type, dataset_version")
            qcd.click_validate_api_input(self.driver)
            
            try:
                element = WebDriverWait(self.driver, qcd.WAIT50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div')))
                time.sleep(qcd.WAIT3)
                element = WebDriverWait(self.driver, qcd.WAIT3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="client-snackbar"]')))
                text = re.compile(r'<[^>]+>').sub('', element.text)
                print(text)
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button')))
                element.click()
            except Exception as e:
                raise Exception('Input1 Validate fails')
            
            qcd.click_datatab_input(self.driver)
            
            
            # Data Quality
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 600, -300)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_quality, 1)
            
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()
                
            qcd.select_rules_tab(self.driver)
            qcd.inputMinValueOnDataQuality(self.driver, 1, 1)
            qcd.inputMaxValueOnDataQuality(self.driver, 1, 10)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_073_Morimura')
            
            detail_span_xpath = '/html/body/div[2]/div[3]/div/div/div/div/div[1]/span[2]'
            try:
                if qcd.isElementPresentForResult(self.driver, detail_span_xpath) != True:
                    raise Exception()
                
                detail_span = self.driver.find_elements_by_xpath(detail_span_xpath)
                if (len(detail_span) == 1):
                    detail_span[0].click()
                    time.sleep(qcd.WAIT3)
            except Exception as e:
                print(e)
                raise Exception(e)
                pass
            
            try:
                records = self.driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[4]/div[1]/div[2]/div')
                    
                for record in records:
                    innerRecord = record.find_element_by_xpath('./div')
                    recordClass = innerRecord.get_attribute("class")
                    
                    columns = innerRecord.find_elements_by_xpath('./div')
                    if recordClass.find('-padRow') == -1:
                        print("Table:{}, Column:{}, Status:{}".format(columns[0].text, columns[1].text, columns[5].text))
                    else:
                        break
            except Exception as e:
                qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
                raise Exception(e)
                pass

            qcd.click_result_close(self.driver)
            qcd.click_action_on_first_flow(self.driver, 1)
            
            self.driver.find_element_by_xpath('//*[@id="drop-location"]/*[name()="svg"]/following-sibling::img').click()
                    
            # Column Type
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Column type", 400, -150)
            
            column_type = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))
            input1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            
            qcd.remove_connection_between(self.driver, input1, data_quality)
            
            if (qcd.open_container(self.driver) != 1):
                column_type.click()
                
            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_select_first_tableitem_for_select_columns(self.driver)
            
            qcd.select_table(self.driver, "id")
            qcd.select_table(self.driver, "title")
            
            qcd.select_item_from_column_data_type_list(self.driver, 1, 9)
            qcd.select_item_from_column_data_type_list(self.driver, 2, 1)
            
            qcd.click_save_on_cp(self.driver)
                
            qcd.remove_connection_between(self.driver, column_type, data_quality)
            
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()
            
            qcd.select_rules_tab(self.driver)
            qcd.check_completeness_on_dataqualityheader(self.driver)
            qcd.check_nullcheck_on_dataqualityheader(self.driver)
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_073_Morimura')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
                
    def check_result(self):
        detail_span_xpath = '/html/body/div[2]/div[3]/div/div/div/div/div[1]/span[2]'
        try:
            if qcd.isElementPresentForResult(self.driver, detail_span_xpath) != True:
                raise Exception()
            
            detail_span = self.driver.find_elements_by_xpath(detail_span_xpath)
            if (len(detail_span) == 1):
                detail_span[0].click()
                time.sleep(qcd.WAIT3)
        except Exception as e:
            print(e)
            raise Exception(e)
            pass
        
        try:
            records = self.driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[4]/div[1]/div[2]/div')
                
            for record in records:
                innerRecord = record.find_element_by_xpath('./div')
                recordClass = innerRecord.get_attribute("class")
                
                columns = innerRecord.find_elements_by_xpath('./div')
                if recordClass.find('-padRow') == -1:
                    print("Table:{}, Column:{}, Status:{}".format(columns[0].text, columns[1].text, columns[5].text))
                else:
                    break
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
        return