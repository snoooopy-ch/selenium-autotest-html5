# -*- coding: cp932 -*-

import time
import sys
import tc_common as qcd
import os
import subprocess
import traceback
import logging
import re

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


class TC053:
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

            qcd.select_dbset_input(self.driver, 'tims')
            qcd.select_db_with_index(self.driver, 'tims_db')
            qcd.select_table(self.driver, "assessment_report")
            qcd.click_add_select_btn(self.driver)

            # input 2
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Target", 300, 160)
            input2 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))

            if (qcd.open_container(self.driver) != 1):
                input2.click()

            qcd.select_dbset_input(self.driver, 'hims')
            qcd.select_db_with_index(self.driver, 'hims_db')
            qcd.select_table(self.driver, "Student_Information")
            qcd.click_add_select_btn(self.driver)

            # data compare
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Data Compare", 400, 80)
            compare1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))

            qcd.connect_elements(self.driver, input1, 1, compare1, 1)
            qcd.connect_elements(self.driver, input2, 1, compare1, 1)

            if (qcd.open_container(self.driver) != 1):
                compare1.click()

            qcd.select_datacompare_type(self.driver, 3)

            qcd.select_mapping_tab(self.driver)
            qcd.add_mapping_table_name(self.driver)

            name_field = self.driver.find_element_by_xpath(qcd.name_xpath)
            name_field.send_keys(Keys.CONTROL + 'a')
            name_field.send_keys(Keys.DELETE)
            name_field.send_keys('TC_053_Morimura')

            btn_save = self.driver.find_element_by_xpath(qcd.save_xpath)
            btn_save.click()
            print('save click')

            try:
                element = WebDriverWait(self.driver, qcd.WAIT100).until(
                    EC.visibility_of_element_located((By.XPATH, qcd.alert_body_xpath)))
                element = WebDriverWait(self.driver, qcd.WAIT3).until(
                    EC.visibility_of_element_located((By.XPATH, qcd.alert_text_xpath)))
                text = re.compile(r'<[^>]+>').sub('', element.text)
                print(text)

                if text != 'Please select the columns':
                    return

                element = WebDriverWait(self.driver, qcd.WAIT20).until(
                    EC.element_to_be_clickable((By.XPATH, qcd.alert_button_xpath)))
                element.click()
            except Exception as e:
                pass

            qcd.select_mapping_table_item(self.driver, 1)
            qcd.add_columns_in_datacompare_tableitem(self.driver)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_053_Morimura')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            qcd.click_result_close(self.driver)

            qcd.open_excutions(self.driver)
            qcd.clickFirstViewEditActionOnExcutions(self.driver)

            input2 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))

            if (qcd.open_container(self.driver) != 1):
                input2.click()

            qcd.select_dbset_input(self.driver, 'tims')
            qcd.select_db_with_index(self.driver, 'tims_db')
            qcd.select_table(self.driver, "assessment_report")
            qcd.click_add_select_btn(self.driver)

            if (qcd.open_container(self.driver) == 1):
                input2.click()

            compare1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component2"]')))

            if (qcd.open_container(self.driver) != 1):
                compare1.click()

            qcd.select_compare_tab(self.driver)
            qcd.select_datacompare_type(self.driver, 1)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_053_Morimura')
            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass
