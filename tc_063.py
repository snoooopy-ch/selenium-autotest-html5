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

class TC063:
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
            code = """
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
f.close()
            """
            qcd.add_python_code_api_input(self.driver, code)
            
            element = self.driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/div/div[2]/label/span[1]/input')
            absolute_file_path = os.path.abspath("files/sample_063.json")
            element.send_keys(absolute_file_path)
            
            self.driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div[3]/div/div/div/div/div/div/div[5]/div/div[2]/span/span[1]').click()
            time.sleep(qcd.WAIT3)
            qcd.click_validate_api_input(self.driver)
            
            try:
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div')))
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="client-snackbar"]')))
                text = re.compile(r'<[^>]+>').sub('', element.text)
                print(text)
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button')))
                element.click()
            except Exception as e:
                print("Validate failed")
                
            qcd.close_maximize_for_select_columns(self.driver)
            time.sleep(qcd.WAIT1)
                
            # Data Profile
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Profile", 600, -250)
            data_profile = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_profile, 1)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_063_Morimura')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            summary_table = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div[1]/div[2]')
            table_trs = summary_table.find_elements_by_xpath('./div')

            flag = 0
            try:
                for tr in table_trs:
                    inner_tr = tr.find_element_by_xpath('./div')
                    tds = inner_tr.find_elements_by_xpath('./div')

                    output = ''
                    find = 0
                    print("Count:{}, Min:{}, Max{}".format(tds[1].text, tds[4].text, tds[5].text))
            except Exception as ex:
                print(ex)
                pass

            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
        return
