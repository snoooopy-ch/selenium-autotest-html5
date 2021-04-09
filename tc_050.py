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

class TC050:
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
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, "City")
            qcd.select_table(self.driver, "Claims")
            qcd.click_add_select_btn(self.driver)

            # select columns
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Select Columns", 400, -80)
            selectcolumns = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))

            qcd.connect_elements(self.driver, input1, 1, selectcolumns, 1)
            
            if (qcd.open_container(self.driver) != 1):
                selectcolumns.click()

            qcd.click_select_tableitem_for_select_columns(self.driver, "Claims")
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(self.driver, "City")
            qcd.select_table(self.driver, "zipcode")
            qcd.click_save_on_cp(self.driver)
            
            # Column type
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Column type", 800, -150)
            columntype = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))

            qcd.connect_elements(self.driver, selectcolumns, 2, columntype, 1)

            if (qcd.open_container(self.driver) != 1):
                columntype.click()

            qcd.click_maximize_for_select_columns(self.driver)
            
            qcd.click_select_tableitem_for_select_columns(self.driver, "Claims")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.select_item_from_column_data_type_list(self.driver, 2, 1)
            qcd.click_save_on_cp(self.driver)
            
            qcd.click_select_tableitem_for_select_columns(self.driver, "City")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.select_item_from_column_data_type_list(self.driver, 1, 1)
            qcd.click_save_on_cp(self.driver)

            # Remove Duplicate
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Remove Duplicates", 1000, -250)
            removeduplicates = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component3"]')))

            qcd.connect_elements(self.driver, columntype, 2, removeduplicates, 1)
            if (qcd.open_container(self.driver) != 1):
                removeduplicates.click()

            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_select_tableitem_for_select_columns(self.driver, "Claims")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(self.driver, "City")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.click_save_on_cp(self.driver)

            qcd.close_maximize_for_select_columns(self.driver)
                
            # Data Quality
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 1150, -250)
            quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component4"]')))

            qcd.connect_elements(self.driver, removeduplicates, 2, quality, 1)

            if (qcd.open_container(self.driver) != 1):
                quality.click()
                
            time.sleep(qcd.WAIT1)
            qcd.select_rules_tab(self.driver)
            qcd.check_completeness_on_dataqualityheader(self.driver)
            qcd.check_nullcheck_on_dataqualityheader(self.driver)
            qcd.check_leftspaces_on_dataqualityheader(self.driver)
            qcd.check_rightspaces_on_dataqualityheader(self.driver)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_050_Morimura')

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            detail_span_xpath = '/html/body/div[2]/div[3]/div/div/div/div/div[1]/span[2]'
            try:
                if qcd.isElementPresentForResult(self.driver, detail_span_xpath) != True:
                    raise Exception()
                
                detail_span = self.driver.find_elements_by_xpath(detail_span_xpath)
                if (len(detail_span) == 1):
                    detail_span[0].click()
                    time.sleep(qcd.WAIT3)
            except Exception as e:
                print(e)
                raise Exception(e)
                pass

            summary_table = self.driver.find_element_by_xpath(qcd.normal_result_summary_xpath)
            table_trs = summary_table.find_elements_by_xpath('./div')

            flag = 0
            try:
                for tr in table_trs:
                    inner_tr = tr.find_element_by_xpath('./div')
                    tds = inner_tr.find_elements_by_xpath('./div')

                    output = ''
                    find = 0
                    print("{} {} {}".format(tds[1].find_element_by_xpath('./div').text, tds[2].find_element_by_xpath('./div').text, tds[6].find_element_by_xpath('./div/span').text))
            except Exception as ex:
                print(ex)
                pass

            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
        return
