from better_goods_choose.android_appium.appium_scripts.taobao import taobao_script
from better_goods_choose.android_appium.appium_scripts.jd import jd_script
from better_goods_choose.android_appium.appium_scripts.pdd import pdd_script
from tenacity import retry,retry_if_exception_type,stop_after_attempt,wait_random
from loguru import logger

def appium_schedule(schedule_search_content):

    def schedule():
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_random(min=1, max=2),
            retry=retry_if_exception_type(Exception)
        )
        def inner_taobao():
            taobao_script(search_content=schedule_search_content)

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_random(min=1, max=2),
            retry=retry_if_exception_type(Exception)
        )
        def inner_jd():
            jd_script(search_content=schedule_search_content)

        inner_taobao()
        inner_jd()

    schedule()

if __name__ == '__main__':
    appium_schedule(schedule_search_content='雨伞')
