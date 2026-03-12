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
import os



def jd_script(search_content):
    jd_store_path = r'E:\python_projects\better_goods_choose_ver_1.1\goods_messages.txt'

    jd_driver = default_appium_driver()
    wait = WebDriverWait(jd_driver, 20)

    jd_feature = '//android.widget.TextView[@text="京东"]'

    def inner_jd_script():
        try:
            wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, jd_feature))).click()
            try:
                top_search_column_feature = '//android.widget.TextView[@content-desc="搜索栏"]'
                top_search_column_location = wait.until(
                    e_conditions.presence_of_element_located((AppiumBy.XPATH, top_search_column_feature)))
                top_search_column_location.click()

                logger.info(search_content)

                top_input_feature = '//android.widget.EditText'
                top_input = wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, top_input_feature)))
                top_input.send_keys(search_content)

                ensure_search_button_feature = '//android.widget.TextView[@text="搜索"]'
                ensure_search_button = wait.until(
                    e_conditions.presence_of_element_located((AppiumBy.XPATH, ensure_search_button_feature)))
                ensure_search_button.click()

                ###############爬取部分####################
                """
                商品主节点来源 : '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.jd.lib.search.feature:id/a4e"]'
                搜索后会出现商品,可滑动,
                """
                def craw_part():
                    all_goods_element_feature = '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.jd.lib.search.feature:id/a4e"]/android.widget.FrameLayout'
                    all_goods_num = len(wait.until(
                        e_conditions.presence_of_all_elements_located((AppiumBy.XPATH, all_goods_element_feature))))
                    logger.info(all_goods_num)

                    for i in range(1, all_goods_num + 1):
                        # title_feature = '(//android.widget.LinearLayout[@resource-id="com.jd.lib.search.feature:id/xi"])[{}]/android.widget.TextView'.format(
                        #     i)
                        title_feature = f'//androidx.recyclerview.widget.RecyclerView[@resource-id="com.jd.lib.search.feature:id/a4e"]/android.widget.FrameLayout[{i}]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup'
                        title = wait.until(
                            e_conditions.presence_of_element_located((AppiumBy.XPATH, title_feature))).get_attribute(
                            'content-desc').strip()
                        prepare_title = str(title).replace(r'\200b', '').replace(r'\u200b', '').strip()
                        logger.info(prepare_title)
                        logger.debug('@@@@@@@@@@@@@@@@@@@@')
                        try:
                            with open(jd_store_path, 'a') as f:
                                write_content = f'{prepare_title}\n'
                                f.write(write_content)

                        except Exception as a:
                            logger.debug(a)


                craw_part()  #一次
                jd_driver.swipe(749, 3058, 749, 872)
                @retry(
                    stop=stop_after_attempt(5),
                    wait=wait_random(min=1, max=2),
                    retry=retry_if_exception_type(Exception),
                )
                def back_process():
                    jd_driver.back()
                    jd_driver.back()
                    jd_driver.back()
                    jd_driver.back()
                    jd_driver.back()
                    jd_driver.back()
                    if wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, jd_feature))):
                        logger.info('已返回至首页....')
                        jd_driver.quit()

                back_process()

            except NoSuchElementException:
                jd_driver.quit()

        except NoSuchElementException:
            jd_driver.quit()

    inner_jd_script()


if __name__ == '__main__':
    jd_script(search_content='雨伞')

    # test_driver = default_appium_driver()
    # wait = WebDriverWait(test_driver, 30)
    #
    # title_feature = '(//android.widget.LinearLayout[@resource-id="com.jd.lib.search.feature:id/xi"])[1]/android.widget.TextView'
    # title = wait.until(e_conditions.presence_of_element_located((AppiumBy.XPATH, title_feature))).get_attribute('text')
    # logger.info(title)

