# -*- coding: cp932 -*-

import time
import sys
import tc_common as qcd
import os
import subprocess
import traceback
import logging

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

class TC037:
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
                
            qcd.click_manual_upload_input(self.driver)
            qcd.select_manual_upload_dataset_format(self.driver, 3)
            
            absolute_file_path = os.path.abspath("files/dp_resck_037.json")
            qcd.set_dataset_path(self.driver, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/label/span[1]/input', absolute_file_path)
            time.sleep(qcd.WAIT3)
            qcd.click_manual_upload_validate(self.driver, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div[1]/button')
            
            try:
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div')))
                time.sleep(qcd.WAIT3)
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button')))
                element.click()
            except Exception as e:
                raise Exception('Input1 Validate fails')
            
            # Data Quality
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 500, -200)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_quality, 1)

            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            qcd.nullCheckOnDataQuality(self.driver, 2)
            
            qcd.nullCheckOnDataQuality(self.driver, 3)
            qcd.checkCompletenessOnDataQuality(self.driver, 3)
            qcd.checkLeftSpacesOnDataQuality(self.driver, 3)
            qcd.checkRightSpacesOnDataQuality(self.driver, 3)
            
            qcd.nullCheckOnDataQuality(self.driver, 4)
            
            qcd.nullCheckOnDataQuality(self.driver, 5)
            qcd.checkCompletenessOnDataQuality(self.driver, 5)
            qcd.checkLeftSpacesOnDataQuality(self.driver, 5)
            qcd.checkRightSpacesOnDataQuality(self.driver, 5)
            
            qcd.nullCheckOnDataQuality(self.driver, 6)
            qcd.checkCompletenessOnDataQuality(self.driver, 6)
            qcd.checkLeftSpacesOnDataQuality(self.driver, 6)
            qcd.checkRightSpacesOnDataQuality(self.driver, 6)
            
            qcd.nullCheckOnDataQuality(self.driver, 7)
            
            qcd.nullCheckOnDataQuality(self.driver, 8)
            
            qcd.nullCheckOnDataQuality(self.driver, 9)
            
            qcd.nullCheckOnDataQuality(self.driver, 10)
            qcd.checkCompletenessOnDataQuality(self.driver, 10)
            qcd.checkLeftSpacesOnDataQuality(self.driver, 10)
            qcd.checkRightSpacesOnDataQuality(self.driver, 10)
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_037_ALEX')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            print(1)
        except Exception as e:
            raise Exception(e)
            pass
        return
