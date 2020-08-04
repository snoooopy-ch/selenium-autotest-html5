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


class TC026:
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
            qcd.select_table(self.driver, "courses_info")
            qcd.click_add_select_btn(self.driver)
            
            # data profile
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Profile", 500, -160)
            data_profile = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_profile, 1)

            # execute
            qcd.save_excute_workflow(self.driver, 'Clone_Edit_Delete')

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

        print('finished')

    def check_result(self):
        try:
            qcd.click_result_close(self.driver)
            
            dateTimeObj = datetime.now()
            timestamp = str(dateTimeObj.microsecond)
            # Clone
            qcd.click_action_on_flow_page(self.driver)
            qcd.find_specific_flow(self.driver, "Clone_Edit_Delete")
            qcd.click_action_on_first_flow(self.driver, 2)
            element = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/input')))
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.DELETE)
            element.send_keys(timestamp + "_cloned")
            element = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[3]/div[1]')))
            element.click()
            time.sleep(qcd.WAIT10)
            
            # Edit
            qcd.click_action_on_first_flow(self.driver, 1)
            input1 = self.driver.find_element_by_xpath('//div[@id="copy-component0"]')
            print('Input is copied')
            data_profile = self.driver.find_element_by_xpath('//div[@id="copy-component1"]')
            print('DataProfile is copied')
            
            # Rename
            qcd.click_action_on_flow_page(self.driver)
            qcd.find_specific_flow(self.driver, "Clone_Edit_Delete")
            qcd.click_action_on_first_flow(self.driver, 4)
            element = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/input')))
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.DELETE)
            element.send_keys(timestamp + "_Modified_Flow")
            element = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[3]/div[1]')))
            element.click()
            time.sleep(qcd.WAIT5)
            
            # Check
            qcd.find_specific_flow(self.driver, timestamp + "_Modified_Flow")
            element = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/span')))
            if (element.text == (timestamp + '_Modified_Flow')):
                print('Renamed to Modified_flow')
            else:
                print('Unrenamed to Modified_flow')
            
            # Delete
            qcd.click_action_on_flow_page(self.driver)
            qcd.find_specific_flow(self.driver, timestamp + "_cloned")
            qcd.click_action_on_first_flow(self.driver, 3)
            time.sleep(qcd.WAIT5)
            
            # Check
            qcd.find_specific_flow(self.driver, timestamp + "_cloned")
            element = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/span')))
            if (element.text == (timestamp + '_cloned')):
                print('TC026_cloned is UnDeleted')
            else:
                print('TC026_cloned is Deleted')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass