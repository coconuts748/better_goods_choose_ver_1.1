from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as e_conditions
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from appium.options.android import UiAutomator2Options
import subprocess
from loguru import logger



def get_appium_param():
    logger.info('get_appium_param')
    origin_sub_driver = subprocess.Popen(
        'cmd',
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE

    )
    origin_sub_driver.stdin.write(b'adb devices \n')
    origin_sub_driver.stdin.write(b'exit \n')
    origin_sub_driver.stdin.flush()
    return_results = origin_sub_driver.stdout.readlines()

    for i,i_num in zip(return_results,range(len(return_results))):
        return_result = i.decode('gbk')
        if 'List' in return_result:
            # logger.info(return_result)
            device_name_byte = return_results[i_num + 1 ].decode('gbk')
            # logger.info(device_name_byte)
            device_name = str(device_name_byte).replace('device', '').strip()
            logger.info(device_name)
            return device_name
        else:
            pass


def default_appium_driver():
    device_params = {
        'DeviceName': get_appium_param(),
        'platformName' : 'Android',
        'noReset': True,
        'automationName': 'uiautomator2'
    }

    make_up_options_params = UiAutomator2Options()
    make_up_options_params.load_capabilities(device_params)

    appium_driver = webdriver.Remote('http://169.254.190.0:4723',options=make_up_options_params)

    return appium_driver


if __name__ == '__main__':
    default_appium_driver()
