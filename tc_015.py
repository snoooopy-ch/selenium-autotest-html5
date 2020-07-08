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

class TC015:
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

            qcd.select_dbset_input(self.driver, 'marketing_dev')
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, "City")
            qcd.select_table(self.driver, "Claims")
            qcd.select_table(self.driver, "Diagnosis")
            qcd.select_table(self.driver, "History")
            qcd.select_table(self.driver, "H_Ins_Staff")
            qcd.click_add_select_btn(self.driver)

            # data profile
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Profile", 400, -160)
            data_profile = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_profile, 1)

            if (qcd.open_container(self.driver) != 1):
                data_profile.click()

            
            # custom
            selected = self.driver.find_elements_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div')
            for item in selected:
                print("TC015: {0} table are selected", item.text)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_015_ALEX')

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[1]/div/div/div[1]').click()
        time.sleep(qcd.WAIT1)
        count_tr = self.driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[1]/div/div[2]/div/div')
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[1]/div/div/div[1]').click()

        for tr in range(0, len(count_tr)):
            self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[1]/div/div/div[1]').click()
            time.sleep(qcd.WAIT1)
            table_tr = self.driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[1]/div/div[2]/div/div')
            table_tr[tr].click()
            time.sleep(qcd.WAIT1)

            attribute_tr = self.driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[2]/div/div[1]/div[5]/div')
            for attr_tr in attribute_tr:
                attr_tr.find_element_by_xpath('./div/div')
                attr_tr.click()
                time.sleep(qcd.WAIT3)
        pass