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


class TC074:
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
            qcd.select_table(self.driver, "collegedetails_zero_records")
            qcd.click_add_select_btn(self.driver)

            # Data Quality
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Data Quality", 400, -200)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_quality, 1)

            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            time.sleep(qcd.WAIT1)
            qcd.select_rules_tab(self.driver)

            # save
            name_field = self.driver.find_element_by_xpath(qcd.name_xpath)
            name_field.send_keys(Keys.CONTROL + 'a')
            name_field.send_keys(Keys.DELETE)
            name_field.send_keys('TC_074_Morimura')

            qcd.clickAutoSuggestOnDataQuality(self.driver)
            print('clickAutoSuggestOnDataQuality')
            time.sleep(qcd.WAIT1)

            # btn_save = self.driver.find_element_by_xpath(qcd.save_xpath)
            # btn_save.click()
            # print('save click');

            # try:
            #     element = WebDriverWait(self.driver, qcd.WAIT100).until(EC.visibility_of_element_located((By.XPATH, qcd.alert_body_xpath)))
            #     element = WebDriverWait(self.driver, qcd.WAIT20).until(EC.element_to_be_clickable((By.XPATH, qcd.alert_button_xpath)))
            #     element.click()
            #     print('save dailog click');
            # except Exception as e:
            #     print(e)

            # qcd.click_back_execute_log_panel(self.driver)

            # print('executing...')
            # btn_execute = self.driver.find_element_by_xpath(qcd.excute_xpath)
            # btn_execute.click()
            # print('execute click');

            try:
                element = WebDriverWait(self.driver, qcd.WAIT100).until(
                    EC.visibility_of_element_located((By.XPATH, qcd.alert_body_xpath)))

                element = WebDriverWait(self.driver, qcd.WAIT3).until(
                    EC.visibility_of_element_located((By.XPATH, qcd.alert_text_xpath)))
                text = re.compile(r'<[^>]+>').sub('', element.text)
                print(text)

                element = WebDriverWait(self.driver, qcd.WAIT20).until(
                    EC.element_to_be_clickable((By.XPATH, qcd.alert_button_xpath)))
                print('initial dialog click')
            except Exception as e:
                pass

            try:
                element = WebDriverWait(self.driver, qcd.WAIT100).until(
                    EC.visibility_of_element_located((By.XPATH, qcd.alert_body_xpath)))

                element = WebDriverWait(self.driver, qcd.WAIT3).until(
                    EC.visibility_of_element_located((By.XPATH, qcd.alert_text_xpath)))
                text = re.compile(r'<[^>]+>').sub('', element.text)
                print(text)

                element = WebDriverWait(self.driver, qcd.WAIT20).until(
                    EC.element_to_be_clickable((By.XPATH, qcd.alert_button_xpath)))
                print('execute dialog click')
            except Exception as e:
                print(e)
                raise Exception('Autofill failed')

            qcd.click_back_execute_log_panel(self.driver)

            if self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div[3]/div/div/span[1]/span[1]/input').is_selected():
                print('all checked')
                qcd.check_leftspaces_on_dataqualityheader(self.driver)

                # execute
                qcd.save_excute_workflow(self.driver, 'TC_074_Morimura')
            else:
                print('unchecked')

        except Exception as e:

            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        return
