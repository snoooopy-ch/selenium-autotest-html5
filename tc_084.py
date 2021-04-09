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

class TC084:
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

            qcd.select_dbset_input(self.driver, 'marketing_dev')
            qcd.select_db_with_index(self.driver, 'demodb')
            qcd.select_table(self.driver, "Claims")
            qcd.click_add_select_btn(self.driver)

            # Target
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Target", 300, 60)
            target = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))

            if (qcd.open_container(self.driver) != 1):
                target.click()

            qcd.select_dbset_input(self.driver, 'marketing_dev')
            qcd.select_db_with_index(self.driver, 'demodb')
            qcd.select_table(self.driver, "Claims")
            qcd.click_add_select_btn(self.driver)

            # data compare
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Compare", 400, 80)
            compare1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))

            qcd.connect_elements(self.driver, input1, 1, compare1, 1)
            qcd.connect_elements(self.driver, target, 1, compare1, 1)

            if (qcd.open_container(self.driver) != 1):
                compare1.click()
            
            qcd.select_datacompare_type(self.driver, 1)

            qcd.select_mapping_tab(self.driver)
            qcd.select_key_for_warning_mapping_tableitem(self.driver, 1)
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_084_Morimura', 700)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

        print('finished')

    def check_result(self):
        try:
            records = self.driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[4]/div[1]/div[2]/div')
                
            for record in records:
                innerRecord = record.find_element_by_xpath('./div')
                recordClass = innerRecord.get_attribute("class")
                
                columns = innerRecord.find_elements_by_xpath('./div')
                if recordClass.find('-padRow') == -1:
                    print("Src Table:{}, Dest Table:{}, Match:{}, Src Record Count:{}, Src Record Mismatch:{}, Src Orphan Records:{}, Dest Record Count:{}, Dest Record Mismatch:{}, Dest Orphan Records".format(columns[0].text, columns[1].text, columns[2].find_element_by_xpath('./img').get_attribute('alt'), columns[3].text, columns[4].text, columns[5].text, columns[6].text, columns[7].text, columns[8].text))
                else:
                    break
            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
        
        qcd.click_result_close(self.driver)
        qcd.click_action_on_first_flow(self.driver, 1)
        
        target = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
        data_compare = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))
        qcd.remove_connection_between(self.driver, target, data_compare)
        
        qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Column Type", 400, 80)
        column_type = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component3"]')))
        
        qcd.connect_elements(self.driver, target, 1, column_type, 1)
        qcd.connect_elements(self.driver, column_type, 2, data_compare, 1)
        
        if (qcd.open_container(self.driver) != 1):
            column_type.click()
            
        qcd.click_maximize_for_select_columns(self.driver)
        qcd.click_select_tableitem_for_select_columns(self.driver, "Claims")
        qcd.click_select_all_for_columntype(self.driver)
        qcd.select_item_from_column_data_type_list(self.driver, 1, 9)
        qcd.click_save_on_cp(self.driver)
        qcd.close_maximize_for_select_columns(self.driver)
        
        if (qcd.open_container(self.driver) == 1):
            column_type.click()
            
        if (qcd.open_container(self.driver) == 1):
            data_compare.click()
        
        qcd.select_compare_tab(self.driver)
        qcd.select_datacompare_type(self.driver, 3)
        
        return
