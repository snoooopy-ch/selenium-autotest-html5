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

#BASE_URL = 'http://dataq-frontend.s3-website.us-east-2.amazonaws.com/#/user-home/flow'
#BASE_URL = 'http://dataq-automation-alb-1598668034.us-east-1.elb.amazonaws.com:9000'

def str2Class(str):
    return getattr(sys.modules[__name__], str)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--url", help="input site url, default 'http://dataq-automation-alb-1598668034.us-east-1.elb.amazonaws.com:9000'")
    parser.add_argument("-u", "--user", help="input login user, default 'john'")
    parser.add_argument("-p", "--password", help="input login pass, default 'dataq'")
    parser.add_argument("-s", "--scripts", help="input script number to execute using comma")
    parser.add_argument("-a", "--all", help="input for all scripts", action="store_true")
    args = parser.parse_args()

    if args.url:
        url = agrs.url
    else:
        url = 'http://dataq-automation-alb-1598668034.us-east-1.elb.amazonaws.com:9000'
    
    print(url)

    if args.user:
        user = args.user
    else:
        user = "john"

    print(user)

    if args.password:
        password = args.password
    else:
        password = "dataq"

    print(password)

    if args.scripts:
        scpt_number = [int(item) for item in args.scripts.split(',')]
    else:
        scpt_number = [1,2,3,4,5,6,7,8,9,11,12,13,15,16,19,20,21,22,23,24,25,26,27]
        
    if args.all:
        scpt_number = [1,2,3,4,5,6,7,8,9,11,12,13,15,16,19,20,21,22,23,24,25,26,27]

    print(scpt_number)

    driver = qcd.init_selenium() 
    try:
        driver.get(url)
        driver.set_window_size(1920, 1080)

    	# login page loading...
        time.sleep(qcd.WAIT1)
        
        runTotal = len(scpt_number)
        passedTotal = 0
        failedTotal = 0
        
        passedNumbers = []
        failedNumbers = []
        try:
            # login
            if (qcd.login(driver, user, password) != 1):
                raise Exception('fail to login')

            startTotal = time.time()
            for index in scpt_number:
                print("================")
                start_time = time.time()
                try:
                    driver.refresh()
                    TCCLASS = str2Class("TC" + str(index).zfill(3))
                    tc = TCCLASS(driver)
                    tc.test()
                    
                    passedTotal = passedTotal + 1
                    passedNumbers.append(index)
                except Exception as e:
                    failedTotal = failedTotal + 1
                    failedNumbers.append(index)
                    pass
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

        time.sleep(qcd.WAIT1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        qcd.logger.warning("Exception : {} : {}".format(e, traceback.format_exc()))
        print("exception:{}".format(e))
    finally:
        driver.quit()
    
    sys.exit()
