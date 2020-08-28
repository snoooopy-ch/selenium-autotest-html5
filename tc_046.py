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


class TC046:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            qcd.open_settings(self.driver)
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

    def workflow(self):
        try:
            qcd.selectRuleOnSettings(self.driver)
            
            qcd.clickAddNewRuleButton(self.driver)
            qcd.addNewRule(self.driver, "SQLtest", "Doctor\r\nWHERE gendertypeid=2;", "SQL")
            qcd.checkMessageAndClose(self.driver)
            
            qcd.clickEditViewRuleButton(self.driver, "SQLtest")
            qcd.clickAddRuleButton(self.driver)
            qcd.checkMessageAndClose(self.driver)
            
            qcd.deleteRule(self.driver, "SQLtest")
            qcd.checkMessageAndClose(self.driver)
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass

        print('finish')

    def check_result(self):
        pass
