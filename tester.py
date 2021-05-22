# -*- coding: cp932 -*-

import time
import sys
import os
import subprocess
import traceback

import tc_common as qcd
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


class DTESTER:
    def __init__(self, drv):
        self.driver = drv

    def test(self):
        try:
            self.open_workspace()
            self.workflow()
            self.check_result()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass

    def open_workspace(self):
        try:
            # open
            if (qcd.open_workspace(self.driver) != 1):
                raise Exception('fail to open workspace')
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(
                e, traceback.format_exc()))
            raise Exception(e)
            pass

    def workflow(self):
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="root"]/div/div/div/div[1]/div/div/header/div/div[2]/div/div/div/button[1]').click()
            time.sleep(10)
            qcd.click_action_on_first_flow(self.driver, 1)
            self.driver.find_element_by_xpath(
                '//*[@id="root"]/div/div/div/div[1]/div/div/div/div/div/div[1]/header/div/button[3]').click()

            for i in range(1, 5):
                print("start {}".format(i))
                print(0)
                item = self.driver.find_element_by_xpath(
                    '//*[@id="select1"]/div/div/div[1]/div[1]')
                item.click()
                print(1)
                item = self.driver.find_element_by_xpath(
                    '//*[@id="select1"]/div/div[2]/div/div[' + str(i) + ']')
                item_txt = item.text
                item.click()
                print(2)

                histogram = self.driver.find_element_by_xpath(
                    '//*[@id="histogramResult"]')
                try:
                    chart = histogram.find_element_by_xpath('./div')
                    print("{0} : {1}".format(item_txt, "graph"))
                except Exception as e:
                    print("{0} : {1}".format(item_txt, "NA"))
                    pass
        except Exception as e:
            print(e)
            pass

    def check_result(self):
        pass
