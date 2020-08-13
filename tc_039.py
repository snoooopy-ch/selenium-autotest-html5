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

class TC039:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_dashboard()
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def open_dashboard(self):
        try:
            # open
            if (qcd.open_dashboard(self.driver) != 1):
                raise Exception('fail to open dashboard')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def workflow(self):
        try:
            fields = ["ID", "Job Type", "Flow Name", "Begin Time", "Duration", "Status"];
            
            for i in range(6):
                p = str(i + 1)
                firstElement = self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[' + p + ']/div')
                searchbox = self.driver.find_element_by_xpath(qcd.searchbox_dashboard_xpath)
                searchbox.send_keys(Keys.CONTROL + 'a')
                searchbox.send_keys(Keys.DELETE)
                searchbox.send_keys(firstElement.text)
                time.sleep(qcd.WAIT1)
                records = self.driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div')
                
                for record in records:
                    innerRecord = record.find_element_by_xpath('./div')
                    recordClass = innerRecord.get_attribute("class")
                    if recordClass.find('-padRow') == -1:
                        idElement = innerRecord.find_element_by_xpath('./div[' + p + ']/div')
                        
                        if idElement.text.find(firstElement.text) == -1:
                            print("{} search not working".format(fields[i]))
                            break
                    else:
                        break
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

        print('finished')

    def check_result(self):
        pass