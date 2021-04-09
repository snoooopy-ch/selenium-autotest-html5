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

class TC060:
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
            
            # input 1
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Source", 300, 0)
            input1 = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component0"]')))

            if (qcd.open_container(self.driver) != 1):
                input1.click()

            qcd.select_dbset_input(self.driver, 'marketing_dev')
            qcd.select_db(self.driver)
            qcd.select_table(self.driver, "Doctor")
            qcd.select_table(self.driver, "Patient")
            qcd.select_table(self.driver, "Insurance")
            qcd.select_table(self.driver, "Staff")
            qcd.click_add_select_btn(self.driver)

            # Data Quality
            qcd.drop_element_to_position(self.driver, drag_and_drop_js, "Data Quality", 400, -200)
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            qcd.connect_elements(self.driver, input1, 1, data_quality, 1)

            if (qcd.open_container(self.driver) != 1):
                data_quality.click()
            time.sleep(qcd.WAIT3)
            
            qcd.select_sql_mapping_tab(self.driver)
            
            qcd.apply_sql_rul_dataquality(self.driver, "SELECT Patient_name,Patient_blood_group,diagnosis_session, Patient_healthcard_no FROM Patient WHERE Patient_healthcard_no BETWEEN 47 AND 48 LIMIT 49", "sql1")
            qcd.apply_sql_rul_dataquality(self.driver, "SELECT I_id,I_name,I_address FROM Insurance where active=1", "sql2")
            qcd.apply_sql_rul_dataquality(self.driver, "SELECT doc_name,Specialization From Doctor ORDER BY doc_name", "sql3")
            qcd.apply_sql_rul_dataquality(self.driver, "SELECT Patient_name from Patient where Patient_blood_group='A+ve'", "sql4")
            qcd.apply_sql_rul_dataquality(self.driver, "SELECT birth_date from Patient where Patient_name='Ratna'", "sql5")
            
            qcd.modify_sql_rul_dataquality(self.driver, 5, "Select birth_date from Patient where Patient_name='Vithika'", "")

            # execute
            qcd.save_excute_workflow(self.driver, 'TC_060_Morimura')
            
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
        
    def check_result(self):
        try:
            self.printResultTable()
            
            qcd.open_excutions(self.driver)
            qcd.clickFirstViewEditActionOnExcutions(self.driver)
            
            data_quality = WebDriverWait(self.driver, qcd.WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="copy-component1"]')))
            
            if (qcd.open_container(self.driver) == 1):
                data_quality.click()
                
            if (qcd.open_container(self.driver) != 1):
                data_quality.click()
            
            qcd.select_sql_mapping_tab(self.driver)
            qcd.apply_sql_rul_dataquality(self.driver, "Select doc_name From Doctor where age=40", "sql6")
            
            self.driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[3]/div/div[2]/div/div/div[1]/div[2]/div[6]/div/div[5]/div/div').click()
            
            # execute
            qcd.save_excute_workflow(self.driver, 'TC_060_Morimura', 500)
            
            self.printResultTable()
        except Exception as e:
            qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
            raise Exception(e)
            pass
        return
    
    def printResultTable(self):
        detail_span_xpath = '/html/body/div[2]/div[3]/div/div/div/div/div[1]/span[2]'
        try:
            if qcd.isElementPresentForResult(self.driver, detail_span_xpath) != True:
                raise Exception()
            
            detail_span = self.driver.find_elements_by_xpath(detail_span_xpath)
            if (len(detail_span) == 1):
                detail_span[0].click()
                time.sleep(qcd.WAIT3)
        except Exception as e:
            print(e)
            raise Exception(e)
            pass
        qcd.check_summary_statue_in_final_tc60_result(self.driver, self.__class__.__name__, qcd.normal_result_summary_xpath)
        qcd.click_result_close(self.driver)
        