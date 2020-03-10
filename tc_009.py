# -*- coding: cp932 -*-

import time
import sys
import tc_common as qcd


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

import requests
import lxml.html
import os
import subprocess
import traceback

import logging

LOG_LEVEL = logging.INFO

logger = logging.getLogger("")
formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s [%(threadName)s] [%(name)s/%(funcName)s() at line %(lineno)d]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

logger.setLevel(LOG_LEVEL)

if __name__ == '__main__':

    try:
        driver = qcd.init_selenium() 
        driver.get(qcd.BASE_URL)

	# login page loading...
        time.sleep(qcd.WAITS)
        try:
            # load jQuery
            jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"
            with open("jquery_load_helper.js") as f:
                load_jquery_js = f.read()

            driver.execute_async_script(load_jquery_js, jquery_url)
                
            with open("drag_and_drop.js") as f:
                drag_and_drop_js = f.read()
            
            # login
            if (qcd.login(driver, 'john', 'dataq') != 1):
                raise Exception('fail to login')

            # open
            if (qcd.open_workspace(driver) != 1):
                raise Exception('fail to open workspace')

            # input 1
            qcd.drop_element_to_position(driver, drag_and_drop_js, qcd.input_xpath, 300, 0)
            input1 = driver.find_element_by_xpath('//div[@id="copy-component0"]')

            if (qcd.open_container(driver) != 1):
                input1.click()

            qcd.select_dbset_input(driver, 'marketing_dev')
            qcd.select_db(driver)
            qcd.select_table(driver, 11)
            qcd.click_add_select_btn(driver)

            # input 2
            qcd.drop_element_to_position(driver, drag_and_drop_js, qcd.input_xpath, 300, 160)
            input2 = driver.find_element_by_xpath('//div[@id="copy-component1"]')

            if (qcd.open_container(driver) != 1):
                input2.click()

            qcd.select_dbset_input(driver, 'marketing_dev')
            qcd.select_db(driver)
            qcd.select_table(driver, 11)
            qcd.click_add_select_btn(driver)

            # remove duplicates
            qcd.drop_element_to_position(driver, drag_and_drop_js, qcd.removeDup_xpath, 500, -150)
            removeDuplicate = driver.find_element_by_xpath('//div[@id="copy-component2"]')

            qcd.connect_elements(driver, input1, 1, removeDuplicate, 1)

            if (qcd.open_container(driver) != 1):
                removeDuplicate.click()

            qcd.click_select_tableitem_for_select_columns(driver, 1)

            qcd.select_item_from_column_type(driver, 3)
            qcd.click_sc_done(driver)

            # data compare
            qcd.drop_element_to_position(driver, drag_and_drop_js, qcd.compare_xpath, 700, 80)
            compare1 = driver.find_element_by_xpath('//div[@id="copy-component3"]')

            qcd.connect_elements(driver, removeDuplicate, 2, compare1, 1)
            qcd.connect_elements(driver, input2, 1, compare1, 1)

            if (qcd.open_container(driver) != 1):
                compare1.click()
                
            qcd.cell_by_cell_compare(driver, 1)
            qcd.select_mapping_tab(driver)

            qcd.select_mapping_table_item(driver, 1)
            qcd.select_key_for_table_item(driver, 1)

            # execute
            qcd.save_excute_workflow(driver)
            qcd.check_summary_in_final_result(driver, '')
            
        except Exception as e:
            print(e)
            pass

    except KeyboardInterrupt:
        pass
    except Exception as e:
        # slack_post("error:{}".format(e))
        logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
        print("exception:{}".format(e))
    finally:
        driver.quit()
    
    sys.exit()
