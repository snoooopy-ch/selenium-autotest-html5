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

class TC034:
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
            
            count = 0;
            elements = ["Input", "Data Compare", "Select Columns", "Common Type", "Remove Duplicates", "Data Quality", "Data Profile"]
            results = []
            
            for element in elements:
                qcd.drop_element_to_position(self.driver, drag_and_drop_js, element, 300, 0)
                
                hasAlert = False
                try:
                    alert = self.driver.switch_to.alert
                    text = alert.text
                    alert.accept()
                    hasAlert = True
                    results.append("{} has warning alert '{}'".format(element, text))
                    continue
                except:
                    pass
                    
                if hasAlert == False:
                    try:
                        if qcd.isElementPresentForResult(self.driver, '//*[@id="copy-component' + str(count) + '"]/span') == True:
                            del_btn = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="copy-component' + str(count) + '"]/span')))
                            del_btn.click()
                            results.append("{} is deleted".format(element))
                            --count
                        else:
                            results.append("{} has no delete button".format(element))
                    except:
                        results.append("{} has no delete button".format(element))
                
                ++count
                
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

        print('finished')
        for result in results:
            print(result)

    def check_result(self):
        return