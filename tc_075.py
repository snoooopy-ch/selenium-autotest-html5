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

class TC075:
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
            
            qcd.click_notification(self.driver)
            qcd.select_cluster_execute_job(self.driver, "AWS_HADOOP")
            qcd.save_close_execute_tab(self.driver)

            if (qcd.open_container(self.driver) != 1):
                input1.click()

            qcd.select_dbset_input(self.driver, 'AWS_HADOOP')
            qcd.select_db_with_index(self.driver, 'userdb')
            qcd.click_all_select(self.driver)
            qcd.click_add_select_btn(self.driver)
            
            time.sleep(20)

            # select columns
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Select Columns", 500, -50)
            selectcolumn = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))

            qcd.connect_elements(self.driver, input1, 1, selectcolumn, 1)

            if (qcd.open_container(self.driver) != 1):
                selectcolumn.click()
            
            qcd.click_select_tableitem_for_select_columns(self.driver, "city")
            qcd.select_table(self.driver, "composition")
            qcd.click_save_on_cp(self.driver)
            
            # Column type
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Column type", 500, -100)
            columntype = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))

            qcd.connect_elements(self.driver, selectcolumn, 2, columntype, 1)

            if (qcd.open_container(self.driver) != 1):
                columntype.click()

            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_select_tableitem_for_select_columns(self.driver, "city")
            qcd.select_table(self.driver, "m_name")
            qcd.select_item_from_column_data_type_list(self.driver, 1, 1)
            qcd.click_save_on_cp(self.driver)
            
            # Data Quality
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 900, -300)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component3"]')))
            qcd.connect_elements(self.driver, columntype, 2, data_quality, 1)
            
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            qcd.select_rules_tab(self.driver)
            qcd.select_rule_on_dataquality(self.driver, 4)
            qcd.check_leftspaces_on_dataqualityheader(self.driver)
            qcd.check_rightspaces_on_dataqualityheader(self.driver)
            qcd.nullCheckOnDataQuality(self.driver, 3)
            qcd.uniqueCheckOnDataQuality(self.driver, 3)
            qcd.inputMaxValueOnDataQuality(self.driver, 5, 1)
            qcd.inputMinValueOnDataQuality(self.driver, 5, 100)
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_075_ALEX')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

        print('finished')

    def check_result(self):
        try:
            qcd.check_summary_in_final_result(self.driver, self.__class__.__name__, qcd.normal_result_summary_xpath)
            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass