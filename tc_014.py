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


class TC014:
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

            qcd.select_dbset_input(self.driver, 'marketing_dev')
            qcd.select_db_with_index(self.driver, "demodb")
            qcd.select_table(self.driver, "Patient")
            qcd.select_table(self.driver, "Medicine_manufacturer_info")
            qcd.click_add_select_btn(self.driver)

            # Data Quality
            qcd.drop_element_to_position(
                self.driver, drag_and_drop_js, "Data Quality", 400, -100)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_quality, 1)

            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            qcd.initialize_on_dataquality(self.driver, 1, 2, 3, 1, 1)
            qcd.initialize_on_dataquality(self.driver, 2, 2, 2, 3, 2)
            qcd.initialize_on_dataquality(self.driver, 5, 2, 1, 2, 5)
            qcd.initialize_on_dataquality(self.driver, 9, 2, 1, 1, 1)
            qcd.initialize_on_dataquality_for_select_rule(
                self.driver, 3, 1, 5, 720)
            qcd.initialize_on_dataquality(self.driver, 4, 1, 4, 3, 4)

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_014_Morimura')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass

    def check_result(self):
        try:
            try:
                if qcd.isElementPresentForResult(self.driver, qcd.detail_span_xpath) != True:
                    raise Exception()

                detail_span = self.driver.find_elements_by_xpath(
                    qcd.detail_span_xpath)
                if (len(detail_span) == 1):
                    detail_span[0].click()
                    time.sleep(qcd.WAIT3)
            except Exception as e:
                print(e)
                raise Exception(e)
                pass
            qcd.check_summary_statue_in_final_result(
                self.driver, self.__class__.__name__, '/html/body/div[2]/div[3]/div/div/div/div/div[2]/div[1]/div[2]')
            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass
        return
