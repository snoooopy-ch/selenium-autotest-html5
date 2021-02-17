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

class TC051:
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
            qcd.click_add_select_btn(self.driver)
                
            # Data Quality
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 500, -200)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_quality, 1)

            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            qcd.select_rules_tab(self.driver)
            # save
            name_field = self.driver.find_element_by_xpath(qcd.name_xpath)
            name_field.send_keys(Keys.CONTROL + 'a') 
            name_field.send_keys(Keys.DELETE)
            name_field.send_keys('TC_051_ALEX')
            
            qcd.clickAutoSuggestOnDataQuality(self.driver)
            time.sleep(qcd.WAIT5)
            
            try:
                element = WebDriverWait(self.driver, qcd.WAIT100).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div')))
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button')))
                element.click()
                print('initial dialog click');
            except Exception as e:
                pass

            qcd.click_back_execute_log_panel(self.driver)
            
            if self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div[3]/div/div/span[1]/span[1]/input').is_selected():
                print('all checked')
                qcd.uniqueCheckOnDataQuality(self.driver, 8)
                
                # execute
                qcd.save_excute_workflow(self.driver, 'TC_051_ALEX')
            else:
                print('unchecked')

        except Exception as e:
            
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            pass
        except Exception as e:
            raise Exception(e)
            pass
        return
