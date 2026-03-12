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

def taobao_script(search_content):
    tao_bao_store_path = r'E:\python_projects\better_goods_choose_ver_1.1\goods_messages.txt'


    taobao_driver = default_appium_driver()
    wait = WebDriverWait(taobao_driver, 20)

    tao_bao_feature = '//android.widget.TextView[@text="淘宝"]'
    top_search_column_feature = '//android.view.View[@content-desc="搜索栏"]'
    top_search_edit_feature = '//android.widget.EditText[@resource-id="com.taobao.taobao:id/searchEdit"]'
    top_ensure_search_feature = '//android.widget.Button[@text="搜索"]'

    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, tao_bao_feature))).click()
    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, top_search_column_feature))).click()
    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, top_search_edit_feature))).click()
    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, top_search_edit_feature))).send_keys(search_content)
    wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, top_ensure_search_feature))).click()

    ###############爬取数据部分###############
    """
    主节点: //androidx.recyclerview.widget.RecyclerView
    商品节点: .//android.view.ViewGroup
    """
    main_basic_cite = '//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup'

    ensure_goods_num = wait.until(e_conditions.presence_of_all_elements_located((AppiumBy.XPATH, main_basic_cite)))
    logger.info(len(ensure_goods_num))
    for i in range(1, len(ensure_goods_num) + 1):
        i_feature = f'//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[{i}]/android.view.ViewGroup/android.view.ViewGroup/android.view.View[3]'
        i_title = wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, i_feature))).get_attribute(
            'content-desc')
        logger.info(i_title)
        try:
            with open(tao_bao_store_path, 'a') as f:
                write_content = f'{i_title}\n'
                f.write(write_content)

        except Exception as a:
            logger.debug(a)

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_random(min=1, max=2),
        retry=retry_if_exception_type(Exception)
    )
    def back_process():
        taobao_driver.back()
        taobao_driver.back()
        taobao_driver.back()
        taobao_driver.back()
        taobao_driver.back()
        taobao_driver.back()
        if wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, tao_bao_feature))):
            logger.info('已返回至首页.....')
            taobao_driver.quit()

    back_process()




if __name__ == '__main__':
    taobao_script(search_content='手机')
