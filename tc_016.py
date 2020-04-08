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

class TC016:
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
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
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

            qcd.click_notification(driver)

            if (qcd.open_container(driver) != 1):
                input1.click()

            qcd.select_dbset_input(driver, 'AWS_HADOOP')
            qcd.select_db_with_index(driver, 2)
            qcd.select_table(driver, 2)
            qcd.click_add_select_btn(driver)

            # input 2
            qcd.drop_element_to_position(driver, drag_and_drop_js, qcd.input_xpath, 300, 160)
            input2 = driver.find_element_by_xpath('//div[@id="copy-component1"]')

            if (qcd.open_container(driver) != 1):
                input2.click()

            qcd.select_dbset_input(driver, 'sampledb_dest')
            qcd.select_db(driver)
            qcd.select_table(driver, 2)
            qcd.click_add_select_btn(driver)            

            # data compare
            qcd.drop_element_to_position(driver, drag_and_drop_js, qcd.compare_xpath, 700, 80)
            compare1 = driver.find_element_by_xpath('//div[@id="copy-component2"]')

            qcd.connect_elements(driver, input1, 1, compare1, 1)
            qcd.connect_elements(driver, input2, 1, compare1, 1)

            if (qcd.open_container(driver) != 1):
                compare1.click()
                
            qcd.cell_by_cell_compare(driver, 3)
            qcd.select_mapping_tab(driver)

            # custom
            matching_items = driver.find_elements_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/table/tr')
            matching_count = len(matching_items);
            print("TC012: {} items are matched", matching_count);

            # execute
            qcd.save_excute_workflow(driver, 'TC_016_ALEX')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
            pass

    def check_result(self):
        pass