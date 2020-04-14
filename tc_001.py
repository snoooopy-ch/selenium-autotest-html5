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


class TC001:
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

            self.driver.execute_async_script(load_jquery_js, jquery_url)
                
            with open("js/drag_and_drop.js") as f:
                drag_and_drop_js = f.read()
            
            # input 1
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Input", 300, 0)
            input1 = self.driver.find_element_by_xpath('//div[@id="copy-component0"]')

            if (qcd.open_container(self.driver) != 1):
                input1.click()

            qcd.select_dbset_input(self.driver, 'marketing_dev')
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, 1)
            qcd.select_table(self.driver, 2)
            qcd.select_table(self.driver, 3)
            qcd.click_add_select_btn(self.driver)

            # input 2
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Input", 300, 160)
            input2 = self.driver.find_element_by_xpath('//div[@id="copy-component1"]')

            if (qcd.open_container(self.driver) != 1):
                input2.click()

            qcd.select_dbset_input(self.driver, 'demodb_dest')
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, 1)
            qcd.select_table(self.driver, 2)
            qcd.select_table(self.driver, 3)
            qcd.click_add_select_btn(self.driver)

            # data compare
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Compare", 400, 80)
            compare1 = self.driver.find_element_by_xpath('//div[@id="copy-component2"]')

            qcd.connect_elements(self.driver, input1, 1, compare1, 1)
            qcd.connect_elements(self.driver, input2, 1, compare1, 1)

            if (qcd.open_container(self.driver) != 1):
                compare1.click()
            
            qcd.cell_by_cell_compare(self.driver, 1)

            qcd.select_mapping_tab(self.driver)
            qcd.add_mapping_table_name(self.driver)

            qcd.select_mapping_table_item(self.driver, 1)
            qcd.select_key_for_table_item(self.driver, 1)
            
            qcd.select_mapping_table_item(self.driver, 3)
            qcd.select_key_for_table_item(self.driver, 1)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_001_ALEX')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
            pass

        print('finished')
        time.sleep(qcd.WAIT5)

    def check_result(self):
        try:
            summary_xpath = '/html/body/div[2]/div[3]/div/div/div/div/div[3]/div[1]/div[2]'
            qcd.check_summary_in_final_result(self.driver, self.__class__.__name__, summary_xpath)
            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
            pass