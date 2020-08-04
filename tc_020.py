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

class TC020:
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
            # load jQuery
            jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"
            with open("js/jquery_load_helper.js") as f:
                load_jquery_js = f.read()

            self.driver.execute_async_script(load_jquery_js, jquery_url)
                
            with open("js/drag_and_drop.js") as f:
                drag_and_drop_js = f.read()

            qcd.open_excutions(self.driver)
            record_count = qcd.input_searchbox_on_dashboard(self.driver, "TC_019")
            
            if record_count == 0:
                raise Exception('no search results')
            
            qcd.clickFirstViewEditActionOnExcutions(self.driver)
            time.sleep(qcd.WAIT3)
            qcd.click_notification(self.driver)
            qcd.click_tab_on_notification_board(self.driver, 4)
            qcd.set_start_time_with10(self.driver)

        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

        time.sleep(qcd.WAIT1)

    def check_result(self):
        pass