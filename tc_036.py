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

class TC036:
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
            time.sleep(qcd.WAIT1)
            qcd.onUploadJsonFlowFile(self.driver, "Import_Flow_036.json")
            qcd.click_action_on_first_flow(self.driver, 1)
            
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
                
            # execute
            qcd.save_excute_workflow_without_rename(self.driver)

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        qcd.click_result_close(self.driver)
        
        time.sleep(qcd.WAIT5)
        qcd.open_excutions(self.driver)
        
        qcd.clickFirstViewEditActionOnExcutions(self.driver)
        
        input1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))

        if (qcd.open_container(self.driver) != 1):
            input1.click()
        qcd.click_maximize_for_select_columns(self.driver)
            
        qcd.select_table(self.driver, "courses_info")
        qcd.select_table(self.driver, "Student_Information")
        qcd.select_table(self.driver, "medicine_students_finalreport")
        
        qcd.click_add_select_btn(self.driver)
        
        qcd.save_excute_workflow_without_rename(self.driver)