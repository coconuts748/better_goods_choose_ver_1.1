import sys
import time
import textwrap
from selenium.common import NoSuchElementException
from loguru import logger
from better_goods_choose.android_appium.appium_settings import default_appium_driver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as e_conditions
from selenium.webdriver.support.wait import WebDriverWait
from tenacity import retry, stop_after_attempt,wait_random,retry_if_exception_type

def pdd_script(search_content):
    pdd_driver = default_appium_driver()
    wait = WebDriverWait(pdd_driver, 20)


    pdd_feature = '//android.widget.TextView[@text="拼多多"]'
    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, pdd_feature))).click()

    top_search_feature = '//android.widget.TextView[@content-desc="搜索"]'
    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, top_search_feature))).click()

    edit_search_feature = '//android.widget.EditText[@content-desc="搜索"]'
    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH,edit_search_feature))).send_keys(search_content)
    ensure_search_feature = '//android.widget.TextView[@text="搜索"]'
    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, ensure_search_feature))).click()

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_random(min=1, max=2),
        retry = retry_if_exception_type(Exception)
    )
    def quit_pdd():
        pdd_driver.back()
        pdd_driver.back()
        pdd_driver.back()
        pdd_driver.back()
        pdd_driver.back()
        pdd_driver.back()
        if wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, pdd_feature))):
            pdd_driver.quit()
    quit_pdd()

if __name__ == '__main__':
    pdd_script(search_content='aaaa')
