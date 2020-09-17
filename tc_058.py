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


class TC058:
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
            # first
            qcd.open_excutions(self.driver)
            qcd.input_searchbox_on_dashboard(self.driver, 'Auto Suggest')
            qcd.clickFirstViewEditActionOnExcutions(self.driver)
            
            time.sleep(qcd.WAIT10)
            
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()
                
            
            # Check
            try:
                if self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/span/span[1]/input').is_selected():
                    print('all checked')
                else:
                    print('unchekced')
                    raise Exception('unchecked')
            except:
                pass
            
            # second
            qcd.open_excutions(self.driver)
            qcd.input_searchbox_on_dashboard(self.driver, 'Auto Suggest')
            qcd.clickFirstViewEditActionOnExcutions(self.driver)
            
            time.sleep(qcd.WAIT10)
            
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()
                
            
            # Check
            try:
                if self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/span/span[1]/input').is_selected():
                    print('all checked')
                else:
                    print('unchekced')
                    raise Exception('unchecked')
            except:
                pass   
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

        print('finished')

    def check_result(self):
        try:
            pass
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass