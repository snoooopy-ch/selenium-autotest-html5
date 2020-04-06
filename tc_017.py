# -*- coding: cp932 -*-

import time
import sys
import tc_common as qcd
import requests
import lxml.html
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

class TC017:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_workspace()
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
            pass

    def open_workspace(self):
        try:
            # open
            if (qcd.open_workspace(self.driver) != 1):
                raise Exception('fail to open workspace')
        except Exception as e:
            logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
            pass

    def workflow(self):
        try:
            # load jQuery
            jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"
            with open("js/jquery_load_helper.js") as f:
                load_jquery_js = f.read()

            driver.execute_async_script(load_jquery_js, jquery_url)
                
            with open("js/drag_and_drop.js") as f:
                drag_and_drop_js = f.read()
            
            # input 1
            qcd.drop_element_to_position(driver, drag_and_drop_js, qcd.input_xpath, 300, 0)
            input1 = driver.find_element_by_xpath('//div[@id="copy-component0"]')

            if (qcd.open_container(driver) != 1):
                input1.click()

            qcd.select_dbset_input(driver, 'marketing_dev')
            qcd.select_db(driver)
            qcd.select_table(driver, 4)
            qcd.select_table(driver, 9)
            qcd.select_table(driver, 11)
            qcd.click_add_select_btn(driver)

            # Data Quality
            qcd.drop_element_to_position(driver, drag_and_drop_js, qcd.data_quality_xpath, 500, -300)
            data_quality = driver.find_element_by_xpath('//div[@id="copy-component1"]');
            qcd.connect_elements(driver, input1, 1, data_quality, 1)

            if (qcd.open_container(driver) != 1):
                data_quality.click()

            qcd.add_sql_on_dataquality(driver, 13, "SELECT Patient_name,Patient_blood_group,diagnosis_session, Patient_healthcard_no FROM Patient WHERE Patient_healthcard_no BETWEEN 47 AND 48 LIMIT 49", "job1")
            qcd.add_sql_on_dataquality(driver, 13, "SELECT doc_name,Specialization FROM Doctor WHERE Specialization LIKE '%y'", "job2")
            qcd.add_sql_on_dataquality(driver, 13, "Select doc_name,Specialization From Doctor ORDER BY doc_name", "job3")
            qcd.add_sql_on_dataquality(driver, 13, "SELECT COUNT(DISTINCT active) FROM Insurance", "job3")

            # execute
            qcd.save_excute_workflow(driver, 'TC_017_ALEX')
            
        except Exception as e:
            logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
            pass

    def check_result(self):
        pass