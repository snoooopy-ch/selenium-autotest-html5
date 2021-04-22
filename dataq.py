import argparse
import traceback
import time
import sys
import tc_common as qcd

from tc_001 import TC001
from tc_002 import TC002
from tc_003 import TC003
from tc_004 import TC004
from tc_005 import TC005
from tc_006 import TC006
from tc_007 import TC007
from tc_008 import TC008
from tc_009 import TC009
#from tc_010 import TC010
from tc_011 import TC011
from tc_012 import TC012
from tc_013 import TC013
#from tc_014 import TC014
from tc_015 import TC015
from tc_016 import TC016
#from tc_017 import TC017
#from tc_018 import TC018
from tc_019 import TC019
from tc_020 import TC020
from tc_021 import TC021
from tc_022 import TC022
from tc_023 import TC023
from tc_024 import TC024
from tc_025 import TC025
from tc_026 import TC026
from tc_027 import TC027
from tc_028 import TC028
from tc_029 import TC029
from tc_030 import TC030
from tc_031 import TC031
from tc_032 import TC032
from tc_033 import TC033
from tc_034 import TC034
from tc_035 import TC035
from tc_036 import TC036
from tc_037 import TC037
from tc_038 import TC038
from tc_039 import TC039
from tc_040 import TC040
from tc_041 import TC041
from tc_042 import TC042
from tc_043 import TC043
from tc_044 import TC044
from tc_045 import TC045
from tc_046 import TC046
from tc_047 import TC047
# from tc_049 import TC049
from tc_050 import TC050
from tc_051 import TC051
from tc_052 import TC052
from tc_053 import TC053
from tc_054 import TC054
from tc_055 import TC055
from tc_056 import TC056
from tc_057 import TC057
from tc_058 import TC058
from tc_059 import TC059
from tc_060 import TC060
from tc_061 import TC061
from tc_062 import TC062
from tc_063 import TC063
from tc_064 import TC064
from tc_065 import TC065
from tc_066 import TC066
from tc_067 import TC067
from tc_068 import TC068
from tc_069 import TC069
from tc_070 import TC070
from tc_071 import TC071
from tc_072 import TC072
from tc_073 import TC073
from tc_074 import TC074
from tc_075 import TC075
from tc_076 import TC076
from tc_077 import TC077
from tc_078 import TC078
from tc_079 import TC079
from tc_080 import TC080
from tc_081 import TC081
from tc_082 import TC082
from tc_083 import TC083
from tc_084 import TC084
from tester import DTESTER

def str2Class(str):
    return getattr(sys.modules[__name__], str)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--url", help="input site url, default 'http://dataq-frontend.s3-website.us-east-2.amazonaws.com/#/user-home/flow'")
    parser.add_argument("-u", "--user", help="input login user, default 'tarun'")
    parser.add_argument("-p", "--password", help="input login pass, default 'dataq123'")
    parser.add_argument("-s", "--scripts", help="input script number to execute using comma")
    parser.add_argument("-a", "--all", help="input for all scripts", action="store_true")
    parser.add_argument("-t", "--tester", help="test saved scripts", action="store_true")
    args = parser.parse_args()

    if args.url:
        url = agrs.url
    else:
        url = 'http://dataq-frontend.s3-website.us-east-2.amazonaws.com/#/user-home/flow'
    
    print(url)

    if args.user:
        user = args.user
    else:
        user = "john"

    print(user)

    if args.password:
        password = args.password
    else:
        password = "dataq123"

    print(password)

    if args.scripts:
        scpt_number = [int(item) for item in args.scripts.split(',')]
    else:
        scpt_number = [1,2,3,4,5,6,7,8,11,12,13,15,19,22,23,25,26,27,28,29,30,31,32,33,35,36,37,38,39,40,41,43,44,45,46,47,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,68,69,71,72,73,74,76,77,78,79,80,81,82,83,84]
        
    if args.all:
        scpt_number = [1,2,3,4,5,6,7,8,11,12,13,15,19,22,23,25,26,27,28,29,30,31,32,33,35,36,37,38,39,40,41,43,44,45,46,47,51,52,53,54,55,56,57,58,59,60,61,62,63,64,66,67,68,69,71,72,73,74,76,77,78,79,80,81,82,83,84]

    if args.tester:
        scpt_number = ['tester']
        
    print(scpt_number)

    runTotal = len(scpt_number)
    passedTotal = 0
    failedTotal = 0
    
    passedNumbers = []
    failedNumbers = []
    try:
        startTotal = time.time()
        for index in scpt_number:
            try:
                try:
                    driver = qcd.init_selenium() 
                    driver.get(url)
                    driver.refresh()
        
                    try:
                        alert = driver.switch_to.alert
                        alert.accept()
                    except:
                        pass
        
                    driver.set_window_size(1920, 1080)

                    # login page loading...
                    time.sleep(qcd.WAIT1)

                    print("================")            
                    print("TC{} start".format(str(index).zfill(3)))
                    # login
                    if (qcd.login(driver, user, password) != 1):
                        raise Exception('fail to login')
                
                    start_time = time.time()

                    driver.get(url)
                    driver.refresh()
                    
                    if index == 'tester':
                        TCCLASS = str2Class('DTESTER')
                    else:
                        TCCLASS = str2Class("TC" + str(index).zfill(3))
                        
                    tc = TCCLASS(driver)
                    tc.test()
                    
                    if index != 41:
                        qcd.logout(driver)
                    
                    passedTotal = passedTotal + 1
                    passedNumbers.append(index)
                except Exception as e:
                    failedTotal = failedTotal + 1
                    failedNumbers.append(index)
                    print("exception:{}".format(e))
                    
                    if driver.current_url != 'http://dataq-frontend.s3-website.us-east-2.amazonaws.com/#/':
                        qcd.logout(driver)
                    pass
                
            except Exception as e:
                pass
            finally:
                driver.quit()
            
            end_time = time.time()
            print("TC{} execution time: {} seconds".format(str(index).zfill(3), end_time - start_time))

        endTotal = time.time()
        print("Ran {} tests".format(runTotal))
        print("Passed {} tests".format(passedTotal))
        print("Failed {} tests".format(failedTotal))
        print("Passed Scirpts: {}".format(passedNumbers))
        print("Failed Scirpts: {}".format(failedNumbers))
        print("Total execution time: {} seconds".format(endTotal - startTotal))
    except Exception as e:
        print(e)
        pass
    finally:
        pass
    
    time.sleep(qcd.WAIT1)
    sys.exit()
