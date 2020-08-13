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

import os
import subprocess
import traceback


import logging

LOG_LEVEL = logging.INFO

logging.basicConfig()
logger = logging.getLogger("")
formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s [%(threadName)s] [%(name)s/%(funcName)s() at line %(lineno)d]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

logger.setLevel(LOG_LEVEL)

WAIT1                       = 2
WAIT3                       = 5
WAIT5                       = 10
WAIT10                      = 15
WAIT20                      = 20
WAIT100                     = 100
WAITDRIVER                  = 20

elements                    = ["Input", "Data Compare", "Select Columns", "Common Type", "Remove Duplicates", "Data Quality", "Data Profile"]
element_xpath               = ['//div[@id="component0"]/img', '//div[@id="component1"]/img', '//div[@id="component2"]/img', '//div[@id="component3"]/img', '//div[@id="component4"]/img', '//div[@id="component5"]/img', '//div[@id="component6"]/img']

user_xpath                  = '//*[@id="root"]/div/div/div[1]/div/div[1]/div/div/div[2]/div[1]/div/input'
pass_xpath                  = '//*[@id="root"]/div/div/div[1]/div/div[1]/div/div/div[2]/div[2]/div/input'
loginbtn_xpath              = '//*[@id="root"]/div/div/div[1]/div/div[1]/div/div/div[2]/div[3]/button'
open_xpath                  = '//button[@class="MuiButtonBase-root MuiFab-root MuiFab-sizeSmall MuiFab-primary"]'
input_xpath                 = '//div[@id="component0"]/img'
container_xpath             = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div'
selectcolumn_xpath          = '//div[@id="component2"]/img'
select_all_xpath            = '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[4]/button/span[1]'
selecttype_xpath            = '//div[@id="component3"]/img'
btn_addSelected             = '//div[@id="top_panel"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/button'
compare_xpath               = '//div[@id="component1"]/img'
removeDup_xpath             = '//div[@id="component4"]/img'
data_quality_xpath          = '//div[@id="component6"]/img'
data_profile_xpath          = '//div[@id="component7"]/img'
tabmapping_xpath            = '//*[@id="simple-tab-1"]'
table1_xpath                = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div'
table1_val_xpath            = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div[2]/div'
table2_xpath                = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]/div/div'
table2_val_xpath            = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]/div/div[2]/div'
table_sc_xpath              = '//*[@id="top_panel"]/div/div[2]/div[1]/div/div[1]/div/div/div[1]'
table_sc_val_xpath          = '//*[@id="top_panel"]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/div'
done_sc_xapth               = '//*[@id="top_panel"]/div/div[1]/header/div/button'
mapplus_xpath               = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[1]/div[2]/div[3]'
name_xpath                  = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[1]/header/div/div/div/input'
save_xpath                  = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[1]/header/div/button[1]'
excute_xpath                = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[1]/header/div/button[2]'
result_xpath                = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[1]/header/div/button[3]'
result_txt_xpath            = '/html/body/div[2]/div[3]/div/div/div/div/table/tr[8]/span'
random_input_xpath          = '//*[@id="top_panel"]/div/div[2]/div[2]/div/div[2]/div/div/input'
searchbox_dashboard_xpath   = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[1]/div[3]/div[1]/div/div/input'
search_table_recod_xpath    = '//*[@id="root"]/div/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div'
notification_xpath          = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[1]/header/div/img[1]'
notification_button_xpath   = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div'
start_at_xapth              = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[5]/div/div[1]/div/div[2]/div/div[2]/div/div/span/span[1]/input'
notification_create_xpath   = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[5]/div/div[3]/div[1]/button'
notification_close_xpath    = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/header/div/div[1]'
result_close_xpath          = '/html/body/div[2]/div[3]/div/header/div/button'
save_execute_on_xpath       = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/button'
select_all_commontype_xpath = '//*[@id="top_panel"]/div/div[2]/div[1]/div/div[2]/div[4]/button'
share_btn_xpath             = '/html/body/div[2]/div[3]/div/header/div/div/button'
flow_xpath                  = '//*[@id="root"]/div/div/div[1]/div/div/header/div/div[2]/div/div/div/button[1]'
excution_xpath              = '//*[@id="root"]/div/div/div[1]/div/div/header/div/div[2]/div/div/div/button[2]'
settings_xpath              = '//*[@id="root"]/div/div/div[1]/div/div/header/div/div[2]/div/div/div/button[3]'
settings_searchbox_xpath    = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[1]/div[1]/div/input'
new_connection_xpath        = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[1]/div[2]/button'
input_data_tag_xpath        = '//*[@id="simple-tab-1"]'
input_config_tag_xpath      = '//*[@id="simple-tab-0"]'
data_search_table_xpath     = '//*[@id="top_panel"]/div/div[2]/div[3]/div[1]/div/div/div/div[1]'
sql_column_xpath            = '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[6]/span/*[name()="svg"]'
detail_xpath                = '/html/body/div[2]/div[3]/div/div/div/div/div[1]/div[3]/span[2]'
summary_select_xpath        = '/html/body/div[2]/div[3]/div/div/div/div/div[1]/div[2]/div/div/div[1]'
action_on_first_flow_xpath  = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div/button'
search_flow_xpath           = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div/div[1]/div[2]/div[1]/div/div/input'
manual_upload_xpath         = '//*[@id="top_panel"]/div/div[2]/div[2]/div[1]/div[2]'
dataset_format_xpath        = '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[1]'
manual_upload_validate_xpath = '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div[1]/button'
viewedit_xpath              = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[8]/div/div/*[name()="svg"]'
exportToPDF_xpath           = '/html/body/div[2]/div[3]/div/div/div/div/div[2]/div/div[1]/a/button'
                              
def init_selenium():
    chromeOptions = webdriver.ChromeOptions()
    
    if _platform == "linux" or _platform =="linux2":
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_argument("--remote-debugging-port=9222")
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument("lang=ja_JP") 
        chromeOptions.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        driver = webdriver.Chrome(chrome_options=chromeOptions)
    elif _platform == "darwin":
        chromeOptions.add_argument("--remote-debugging-port=9222")
        chromeOptions.add_argument("start-maximized")
        chromeOptions.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        driver = webdriver.Chrome()
    elif _platform == "win32" or _platform == "win64":
        chromeOptions.add_argument("--remote-debugging-port=9222")
        chromeOptions.add_argument("start-maximized")
        chromeOptions.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        driver = webdriver.Chrome('chromedriver.exe',chrome_options=chromeOptions)
        
    driver.implicitly_wait(10)
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
        time.sleep(WAIT5)

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
        time.sleep(WAIT10)

        print('open workspace')

    except Exception as e:
        print(e)
        ret = 0
        pass

    return ret

# action to open a dashboard
def open_dashboard(driver):
    ret = 1
    try:
        btn_dashboard = driver.find_element_by_xpath(excution_xpath)
        btn_dashboard.click()
        time.sleep(WAIT5)

        print('open dashboard')
    except Exception as e:
        print(e)
        ret = 0
    return ret

# action to move element
def drop_element_to_position(driver, js, element, x, y):
    index = elements.index(element)
    xpath = element_xpath[index]
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
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]')))
    element.click()

    time.sleep(WAIT1)
    db_value = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div')))
    items = db_value.find_elements_by_xpath('./div')
    
    for item in items:
        if (item.text == db):
            item.click()
            break
    
    time.sleep(WAIT3)
    print('select db set')
    return

# action to select db
def select_db(driver):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]')))
    element.click()
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/div/div')))
    element.click()
    time.sleep(WAIT3)
    print('select db name')    
    return

# action to select db table
def select_db_with_index(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]')))
    element.click()
    
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/div/div[' + str(index) + ']')))
    element.click()
    
    time.sleep(WAIT5)
    print('select db name')    
    return

# click to maximize button on select columns, data_compare
def click_maximize_for_select_columns(driver):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[1]/header/div/div/*[name()="svg"]')))
    element.click()
    return

# action to select table item for 'select columns' or 'remove_duplicate'
def click_select_tableitem_for_select_columns(driver, index):
    db_select = driver.find_element_by_xpath(table_sc_xpath)
    db_select.click()
    time.sleep(WAIT1)

    db_value = driver.find_element_by_xpath(table_sc_val_xpath + '[' + str(index) + ']')
    db_value.click()
    time.sleep(WAIT1)
    print('select table item')
    return
    
# action to click one item of table
def select_table(driver, index):
    xpath = '//input[@id="' + index + '"]'
#    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element = driver.find_element_by_xpath(xpath);
    element.click()
    print('select table ' + str(index))
    return

# action to click one item of column type
def select_item_from_column_type(driver, index):
    xpath = '//*[@id="' + index + '"]'
    city = driver.find_element_by_xpath(xpath)
    city.click()

    print('select item from column type ' + str(index))
    return

# action to click data type of column type
def select_item_from_column_data_type(driver, index):
    xpath = "//*[@id='top_panel']/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div/div[4]/div/div[1]/div[1]"
    city = driver.find_element_by_xpath(xpath)
    city.click()
    time.sleep(WAIT1)
    item_xpath = "//*[@id='top_panel']/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div/div[4]/div/div[2]/div/div[" + str(index) + "]"
    item_value = driver.find_element_by_xpath(item_xpath)
    item_value.click()
    time.sleep(WAIT1)
    print('select item from column type ' + str(index))
    return

# action to click data type of column type list
def select_item_from_column_data_type_list(driver, index1, index2):
    xpath = '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[' + str(index1) + ']/div/div[4]/div/div/div[1]'
    city = driver.find_element_by_xpath(xpath)
    city.click()
    time.sleep(WAIT1)

    item_xpath = '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[' + str(index1) + ']/div/div[4]/div/div[2]/div/div[' + str(index2) + ']'
    item_value = driver.find_element_by_xpath(item_xpath)
    item_value.click()
    time.sleep(WAIT1)
    print('select item from column type ' + str(index1) + ":" + str(index2))
    return

# action to click all check of table
def click_all_select(driver):
    btn_select_all = driver.find_element_by_xpath(select_all_xpath)
    btn_select_all.click()
    
    print('select all the table')
    time.sleep(WAIT1)
    return

# action to click 'Add Selected' button
def click_add_select_btn(driver):
    btn_add = driver.find_element_by_xpath(btn_addSelected)
    btn_add.click()
    time.sleep(WAIT3)

    print('add selected click')
    return

# connecting
def connect_all_elements(driver):
    entry1 = driver.find_elements_by_xpath('//div[@id="drop-location"]/div')[1]
    entry2 = driver.find_elements_by_xpath('//div[@id="drop-location"]/div')[3]
    entry3 = driver.find_elements_by_xpath('//div[@id="drop-location"]/div')[5]

    action = ActionChains(driver)
    action.click_and_hold(entry1).move_to_element(entry3).release(entry3).perform()
    time.sleep(WAIT1)

    action.click_and_hold(entry2).move_to_element(entry3).release(entry3).perform()
    time.sleep(WAIT1)

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
    time.sleep(WAIT1)

    print('connected')
    return


# select 'cell By cell Compare' item
def cell_by_cell_compare(driver, index):
    db_select3 = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div/div/div/div/div')))
    db_select3.click()
    print("db open")

    db_select_val3 = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div/div/div/div[2]/div/div[' + str(index) + ']')))
    db_select_val3.click()
    print("selected")
    return

# select mapping tab
def select_mapping_tab(driver):
    tab_mapping = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, tabmapping_xpath)))
    tab_mapping.click()
    print('mapping tab selected')
    return

# selct mapping table name
def add_mapping_table_name(driver):
    table = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, table1_xpath)))
    table.click()
    
    table_value = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, table1_val_xpath)))
    table_value.click()
    
    table = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, table2_xpath)))
    table.click()

    table_value = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, table2_val_xpath)))
    table_value.click()

    plus = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, mapplus_xpath)))
    plus.click()

    print('mapping table names')
    return

# adding table on type compare mapping tab
def add_mapping_table_for_type_compare(driver):
    table = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tableContainer"]/div[2]/div[1]/div/div/div[1]')))
    table.click()
    
    table_value = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tableContainer"]/div[2]/div[1]/div/div[2]/div/div')))
    table_value.click()
    
    table = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tableContainer"]/div[2]/div[2]/div/div/div[1]')))
    table.click()

    table_value = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tableContainer"]/div[2]/div[2]/div/div[2]/div/div')))
    table_value.click()

    plus = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tableContainer"]/div[2]/div[3]/img')))
    plus.click()

    print('adding mapping table')
    return

# select mapping table item
def select_mapping_table_item(driver, index):
    table_item = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tableContainer"]/table/tbody/tr[' + str(index) + ']/td[2]')))
    table_item.click()
    print('select mapping table item')
    return

#select primary key for data compare table item
def select_primary_key_for_type_compare(driver, index):
    input_key = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[1]/span/span[1]')))
    input_key.click()
    print('select key for table item')
    return

# select key for table item
def select_key_for_table_item(driver, index):
    # 2020/07/23 for 009
    input_key = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[1]/span/span[1]')))
    input_key.click()
    print('select key for table item')
    return

def select_key_for_warning_mapping_tableitem(driver, keyindex):
    tables_tr = driver.find_elements_by_xpath('//*[@id="tableContainer"]/table/tbody/tr')
    count = len(tables_tr)
    for i in range(count):
        try:
            img = driver.find_element_by_xpath('//*[@id="tableContainer"]/table/tbody/tr[' + str(i + 1) + ']/td[4]/img')
            table_item = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tableContainer"]/table/tbody/tr[' + str(i + 1) + ']/td[2]/span[1]')))
            table_item.click()
            input_key = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[' + str(keyindex) + ']/div/div[1]/span/span[1]')))
            input_key.click()
            time.sleep(WAIT1)
        except Exception as e:
            pass
    return

# action to click save button
def click_save_on_cp(driver):
    btn_done = driver.find_element_by_xpath(done_sc_xapth)
    btn_done.click()
    print('click done')
    return    

# action to input random on data compare
def input_random_sample_on_data_compare(driver, value):
    input_random = driver.find_element_by_xpath(random_input_xpath)
    input_random.send_keys(value)
    return

# select rule on data quality
def select_rule_on_dataquality(driver, index):
    driver.execute_script("document.getElementById('top_panel').scrollTop = 0;")
    
    select_rule = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[1]/div/div/div[1]')
    select_rule.click()

    select_rule_item = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div/div[' + str(index) + ']')
    select_rule_item.click()
    print('select rule on data quality')
    return

# select table on data quality
def select_table_on_dataquality(driver, index):
    select_table = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/div[1]')
    select_table.click()

    select_table_item = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[' + str(index) + ']')
    select_table_item.click()
    print('select table on data quality')
    return

# select column on data quality
def select_column_on_dataquality(driver, index):
    select_column = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div[1]')
    select_column.click()

    select_column_item = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[' + str(index) + ']')
    select_column_item.click()
    print('select column on data quality')
    return

# select operator on data quality
def select_operator_on_dataquality(driver, index):
    select_operator = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[3]/div/div/div[1]')
    select_operator.click()

    select_operator_item = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[2]/div/div[' + str(index) + ']')
    select_operator_item.click()
    print('select operator on data quality')
    return

# insert rule value on data quality
def insert_rulevalue_on_dataquality(driver, value):
    rule_value = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/input')
    rule_value.send_keys(value)
    print('insert value on data quality')
    return

# apply button on data quality
def apply_button_on_dataquality(driver):
    apply_button = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[5]/button')
    apply_button.click()
    print('apply on data quality')
    return

# initialize on data quality
def initialize_on_dataquality(driver, index1, index2, index3, index4, value):
    select_rule_on_dataquality(driver, index1)
    select_table_on_dataquality(driver, index2)
    select_column_on_dataquality(driver, index3)
    select_operator_on_dataquality(driver, index4)    
    apply_button_on_dataquality(driver)
    time.sleep(WAIT3)
    return

# initialize on data quality
def initialize_on_dataquality_for_select_rule(driver, index1, index2, index3, value):
    # only TABLE_SIZE value for Select Rule
    select_rule_on_dataquality(driver, index1)
    select_table_on_dataquality(driver, index2)
    select_operator_on_dataquality(driver, index3)    
    apply_button_on_dataquality(driver)
    time.sleep(WAIT3)
    return

# insert sql on data quality
def insert_sql_on_dataquality(driver, sql):
    sql_rule = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[2]/textarea[1]')
    sql_rule.send_keys(sql)

# action sql on data quality
def add_sql_on_dataquality(driver, index, sql, job):
    select_rule_on_dataquality(driver, index)
    insert_sql_on_dataquality(driver, sql)
    job_name = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/input')
    job_name.send_keys(job)
    apply = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div/div[1]/div[4]/button')
    apply.click()
    
# save and excute workflow
def save_excute_workflow(driver, flow_name):
    name_field = driver.find_element_by_xpath(name_xpath)
    name_field.send_keys(Keys.CONTROL + 'a') 
    name_field.send_keys(Keys.DELETE)
    name_field.send_keys(flow_name)

    btn_save = driver.find_element_by_xpath(save_xpath)
    btn_save.click()
    time.sleep(WAIT3)

    print('executing...')
    btn_execute = driver.find_element_by_xpath(excute_xpath)
    btn_execute.click()

    try:
        btn_result = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, result_xpath)))
        btn_result.click()
    except Exception as e:
        pass
    
    WebDriverWait(driver, WAITDRIVER).until(EC.url_contains("show-result"))
    time.sleep(WAIT3)

    return

def save_excute_workflow_without_rename(driver):
    btn_save = driver.find_element_by_xpath(save_xpath)
    btn_save.click()
    time.sleep(WAIT3)

    print('executing...')
    btn_execute = driver.find_element_by_xpath(excute_xpath)
    btn_execute.click()

    try:
        btn_result = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, result_xpath)))
        btn_result.click()
    except Exception as e:
        pass
    
    WebDriverWait(driver, WAITDRIVER).until(EC.url_contains("show-result"))
    time.sleep(WAIT3)

    return

# select all for common type and select column
def click_select_all_for_commontype(driver):
    select_all_button = driver.find_element_by_xpath(select_all_commontype_xpath)
    select_all_button.click()
    print('select all the table')
    time.sleep(WAIT1)
    return

# check summary in final result
def check_summary_in_final_result(driver, class_name, summary_xpath):
    print(class_name + ' result:')
    
    try:
        check = isElementPresentForResult(driver, result_txt_xpath)
        if check != True:
            raise Exception()
        
        result_txt = driver.find_elements_by_xpath(result_txt_xpath)
        if (len(result_txt) == 1):
            if (result_txt[0].text == 'No mismatch in the table'):
                print('No mismatch in the table')
                return
    except Exception as e:
        pass

    if (summary_xpath == ''):
        return
    
    summary_table = driver.find_element_by_xpath(summary_xpath)
    table_trs = driver.find_elements_by_xpath(summary_xpath + '/div')

    flag = 0
    try:
        for i in range(0, len(table_trs)):
            tr = driver.find_element_by_xpath(summary_xpath + '/div[' + str(i + 1) + ']')
            inner_tr = driver.find_element_by_xpath(summary_xpath + '/div[' + str(i + 1) + ']/div')
            
            className = inner_tr.get_attribute("class")
            if className.find("padRow") != -1:
                break
            
            tds = driver.find_elements_by_xpath(summary_xpath + '/div[' + str(i + 1) + ']/div/div')
            
            output = ''
            find = 0
            for j in range(0, len(tds)):
                try:
                    td = driver.find_element_by_xpath(summary_xpath + '/div[' + str(i + 1) + ']/div/div[' + str(j + 1) + ']')
                    img_xpath = summary_xpath + '/div[' + str(i + 1) + ']/div/div[' + str(j + 1) + ']/img'
                    check = isElementPresentForResult(driver, img_xpath)
                    
                    if check != True:
                        raise Exception()

                    img_element = driver.find_element_by_xpath(img_xpath)
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
        pass
    
    if (flag == 0):
        print('No mismatch in the table')
    return

# add columns for datacompare's table item
def add_columns_in_datacompare_tableitem(driver):
    column1 = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[1]/div[1]/div/div/div[1]')
    column1.click()
    driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div[3]').click()

    column2 = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/div[1]')
    column2.click()
    driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[3]').click()

    driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[1]/div[3]').click()
    return

# click to share button
def click_share_button_and_close(driver):
    share_btn = driver.find_element_by_xpath(share_btn_xpath)
    share_btn.click()
    time.sleep(WAIT1)
    print("share link : " + driver.find_element_by_xpath('//*[@id="share-link-textfield"]').get_attribute("value"))
    copy_btn = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[3]/button[1]')
    copy_btn.click()
    close_btn = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[3]/button[2]')
    close_btn.click()
    return

# check summary in final result for TC014
def check_summary_statue_in_final_result(driver, class_name, summary_xpath):
    print(class_name + ' result:')

    summary_table = driver.find_element_by_xpath(summary_xpath)
    table_trs = summary_table.find_elements_by_xpath('./div')

    flag = 0
    try:
        for tr in table_trs:
            inner_tr = tr.find_element_by_xpath('./div')
            tds = inner_tr.find_elements_by_xpath('./div')

            output = ''
            find = 0
            print("{} {} {}".format(tds[1].text, tds[7].text, tds[9].find_element_by_xpath('./span').text))
    except Exception as ex:
        print(ex)
        pass

    time.sleep(WAIT10)

    return;

# check summary in final result for TC007, TC009
def check_summary_in_fianl_mismatched_count(driver, class_name, summary_xpath):
    print(class_name + ' result:')

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

    time.sleep(WAIT10)
    return

# action to search on dashboard
def input_searchbox_on_dashboard(driver, value):
    searchbox = driver.find_element_by_xpath(searchbox_dashboard_xpath)
    searchbox.send_keys(Keys.CONTROL + 'a')
    searchbox.send_keys(Keys.DELETE)
    searchbox.send_keys(value)
    time.sleep(WAIT1)

    try:
        records = driver.find_elements_by_xpath(search_table_recod_xpath)
    except Exception as e:
        records = []
    
    return len(records)

# action to click notification on dashboard()
def click_notification(driver):
    try:
        notification = driver.find_element_by_xpath(notification_xpath)
        notification.click()
    except Exception as e:
        print(e)
        pass
    return

# action to click tab on notification board
def click_tab_on_notification_board(driver, index):
    button = driver.find_element_by_xpath(notification_button_xpath + '/button[' + str(index) + ']')
    button.click()
    print('open notification dialog')
    return

# action to set start time    
def set_start_time_with10(driver):
    driver.find_element_by_xpath(start_at_xapth).click()
    now_plus_10 = datetime.now() + timedelta(minutes = 1)
    current_min = now_plus_10.minute
    current_hour = now_plus_10.hour
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[5]/div/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div/select/option[@id="' + str(current_hour) + '"]')
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[5]/div/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/select/option[@id="' + str(current_min) + '"]')
    driver.find_element_by_xpath(notification_create_xpath).click()
    driver.find_element_by_xpath(notification_close_xpath).click()
    print('set time')
    return

# action to click result close
def click_result_close(driver):
    try:
        elements = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, result_close_xpath)))
        elements.click()
        time.sleep(WAIT3)
    except Exception as e:
        print(e)
    return

# action select cluster on notification dialog
def select_cluster_execute_job(driver, index):
    try:
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div[1]').click()
        time.sleep(WAIT1)
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[' + str(index) + ']').click()
        time.sleep(WAIT1)
    except Exception as e:
        pass
    return

# action save and close on execute tab
def save_close_execute_tab(driver):
    driver.find_element_by_xpath(save_execute_on_xpath).click()
    driver.find_element_by_xpath(notification_close_xpath).click()
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button')))
    element.click()
    return

# open excutions
def open_excutions(driver):
    excutions_btn = driver.find_element_by_xpath(excution_xpath)
    excutions_btn.click()
    time.sleep(WAIT5)
    return

# open settings
def open_settings(driver):
    settings_btn = driver.find_element_by_xpath(settings_xpath)
    settings_btn.click()
    time.sleep(WAIT5)
    return

# input keywords to search box in settings board
def search_in_settings(driver, keyword):
    search_input = driver.find_element_by_xpath(settings_searchbox_xpath)
    search_input.send_keys(keyword)
    time.sleep(WAIT3)
    return

# delete on settings board
def click_delete_settings_search(driver):
    try:
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div[6]/div/button[2]').click()
        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[3]/button[2]').click()
        time.sleep(WAIT3)
    except Exception as e:
        pass
    return

# add new connection on settings board
def add_new_connection(driver, index, name, url, user, password):
    driver.find_element_by_xpath(new_connection_xpath).click()
    time.sleep(WAIT10)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div[2]/ul/div[' + str(index) + ']/div').click()
    print('database clicked')

    time.sleep(WAIT3)
    driver.find_element_by_xpath('//*[@id="outlined-bare"]').send_keys(name)
    
    dateTimeObj = datetime.now()
    database_name = 'employee_' + str(dateTimeObj.microsecond)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[1]/div[2]/div[3]/div[1]/div/input').send_keys(database_name)
    
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[1]/div[2]/p/span').click()

    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[1]/div[2]/div/div/div[1]/div/input').send_keys(Keys.CONTROL + 'a') 
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[1]/div[2]/div/div/div[1]/div/input').send_keys(Keys.DELETE)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[1]/div[2]/div/div/div[1]/div/input').send_keys(url)

    absolute_file_path = os.path.abspath("files/mysql-connector-java-8.0.12.jar")
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[1]/div[2]/input').send_keys(absolute_file_path)

    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[2]/div[1]/div/div/input').send_keys(user)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[2]/div[2]/div/div/input').send_keys(password)

    try:
        test_btn = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[3]/div/div[2]/button')))
        test_btn.click()
        
        WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/button'))).click()
    except Exception as e:
        print(e)
        pass

    try:
        create_btn = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/main/div[2]/div/div[2]/div/div/section[3]/div/div[1]/button')))
        create_btn.click()
    except Exception as e:
        print(e)
        pass

    print('new connection added')
    time.sleep(WAIT3)
    return

# click data tab on input
def click_datatab_input(driver):
    driver.execute_script("document.getElementById('top_panel').scrollTop = 0;")
    driver.find_element_by_xpath(input_data_tag_xpath).click()
    time.sleep(WAIT1)
    print('datatab clicked')
    return

# select table item on data tab
def select_tableitem_on_datasearch(driver, index):
    driver.find_element_by_xpath(data_search_table_xpath).click()
    time.sleep(WAIT1)
    driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div[' +  str(index)+ ']').click()
    time.sleep(WAIT1)
    print('select table item on data search')
    return

# input sql on sql column
def input_sql_on_sqlcolumn(driver):
    driver.find_element_by_xpath(sql_column_xpath).click()
    driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/input').send_keys('lower(city_name)')
    driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/span[2]').click()
    time.sleep(WAIT1)
    print('insert sql transformation')
    return

# click summary index
def click_summary_index(driver, index):
    driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div/div[3]/span[2]').click()

    driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[1]/div[2]/div/div/div[1]').click()
    driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[' + str(index) + ']').click()

    rows = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div/div/div/div[2]/div/div/div[1]/div[2]/div')
    for row in rows:
        typevalue = row.find_element_by_xpath('./div/div[1]/div/div[1]').text
        if typevalue == '':
            city_name = row.find_element_by_xpath('./div/div[2]/div/div[2]').text
            print('city name is converted to lower case: ' + city_name)
    return


# clear entry before inputing value
def entry_clear(self, element):
    element.send_keys(Keys.CONTROL + 'a') 
    element.send_keys(Keys.DELETE)
    return

# open config tab on input
def open_config_tab_on_input(driver):
    driver.find_element_by_xpath(input_config_tag_xpath).click()
    time.sleep(WAIT1)
    return

# action to flow page
def click_action_on_flow_page(driver):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, flow_xpath)))
    element.click()
    time.sleep(WAIT5)
    return

# action to first flow
def click_action_on_first_flow(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, action_on_first_flow_xpath)))
    element.click()
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="long-menu"]/div[3]/ul/li[' + str(index) + ']')))
    element.click()
    time.sleep(WAIT5)
    return

# action to find flow
def find_specific_flow(driver, keys):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, search_flow_xpath)))
    element.send_keys(Keys.CONTROL + 'a')
    element.send_keys(Keys.DELETE)
    element.send_keys(keys)
    time.sleep(WAIT3)
    return

# action to click manual upload in input
def click_manual_upload_input(driver):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, manual_upload_xpath)))
    element.click()
    return

# select manual upload dataset format
def select_manual_upload_dataset_format(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, dataset_format_xpath)))
    element.click()
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/div[' + str(index) + ']')))
    element.click()
    return;

# set dataset path
def set_dataset_path(driver, xpath, path):
    element = driver.find_element_by_xpath(xpath)
    element.send_keys(path)
    return

# check multiline manual upload on input
def check_multiline_manual_upload_input(driver):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/span')))
    element.click()
    return

# click manual upload validate
def click_manual_upload_validate(driver, xpath):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    return

# input delimiter on input
def input_delimiter_on_input(driver, value):
    element = driver.find_element_by_xpath('//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[1]/div[2]/div/input')
    element.send_keys(value)
    return

# set header as true or false on input
def set_header_on_input(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div[1]')))
    element.click()
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div[2]/div/div[' + str(index) + ']')))
    element.click()
    return

# set interschema as true or false on input
def set_interschema_on_input(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[3]/div[2]/div/div[1]')))
    element.click()
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[3]/div[2]/div[2]/div/div[' + str(index) + ']')))
    element.click()
    return


# check element present in UI
def isElementPresentForResult(driver, index):
    driver.implicitly_wait(1)
    try:
        driver.find_element_by_xpath(index)
        return True
    except Exception as e:
        return False
    finally:
        driver.implicitly_wait(20)
        
# checkCompleteness
def checkCompletenessOnDataQuality(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[2]/span/span[1]')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    return

# nullCheckOnDataQuality
def nullCheckOnDataQuality(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[3]/div/div/span')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    return

# uniqueCheckOnDataQuality
def uniqueCheckOnDataQuality(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[4]/div/div/span')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    return

# checkLeftSpacesOnDataQuality
def checkLeftSpacesOnDataQuality(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[5]/span')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    return

# checkRightSpacesOnDataQuality
def checkRightSpacesOnDataQuality(driver, index):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[6]/span')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    return

# inputMaxLengthOnDataQuality
def inputMaxLengthOnDataQuality(driver, index, value):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[7]/div/div/input')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.send_keys(value);
    return

# inputMinLengthOnDataQuality
def inputMinLengthOnDataQuality(driver, index, value):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[8]/div/div/input')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.send_keys(value)
    return

# inputRegularExpressOnDataQuality
def inputRegularExpressOnDataQuality(driver, index, value):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[12]/div/div/textarea')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.send_keys(value)
    return

# inputSQLWhereConditionOnDataQuality
def inputSQLWhereConditionOnDataQuality(driver, index, value):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[11]/div/div/textarea')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.send_keys(value)
    return

# inputMaxValueOnDataQuality
def inputMaxValueOnDataQuality(driver, index, value):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[9]/div/div/input')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.send_keys(value)
    return

# inputMinValueOnDataQuality
def inputMinValueOnDataQuality(driver, index, value):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[' + str(index) + ']/div/div[10]/div/div/input')))
    if index > 7:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    element.send_keys(value)
    return

# clickNextButtonOnDataQuality
def clickNextButtonOnDataQuality(driver):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[3]/button')))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    return

# scrollToTop
def scrollToTop(driver):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top_panel"]/div/div[3]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]')))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    return

# clickViewEditActionOnExcutions
def clickFirstViewEditActionOnExcutions(driver):
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, viewedit_xpath)))
    element.click()
    return

# check summary in final result for TC028
def check_summary_statue_in_TC028_result(driver, class_name, summary_xpath):
    print(class_name + ' result:')

    summary_table = driver.find_element_by_xpath(summary_xpath)
    table_trs = summary_table.find_elements_by_xpath('./div')

    flag = 0
    try:
        for tr in table_trs:
            inner_tr = tr.find_element_by_xpath('./div')
            tds = inner_tr.find_elements_by_xpath('./div')

            output = ''
            find = 0
            print("{} {} {}".format(tds[2].find_element_by_xpath('./div').text, tds[5].find_element_by_xpath('./div').text, tds[6].find_element_by_xpath('./div/span').text))
            
        button = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div/div[2]/div[2]/div/div[3]/button')))
        
        if button.is_enabled() and button.is_displayed():
            button.click()
            summary_table = driver.find_element_by_xpath(summary_xpath)
            table_trs = summary_table.find_elements_by_xpath('./div')
            
            for tr in table_trs:
                inner_tr = tr.find_element_by_xpath('./div')
                tds = inner_tr.find_elements_by_xpath('./div')

                output = ''
                find = 0
                print("{} {} {}".format(tds[2].find_element_by_xpath('./div').text, tds[5].find_element_by_xpath('./div').text, tds[6].find_element_by_xpath('./div/span').text))
    except Exception as ex:
        print(ex)
        pass

    time.sleep(WAIT10)

    return

# Upload Json Flow File
def onUploadJsonFlowFile(driver, filePath):
    element = driver.find_element_by_xpath('//*[@id="upload-image1"]')
    absolute_file_path = os.path.abspath("files/" + filePath)
    element.send_keys(absolute_file_path)
    element = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/input')
    element.send_keys("TC_036_JSON")
    element = WebDriverWait(driver, WAITDRIVER).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[3]/div[1]')))
    element.click()
    return
    
