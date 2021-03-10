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

class TC032:
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

            qcd.select_dbset_input(self.driver, 'hims')
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, "Student_Information")
            qcd.select_table(self.driver, "courses_info")
            qcd.select_table(self.driver, "medicine_students_finalreport")
            qcd.click_add_select_btn(self.driver)

            # Data Quality
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 400, -200)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_quality, 1)

            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            qcd.select_rules_tab(self.driver)
            qcd.select_rule_on_dataquality(self.driver, 'Student_Information')
            qcd.inputRegularExpressOnDataQuality(self.driver, 3, "[a-z A-Z]{2}")
            qcd.inputRegularExpressOnDataQuality(self.driver, 4, "[A-Z][a-z]*[0-9][-]")
            
            qcd.select_rule_on_dataquality(self.driver, 'medicine_students_finalreport')
            qcd.inputRegularExpressOnDataQuality(self.driver, 1, "[A-Z][a-z]+")
            qcd.inputRegularExpressOnDataQuality(self.driver, 2, "[A-Z]{1}")
            qcd.inputRegularExpressOnDataQuality(self.driver, 3, "[0-9]{1,3}")
            qcd.inputRegularExpressOnDataQuality(self.driver, 4, "[A][b][0-9]{3}")
            qcd.inputRegularExpressOnDataQuality(self.driver, 8, "[0-9]{1,3}")
            qcd.inputRegularExpressOnDataQuality(self.driver, 9, "([a-z]{8,9})[-]([0-9]{8,9})")
            qcd.inputRegularExpressOnDataQuality(self.driver, 25, "(([A-Z]?)([a-z]*))")
            qcd.clickNextButtonOnDataQuality(self.driver)
            qcd.inputRegularExpressOnDataQuality(self.driver, 10, "([A_Z][+])[a-z]{2}")
            qcd.inputRegularExpressOnDataQuality(self.driver, 12, "[\w]+")
            qcd.inputRegularExpressOnDataQuality(self.driver, 14, "[A-Z][a-z]+")
            
            qcd.select_rule_on_dataquality(self.driver, 'courses_info')
            qcd.inputRegularExpressOnDataQuality(self.driver, 2, "[B][0-9]{4,6}")
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_032_ALEX')
            
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
                pass
            qcd.click_result_close(self.driver)
            qcd.open_excutions(self.driver)
            qcd.clickFirstViewEditActionOnExcutions(self.driver)
            
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()
                
            qcd.select_rules_tab(self.driver)
            qcd.select_rule_on_dataquality(self.driver, 'medicine_students_finalreport')
            qcd.clickNextButtonOnDataQuality(self.driver)
            qcd.inputRegularExpressOnDataQuality(self.driver, 11, "[a-z A-Z]{2}")
            
            qcd.save_excute_workflow(self.driver, 'TC_032_ALEX')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
            
        time.sleep(qcd.WAIT1)
        return