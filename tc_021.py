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


class TC021:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_workspace()
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass

    def open_workspace(self):
        try:
            # open
            if (qcd.open_workspace(self.driver) != 1):
                raise Exception('fail to open workspace')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
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
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Source", 300, 0)
            input1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))

            if (qcd.open_container(self.driver) != 1):
                input1.click()

            qcd.select_dbset_input(self.driver, 'sampledb_src')
            qcd.select_db_with_index(self.driver, 'sampledb_src')
            qcd.click_all_select(self.driver)
            qcd.click_add_select_btn(self.driver)

            # input 2
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Target", 300, 160)
            input2 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))

            if (qcd.open_container(self.driver) != 1):
                input2.click()

            qcd.select_dbset_input(self.driver, 'sampledb_dest')
            qcd.select_db_with_index(self.driver, 'sampledb_dest')
            qcd.click_all_select(self.driver)
            qcd.click_add_select_btn(self.driver)

            # select columns
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Select Columns", 350, -50)
            selectcolumns = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))

            qcd.connect_elements(self.driver, input1, 1, selectcolumns, 1)

            if (qcd.open_container(self.driver) != 1):
                selectcolumns.click()

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "collegedetails_zero_records")
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "college_zero_records")
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "tolerance")
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "joining_details")
            qcd.select_table(self.driver, "joining_date")
            qcd.click_save_on_cp(self.driver)

            # Column type
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Column type", 700, -100)
            columntype = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component3"]')))

            qcd.connect_elements(self.driver, selectcolumns, 2, columntype, 1)

            if (qcd.open_container(self.driver) != 1):
                columntype.click()

            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_select_tableitem_for_select_columns(
                self.driver, "collegedetails_zero_records")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.select_item_from_column_data_type_list(self.driver, 2, 1)
            qcd.select_item_from_column_data_type_list(self.driver, 5, 1)
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "college_zero_records")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "tolerance")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.select_item_from_column_data_type_list(self.driver, 7, 5)
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "joining_details")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.click_save_on_cp(self.driver)

            # Remove Duplicate
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Remove Duplicates", 850, -250)
            removeduplicates = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component4"]')))

            qcd.connect_elements(self.driver, columntype,
                                 2, removeduplicates, 1)
            if (qcd.open_container(self.driver) != 1):
                removeduplicates.click()

            qcd.click_maximize_for_select_columns(self.driver)
            qcd.click_select_tableitem_for_select_columns(
                self.driver, "collegedetails_zero_records")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "college_zero_records")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "tolerance")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.click_save_on_cp(self.driver)

            qcd.click_select_tableitem_for_select_columns(
                self.driver, "joining_details")
            qcd.click_select_all_for_columntype(self.driver)
            qcd.click_save_on_cp(self.driver)

            # Data Compare
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Data Compare", 850, 50)
            compare1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component5"]')))

            qcd.connect_elements(self.driver, removeduplicates, 2, compare1, 1)
            qcd.connect_elements(self.driver, input2, 1, compare1, 1)

            if (qcd.open_container(self.driver) != 1):
                compare1.click()
            qcd.click_maximize_for_select_columns(self.driver)

            qcd.select_datacompare_type(self.driver, 1)
            qcd.select_mapping_tab(self.driver)
            # qcd.add_mapping_table_name(self.driver)
            qcd.add_mapping_table_for_type_compare_with_index(
                self.driver, 'college_zero_records', 'college_withdata')

            qcd.select_key_for_warning_mapping_tableitem(self.driver, 1)

            qcd.select_mapping_table_item(self.driver, 1)
            data_type = self.driver.find_element_by_xpath(
                '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/img').get_attribute("title")
            print("colleage_code_Varchar's type is " + data_type)

            qcd.select_mapping_table_item(self.driver, 2)
            qcd.add_columns_in_datacompare_tableitem(self.driver)

            data_type = self.driver.find_element_by_xpath(
                '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div/div[3]/div/div[1]/div[2]/div[5]/div/div[2]/img').get_attribute("title")
            print("gradePoints_int's type is " + data_type)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_021_Morimura')

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            qcd.check_summary_in_final_result(
                self.driver, self.__class__.__name__, qcd.normal_result_summary_xpath)

            self.driver.find_element_by_xpath(qcd.detail_xpath).click()

            qcd.click_share_button_and_close(self.driver)
            qcd.click_result_close(self.driver)

            qcd.open_dashboard(self.driver)
            metric_item = self.driver.find_element_by_xpath(
                '/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[7]/div/div')
            ActionChains(self.driver).move_to_element(metric_item).perform()
            print(self.driver.find_element_by_xpath(
                '/html/body/div[2]/div').text)

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass
