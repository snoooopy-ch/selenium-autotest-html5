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

class TC052:
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

            if (qcd.open_container(self.driver) != 1):
                input1.click()

            qcd.select_dbset_input(self.driver, 'tims')
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, "assessment_report")
            qcd.click_add_select_btn(self.driver)

            # data profile
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Profile", 400, -160)
            data_profile = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_profile, 1)

            if (qcd.open_container(self.driver) != 1):
                data_profile.click()
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_052_ALEX')

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        table = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[2]')
        table_trs = table.find_elements_by_xpath('./div')
        
        for tr in table_trs:
            tr_body = tr.find_element_by_xpath('./div')
            
            tr_name_tmp = tr_body.find_element_by_xpath('./div[1]/div/div/div/div').get_attribute('innerHTML')
            tr_name = re.compile(r'<[^>]+>').sub('', tr_name_tmp)
            
            if "physical_Diagnosis_no_data" in tr_name:
                tr_min = tr_body.find_element_by_xpath('./div[5]').text
                tr_max = tr_body.find_element_by_xpath('./div[6]').text
                print("Min is :".format(tr_min if tr_min  else 'NA'))
                print("Max is :".format(tr_max if tr_max  else 'NA'))
                break
        
        pass
        
        