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

class TC070:
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
                
            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_sql_input(self.driver)
            qcd.select_dbset_sql_input(self.driver, 'hims')
            qcd.select_db_sql(self.driver)
            qcd.add_sql_title_content(self.driver, 'courses_info', "select upper(Courses) as Courses from courses_info")
            
            try:
                element = WebDriverWait(self.driver, qcd.WAIT50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div')))
                time.sleep(qcd.WAIT3)
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button')))
                element.click()
            except Exception as e:
                raise Exception('Input1 Validate fails')
            
            if (qcd.open_container(self.driver) == 1):
                input1.click()
            
            # Output 2
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Output", 500, -250)
            output = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, output, 1)

            if (qcd.open_container(self.driver) != 1):
                output.click()
                
            qcd.click_maximize_for_select_columns(self.driver)
            qcd.select_dbset_output(self.driver, 'test_db')
            qcd.select_db_output(self.driver)
            
            qcd.add_output_table_or(self.driver, 'courses_info', 'Course_Name')
            qcd.add_output_table_or(self.driver, 'courses_info', 'test_table')
            qcd.click_output_overwrite(self.driver, 2)
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_070_ALEX')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            records = self.driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[4]/div[1]/div[2]/div')
                
            for record in records:
                innerRecord = record.find_element_by_xpath('./div')
                recordClass = innerRecord.get_attribute("class")
                
                columns = innerRecord.find_elements_by_xpath('./div')
                if recordClass.find('-padRow') == -1:
                    print("Src Table:{}, Dest Table:{}, Match:{}".format(columns[0].text, columns[1].text, columns[2].find_element_by_xpath('./img').get_attribute('alt')))
                else:
                    break
            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
        return
