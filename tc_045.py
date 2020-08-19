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


class TC045:
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
        pass

    def workflow(self):
        try:
            # open
            qcd.click_action_on_flow_page(self.driver)
            
            qcd.click_action_on_first_flow(self.driver, 7)
            time.sleep(qcd.WAIT1)
            qcd.inputValueAndSaveOnDailog(self.driver, "ragini")
            qcd.checkMessageAndClose(self.driver)
            time.sleep(qcd.WAIT3)
            
            # open
            qcd.click_action_on_flow_page(self.driver)
            qcd.click_action_on_first_flow(self.driver, 7)
            time.sleep(qcd.WAIT1)
            qcd.inputValueAndSaveOnDailog(self.driver, "ragini")
            qcd.checkMessageAndClose(self.driver)
            
            qcd.click_action_on_first_flow(self.driver, 3)
            print("deleted")
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            time.sleep(1000)
            raise Exception(e)
            pass

        print('finish')

    def check_result(self):
        pass
