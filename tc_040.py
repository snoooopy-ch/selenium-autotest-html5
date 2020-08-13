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

class TC040:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_flows()
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def open_flows(self):
        try:
            # open
            qcd.click_action_on_flow_page(self.driver)
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def workflow(self):
        try:
            fieldsName = ["Name", "Job Type", "Create Date", "Last Executed Time", "Last Executed Status"];
            filedsIndex = [2, 3, 5, 6, 7];
            fieldsXpath = [
                '/div/div[2]/div/span',
                '/div/div[3]/div',
                '/div/div[5]/div',
                '/div/div[6]/div',
                '/div/div[7]/div/div'                
            ];
            
            for i in range(5):
                p = str(i + 1)
                firstElement = self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]' + fieldsXpath[i])
                searchbox = self.driver.find_element_by_xpath(qcd.search_flow_xpath)
                searchbox.send_keys(Keys.CONTROL + 'a')
                searchbox.send_keys(Keys.DELETE)
                
                keyword = firstElement.text;
                if i == 4:
                    html = firstElement.get_attribute('innerHTML')
                    html = re.compile(r'<[^>]+>').sub('', html)
                    keyword = html
                    
                searchbox.send_keys(keyword)
                time.sleep(qcd.WAIT1)
                records = self.driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div')
                
                for record in records:
                    innerRecord = record.find_element_by_xpath('./div')
                    recordClass = innerRecord.get_attribute("class")
                    if recordClass.find('-padRow') == -1:
                        idElement = record.find_element_by_xpath('.' + fieldsXpath[i])
                        
                        target = idElement.text
                        if i == 4:
                            html = idElement.get_attribute('innerHTML')
                            html = re.compile(r'<[^>]+>').sub('', html)
                            target = html
                    
                        if target.find(keyword) == -1:
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