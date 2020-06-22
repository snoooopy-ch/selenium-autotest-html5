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

class TC029:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_workspace()
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
            pass

    def open_workspace(self):
        try:
            # open
            if (qcd.open_workspace(self.driver) != 1):
                raise Exception('fail to open workspace')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
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

            if (qcd.open_container(self.driver) != 1):
                input1.click()

            qcd.select_dbset_input(self.driver, 'tims')
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, "assessment_report")
            qcd.click_add_select_btn(self.driver)

            # Data Quality
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 500, -200)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_quality, 1)

            if (qcd.open_container(self.driver) != 1):
                data_quality.click()

            qcd.checkCompletenessOnDataQuality(self.driver, 1)
            qcd.nullCheckOnDataQuality(self.driver, 1)
            qcd.uniqueCheckOnDataQuality(self.driver, 1)
            qcd.checkLeftSpacesOnDataQuality(self.driver, 1)
            qcd.checkRightSpacesOnDataQuality(self.driver, 1)
            qcd.inputMaxLengthOnDataQuality(self.driver, 1, 12)
            qcd.inputMinLengthOnDataQuality(self.driver, 1, 4)
            
            qcd.checkCompletenessOnDataQuality(self.driver, 2)
            qcd.nullCheckOnDataQuality(self.driver, 2)
            qcd.uniqueCheckOnDataQuality(self.driver, 2)
            qcd.checkLeftSpacesOnDataQuality(self.driver, 2)
            qcd.checkRightSpacesOnDataQuality(self.driver, 2)
            qcd.inputMaxLengthOnDataQuality(self.driver, 2, 1)
            qcd.inputMinLengthOnDataQuality(self.driver, 2, 1)
            
            qcd.checkCompletenessOnDataQuality(self.driver, 6)
            qcd.nullCheckOnDataQuality(self.driver, 6)
            qcd.uniqueCheckOnDataQuality(self.driver, 6)
            qcd.checkLeftSpacesOnDataQuality(self.driver, 6)
            qcd.checkRightSpacesOnDataQuality(self.driver, 6)
            qcd.inputMaxValueOnDataQuality(self.driver, 6, 625)
            qcd.inputMinValueOnDataQuality(self.driver, 6, 31)
            
            qcd.checkCompletenessOnDataQuality(self.driver, 8)
            qcd.nullCheckOnDataQuality(self.driver, 8)
            qcd.uniqueCheckOnDataQuality(self.driver, 8)
            qcd.checkLeftSpacesOnDataQuality(self.driver, 8)
            qcd.checkRightSpacesOnDataQuality(self.driver, 8)
            qcd.inputMaxValueOnDataQuality(self.driver, 8, 91)
            qcd.inputMinValueOnDataQuality(self.driver, 8, str(0.21))
            
            qcd.clickNextButtonOnDataQuality(self.driver)
            
            qcd.checkCompletenessOnDataQuality(self.driver, 17)
            qcd.inputMaxLengthOnDataQuality(self.driver, 17, 29)
            qcd.inputMinLengthOnDataQuality(self.driver, 17, 0)
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_029_ALEX')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
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
            qcd.check_summary_statue_in_TC028_result(self.driver, self.__class__.__name__, '/html/body/div[2]/div[3]/div/div/div/div/div[2]/div[1]/div[2]')
            qcd.click_result_close(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            print("exception:{}".format(e))
            pass
            
        time.sleep(qcd.WAIT1)
        return