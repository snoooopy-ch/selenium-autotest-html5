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

class TC024:
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
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Input", 300, 0)
            input1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))

            qcd.click_notification(self.driver)
            qcd.select_cluster_execute_job(self.driver, "AWS_HADOOP")
            qcd.save_close_execute_tab(self.driver)

            if (qcd.open_container(self.driver) != 1):
                input1.click()
                
            qcd.click_file_upload_input(self.driver)
            qcd.select_manual_upload_dataset_format(self.driver, 'JSON')
            qcd.set_dataset_path(self.driver, qcd.input_manualupload_dataset_xpath, '/tmp/sale_details.json')
            qcd.check_multiline_manual_upload_input_with_awshadoop(self.driver, "true")
            qcd.click_manual_upload_validate(self.driver, '/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/button')
            
            try:
                element = WebDriverWait(self.driver, qcd.WAIT50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div')))
                time.sleep(qcd.WAIT3)
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button')))
                element.click()
            except Exception as e:
                raise Exception('Input1 Validate fails')
            
            # input 2
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Input", 300, 160)
            input2 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))

            if (qcd.open_container(self.driver) != 1):
                input2.click()
                
            qcd.click_file_upload_input(self.driver)
            qcd.select_manual_upload_dataset_format(self.driver, 'JSON')
            qcd.set_dataset_path(self.driver, qcd.input_manualupload_dataset_xpath, '/tmp/sale_details.json')
            qcd.check_multiline_manual_upload_input_with_awshadoop(self.driver, "true")
            qcd.click_manual_upload_validate(self.driver, '/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/button')
            
            try:
                element = WebDriverWait(self.driver, qcd.WAIT50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div')))
                time.sleep(qcd.WAIT3)
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button')))
                element.click()
            except Exception as e:
                raise Exception('Input2 Validate fails')
            
            # data compare
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Compare", 700, 80)
            compare1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))

            qcd.connect_elements(self.driver, input1, 1, compare1, 1)
            qcd.connect_elements(self.driver, input2, 1, compare1, 1)

            if (qcd.open_container(self.driver) != 1):
                compare1.click()
                
            qcd.select_datacompare_type(self.driver, 1)
            qcd.select_mapping_tab(self.driver)
            qcd.select_mapping_table_item(self.driver, 1)
            qcd.select_key_for_table_item(self.driver, 1)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_024_ALEX')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            qcd.click_share_button_and_close(self.driver)
            qcd.click_result_close(self.driver)
            element = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[8]/div/div')))
            print(1)
            html = element.get_attribute('innerHTML')
            html = re.compile(r'<[^>]+>').sub('', html)
            print("metric percentage = " + str(html))
            print(2)
        except Exception as e:
            raise Exception(e)
            pass
        return
