# -*- coding: cp932 -*-

import time
import sys
from sys import platform as _platform
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

import urllib2
from lxml import etree

import logging

LOG_LEVEL = logging.INFO

logger = logging.getLogger("")
formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s [%(threadName)s] [%(name)s/%(funcName)s() at line %(lineno)d]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

logger.setLevel(LOG_LEVEL)

BASE_URL = 'http://dataq-frontend.s3-website.us-east-2.amazonaws.com/'
WAITS = 1
WAITM = 3
WAITL = 5

user_xpath          = '//div[@id="root"]/div/div/div/div/div/div/input'
pass_xpath          = '//div[@id="root"]/div/div/div/div/div[2]/div/input'
loginbtn_xpath      ="//button[@class='MuiButtonBase-root MuiButton-root jss13 MuiButton-contained MuiButton-containedSecondary']"
open_xpath          = '//button[@class="MuiButtonBase-root MuiFab-root MuiFab-sizeSmall MuiFab-primary"]'
input_xpath         = '//div[@id="component0"]/img'
container_xpath     = '//*[@id="root"]/div/div[1]/div/div/div/div/div/div[2]/div'
selectcolumn_xpath  = '//div[@id="component2"]/img'
select_all_xpath    = '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[4]/button/span[1]'
selecttype_xpath    = '//div[@id="component3"]/img'
btn_addSelected     = '//div[@id="top_panel"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/button'
compare_xpath       = '//div[@id="component1"]/img'
removeDup_xpath     = '//div[@id="component4"]/img'
tabmapping_xpath    = '//*[@id="simple-tab-1"]'
table1_xpath        = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div'
table1_val_xpath    = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div[2]/div'
table2_xpath        = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]/div/div'
table2_val_xpath    = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/div'
table_sc_xpath      = '//*[@id="top_panel"]/div/div[2]/div[1]/div/div[1]/div/div/div[1]'
table_sc_val_xpath  = '//*[@id="top_panel"]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/div'
done_sc_xapth       = '//*[@id="top_panel"]/div/div[1]/header/div/button'
mapplus_xpath       = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[3]'
name_xpath          = '//div[@id="root"]/div/div[1]/div/div/div/div/div/div[1]/header/div/div/div/input'
save_xpath          = '//div[@id="root"]/div/div[1]/div/div/div/div/div/div[1]/header/div/button[1]'
excute_xpath        = '//div[@id="root"]/div/div[1]/div/div/div/div/div/div[1]/header/div/button[2]'
result_xpath        = '//div[@id="root"]/div/div[1]/div/div/div/div/div/div[1]/header/div/button[3]'
result_txt_xpath    = '/html/body/div[2]/div[3]/div/div/div/table/tr[7]/span'



def init_selenium():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--remote-debugging-port=9222")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    if _platform == "linux" or _platform =="linux2":
        driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chromeOptions)
    elif _platform == "darwin":
        driver = webdriver.Chrome()
    elif _platform == "win32" or _platform == "win64":
        driver = webdriver.Chrome('chromedriver.exe',chrome_options=chromeOptions)

    return driver

# action to login
def login(driver, login_user, login_pass):
    ret = 1
    
    try:
        input_user = driver.find_element_by_xpath(user_xpath)
        input_user.send_keys(login_user)

        input_pass = driver.find_element_by_xpath(pass_xpath)
        input_pass.send_keys(login_pass)

        btn_login = driver.find_elements_by_xpath(loginbtn_xpath)[0]
        btn_login.click()
        time.sleep(WAITL)

        print('login')

    except Exception as e:
        print(e)
        ret = 0
        pass
    
    return ret

# action to open a workspace
def open_workspace(driver):
    ret = 1

    try:
        btn_plus = driver.find_element_by_xpath(open_xpath)
        btn_plus.click()
        time.sleep(10)

        print('open workspace')

    except Exception as e:
        print(e)
        ret = 0
        pass

    return ret

# action to move element
def drop_element_to_position(driver, js, xpath, x, y):
    input_element = driver.find_element_by_xpath(xpath)
    driver.execute_script(js, input_element, x, y)

    print('move element')
    pass

# action to open controller
def open_container(driver):
    ret = 1   
    container = driver.find_elements_by_xpath(container_xpath)
    if (len(container) == 2):
        ret = 1
    else:
        ret = 0

    print('open container')
    return ret


# action to select db set.
def select_dbset_input(driver, db):
    db_select = driver.find_elements_by_xpath("//select[@name='connection']")[0]
    db_select.click()
    time.sleep(WAITS)

    db_value = driver.find_element_by_xpath("//select[@name='connection']/option[@value='" + db + "']")
    db_value.click()
    time.sleep(WAITS)

    print('select db set')
    return

# action to select db
def select_db(driver):
    db_name = driver.find_elements_by_xpath("//div[@class=' css-tlfecz-indicatorContainer']")[0]
    db_name.click()
    
    db_demo = driver.find_element_by_xpath("//div[@id='top_panel']/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div")
    db_demo.click()
    time.sleep(WAITM)

    print('select db name')    
    return

# action to select table item for 'select columns' or 'remove_duplicate'
def click_select_tableitem_for_select_columns(driver, index):
    db_select = driver.find_element_by_xpath(table_sc_xpath)
    db_select.click()
    time.sleep(WAITS)

    db_value = driver.find_element_by_xpath(table_sc_val_xpath + '[' + str(index) + ']')
    db_value.click()
    time.sleep(WAITS)
    print('select table item')
    return
    
# action to click one item of table
def select_table(driver, index):
    xpath = "//div[@id='top_panel']/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[" + str(index) + "]/label/span"
    city = driver.find_element_by_xpath(xpath)
    city.click()

    print('select table ' + str(index))
    return

# action to click one item of column type
def select_item_from_column_type(driver, index):
    xpath = "//*[@id='top_panel']/div/div[2]/div[1]/div/div[2]/div[3]/div[" + str(index) + "]/input"
    city = driver.find_element_by_xpath(xpath)
    city.click()

    print('select item from column type ' + str(index))
    return

# action to click data type of column type
def select_item_from_column_data_type(driver, index):
    xpath = "//*[@id='top_panel']/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div/div[4]/div/div[1]/div[1]"
    city = driver.find_element_by_xpath(xpath)
    city.click()
    time.sleep(WAITS)

    item_xpath = "//*[@id='top_panel']/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div/div[4]/div/div[2]/div/div[" + str(index) + "]"
    item_value = driver.find_element_by_xpath(item_xpath)
    item_value.click()
    time.sleep(WAITS)
    print('select item from column type ' + str(index))
    return

# action to click all check of table
def click_all_select(driver):
    btn_select_all = driver.find_element_by_xpath(select_all_xpath)
    btn_select_all.click()
    
    print('select all the table')
    time.sleep(WAITS)
    return

# action to click 'Add Selected' button
def click_add_select_btn(driver):
    btn_add = driver.find_element_by_xpath(btn_addSelected)
    btn_add.click()
    time.sleep(WAITM)

    print('add selected click')
    return

# connecting
def connect_all_elements(driver):
    entry1 = driver.find_elements_by_xpath('//div[@id="drop-location"]/div')[1]
    entry2 = driver.find_elements_by_xpath('//div[@id="drop-location"]/div')[3]
    entry3 = driver.find_elements_by_xpath('//div[@id="drop-location"]/div')[5]

    action = ActionChains(driver)
    action.click_and_hold(entry1).move_to_element(entry3).release(entry3).perform()
    time.sleep(WAITS)

    action.click_and_hold(entry2).move_to_element(entry3).release(entry3).perform()
    time.sleep(WAITS)

    print('element selected')
    return

# connecting_two_element
def connect_elements(driver, element1, n, element2, m):
    first_parent = element1.find_element_by_xpath('..')
    entry1 = first_parent.find_element_by_xpath("./following-sibling::div")
    if (n == 2):
        entry1 = entry1.find_element_by_xpath("./following-sibling::div")

    second_parent = element2.find_element_by_xpath('..')
    entry2 = second_parent.find_element_by_xpath("./following-sibling::div")
    if (m == 2):
        entry2 = entry2.find_element_by_xpath("./following-sibling::div")

    action = ActionChains(driver)
    action.click_and_hold(entry1).move_to_element(entry2).release(entry2).perform()
    time.sleep(WAITS)

    print('connected')
    return


# select 'cell By cell Compare' item
def cell_by_cell_compare(driver, index):
    db_select3 = driver.find_elements_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div/div/div/div')[1]
    db_select3.click()
    time.sleep(WAITS)
    print("db open")

    db_select_val3 = driver.find_elements_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div/div/div[2]/div/div')[index - 1]
    db_select_val3.click()
    print("selected")
    time.sleep(WAITS)
    return

# select mapping tab
def select_mapping_tab(driver):
    tab_mapping = driver.find_element_by_xpath(tabmapping_xpath)
    tab_mapping.click()
    time.sleep(WAITM)

    print('mapping tab selected')
    return

# selct mapping table name
def add_mapping_table_name(driver):
    table = driver.find_element_by_xpath(table1_xpath)
    table.click()
    time.sleep(WAITS)

    table_value = driver.find_element_by_xpath(table1_val_xpath)
    table_value.click()
    time.sleep(WAITS)

    table = driver.find_element_by_xpath(table2_xpath)
    table.click()
    time.sleep(WAITS)

    table_value = driver.find_element_by_xpath(table2_val_xpath)
    table_value.click()
    time.sleep(WAITL)

    plus = driver.find_element_by_xpath(mapplus_xpath)
    plus.click()
    time.sleep(WAITM)

    print('mapping table names')
    return

# select mapping table item
def select_mapping_table_item(driver, index):
    time.sleep(WAITM)
    table_item = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/table/tr[' + str(index) + ']/td[2]/span[1]')
    table_item.click()
    time.sleep(WAITM)
    print('select mapping table item')
    return

# select key for table item
def select_key_for_table_item(driver, index):
    input_key = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[1]/input')
    input_key.click()
    time.sleep(WAITS)

    print('select key for table item')
    return;

# action to click done
def click_sc_done(driver):
    btn_done = driver.find_element_by_xpath(done_sc_xapth)
    btn_done.click()
    print('click done')
    return;    

# save and excute workflow
def save_excute_workflow(driver):
    name_field = driver.find_element_by_xpath(name_xpath);
    name_field.send_keys('ALEX')

    btn_save = driver.find_element_by_xpath(save_xpath)
    btn_save.click()
    time.sleep(WAITM)

    print('executing...')
    btn_execute = driver.find_element_by_xpath(excute_xpath)
    btn_execute.click()
    time.sleep(WAITM)

    try:
        btn_result = WebDriverWait(driver, 2000).until(EC.element_to_be_clickable((By.XPATH, result_xpath)))
        time.sleep(WAITM)
        btn_result.click()
        time.sleep(10)
    except Exception as e:
        time.sleep(10)
        pass

    return

# check summary in final result
def check_summary_in_final_result(driver, summary_xpath):

    try:
        result_txt = driver.find_elements_by_xpath(result_txt_xpath)
        if (len(result_txt) == 1):
            if (result_txt[0].text == 'No mismatch in the table'):
                print('No mismatch in the table')
                return
    except Exception as e:
        print(e)
        pass

    if (summary_xpath == ''):
        return
    
    summary_table = driver.find_element_by_xpath(summary_xpath)
    table_trs = summary_table.find_elements_by_xpath('./div')

    flag = 0
    try:
        for tr in table_trs:
            inner_tr = tr.find_element_by_xpath('./div')
            tds = inner_tr.find_elements_by_xpath('./div')

            output = ''
            find = 0
            for td in tds:
                try:
                    img_element = td.find_element_by_xpath('./img')
                    tmp = img_element.get_attribute("alt")
                    if (tmp.find('umnatch') != -1):
                        find = 1
                        flag = 1
                except Exception as e:
                    pass

                if (find == 1):
                    break
                else:
                    output= output + ' ' + td.text

            if (find == 1):
                print(output + ' is unmatched')
    except Exception as ex:
        print(ex)
        pass

    if (flag == 0):
        print('No mismatch in the table')
        
    time.sleep(10)

    return;

# check summary in final result for TC007, TC009
def check_summary_in_fianl_mismatched_count(driver, summary_xpath):
    try:
        summary_table = driver.find_element_by_xpath(summary_xpath)
        summary_tables = summary_table.find_elements_by_xpath('./div')
        for tr in summary_tables:
            inner_tr = tr.find_element_by_xpath('./div')
            columnname = inner_tr.find_element_by_xpath('./div[1]').text
            count = inner_tr.find_element_by_xpath('./div[2]').text
            print(columnname + ' mismatch count is ' + count)
    except Exception as ex:
        pass

    time.sleep(10)
    return;
            

            
        
        
    
