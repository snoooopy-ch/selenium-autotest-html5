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

class TC022:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_dashboard()
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def open_dashboard(self):
        try:
            # open
            if (qcd.open_dashboard(self.driver) != 1):
                raise Exception('fail to open dashboard')
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

            qcd.open_settings(self.driver)
            
            qcd.search_in_settings(self.driver, "employee_demo")
            qcd.click_delete_settings_search(self.driver)
            qcd.add_new_connection(self.driver, 6, 'employee_demo', 'jdbc:mysql://54.86.47.129:3306/employee?useUnicode=true& useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC', 'demouser1', 'demopassword')
            
            qcd.open_dashboard(self.driver)
            qcd.clickFirstViewEditActionOnExcutions(self.driver)

            input1 = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))
            if (qcd.open_container(self.driver) != 1):
                input1.click()

            time.sleep(qcd.WAIT5)
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        print(self.__class__.__name__ + ' result:')
        try:
            qcd.open_config_tab_on_input(self.driver)
    
            element = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]')))
            element.click()

            time.sleep(qcd.WAIT1)
            db_value = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div')))
            items = db_value.find_elements_by_xpath('./div')
            
            flag = 0
            for item in items:
                if (item.text == 'employee_demo'):
                    print("employee_demo exist")
                    flag = 1
                    break
            
            if (flag == 0):
                print("employee_demo unexist")    

        except NoSuchElementException:
            print("employee_demo unexist")
            raise Exception(e)
