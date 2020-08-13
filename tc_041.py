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

class TC041:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_flows()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def open_flows(self):
        button = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, qcd.flow_xpath)))
        className = button.get_attribute("class")
        
        if className.find("Mui-selected") != -1:
            print("It redirected to Flow page")
        else:
            print("Redirecting to Flow page is failed")
            
        logoutBtn = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, qcd.logout_xpath)))
        logoutBtn.click()
        
        self.driver.back()
        print("back button clicked")
        
        if (qcd.login(self.driver, "user", "password") != 1):
            raise Exception('fail to login')
        
        currentUrl = self.driver.current_url
        if currentUrl == "http://dataq-frontend.s3-website.us-east-2.amazonaws.com/#/":
            print("Login failed")
        else:
            print("Login succeed")

    