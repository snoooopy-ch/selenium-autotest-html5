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

class TC078:
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
            
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Input", 300, 0)
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Select Columns", 500, -80)
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Column type", 500, -150)
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 700, -200)
            
            input1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))
            selectcolumns = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            commontype = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component3"]')))
            
            qcd.connect_elements(self.driver, input1, 1, selectcolumns, 1)
            qcd.connect_elements(self.driver, selectcolumns, 2, commontype, 1)
            qcd.connect_elements(self.driver, commontype, 2, data_quality, 1)
            
            # input 1
            if (qcd.open_container(self.driver) != 1):
                input1.click()
                
            qcd.select_dbset_input(self.driver, 'marketing_dev')
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, "City")
            qcd.click_add_select_btn(self.driver)
            
            if (qcd.open_container(self.driver) == 1):
                input1.click()
            
            # select columns
            if (qcd.open_container(self.driver) != 1):
                selectcolumns.click()

            qcd.click_select_tableitem_for_select_columns(self.driver, "City")
            qcd.select_table(self.driver, "city_name")
            qcd.click_save_on_cp(self.driver)
            
            if (qcd.open_container(self.driver) == 1):
                selectcolumns.click()
            
            # Column type
            if (qcd.open_container(self.driver) != 1):
                commontype.click()

            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_select_tableitem_for_select_columns(self.driver, "City")
            qcd.click_select_all_for_commontype(self.driver)
            qcd.select_item_from_column_data_type_list(self.driver, 1, 1)
            qcd.select_item_from_column_data_type_list(self.driver, 2, 9)
            qcd.click_save_on_cp(self.driver)
            
            qcd.close_maximize_for_select_columns(self.driver)
            
            if (qcd.open_container(self.driver) == 1):
                commontype.click()
                
            # Data Quality
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            qcd.check_completeness_on_dataqualityheader(self.driver)
            qcd.check_nullcheck_on_dataqualityheader(self.driver)
            qcd.check_leftspaces_on_dataqualityheader(self.driver)
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_078_ALEX')

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            qcd.click_result_close(self.driver)
            qcd.click_action_on_first_flow(self.driver, 1)
            
            # Column type
            commontype = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))
            if (qcd.open_container(self.driver) != 1):
                commontype.click()
                
            qcd.select_item_from_column_data_type_list(self.driver, 1, 9)
            qcd.select_item_from_column_data_type_list(self.driver, 2, 1)
            
            qcd.click_save_on_cp(self.driver)
            
            if (qcd.open_container(self.driver) == 1):
                commontype.click()
                
            # Data Quality
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component3"]')))
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            qcd.check_completeness_on_dataqualityheader(self.driver)
            qcd.check_completeness_on_dataqualityheader(self.driver)
            qcd.check_nullcheck_on_dataqualityheader(self.driver)
            qcd.check_nullcheck_on_dataqualityheader(self.driver)
            qcd.check_leftspaces_on_dataqualityheader(self.driver)
            qcd.check_leftspaces_on_dataqualityheader(self.driver)
                
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_078_ALEX')
            qcd.qcd.click_result_close(self.driver)
            pass
        except Exception as e:
            raise Exception(e)
            pass
        return
