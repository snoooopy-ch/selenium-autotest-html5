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

class TC062:
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
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Source", 300, 0)
            input1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))

            if (qcd.open_container(self.driver) != 1):
                input1.click()
                
            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_sql_input(self.driver)
            qcd.select_dbset_sql_input(self.driver, 'marketing_dev')
            qcd.select_db_sql(self.driver)
            qcd.add_sql_title_content(self.driver, 'sqlPaintent', "select Patient_name from Patient WHERE Patient_status='Paid'")
            
            try:
                element = WebDriverWait(self.driver, qcd.WAIT50).until(EC.visibility_of_element_located((By.XPATH, qcd.alert_body_xpath)))
                time.sleep(qcd.WAIT3)
                element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, qcd.alert_button_xpath)))
                element.click()
            except Exception as e:
                raise Exception('Input1 Validate fails')
            
            if (qcd.open_container(self.driver) == 1):
                input1.click()
                
            # Data Profile
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Profile", 600, -250)
            data_profile = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_profile, 1)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_062_Morimura')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            summary_table = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div[1]/div[2]')
            table_trs = summary_table.find_elements_by_xpath('./div')

            flag = 0
            try:
                for tr in table_trs:
                    inner_tr = tr.find_element_by_xpath('./div')
                    tds = inner_tr.find_elements_by_xpath('./div')

                    output = ''
                    find = 0
                    print("Count:{}, Min:{}, Max:{}".format(tds[1].text, tds[4].text, tds[5].text))
            except Exception as ex:
                print(ex)
                pass

            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
        return
