import sys
import tkinter
from tkinter import messagebox,ttk
from loguru import logger
import hashlib
import json
import datetime
import requests
from bs4 import BeautifulSoup
import textwrap
import subprocess
import time
from urllib.parse import quote, unquote
from better_goods_choose.android_appium.appium_schedule import appium_schedule
import os



local_time = datetime.datetime.now()

limited_search_dict = {}


def init():
    default = {}
    default_name = 'test_name'
    default_code = 'test_code'
    default_name = hashlib.sha256(default_name.encode()).hexdigest()
    default_code = hashlib.sha256(default_code.encode()).hexdigest()
    default['name'] = default_name
    default['code'] = default_code
    with open('verify.json','w') as f:
        # print(default)
        write_content = json.dumps(default,ensure_ascii=False)
        f.write(write_content)

def get_weather():
    craw_url = 'https://tianqi.2345.com/'
    r = requests.get(craw_url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'})
    if r.status_code == 200:
        soup = BeautifulSoup(r.content,'lxml')
        # logger.info(soup.prettify())
        today_conditions_source = soup.find('div',class_='banner-right-con')
        today_conditions_source_1 = today_conditions_source.find('div')
        today_conditions = today_conditions_source_1.find_all('div',class_='banner-right-con-list-item')
        # logger.info(today_conditions)
        # logger.info(len(today_conditions))
        if len(today_conditions) == 0:
            messagebox.showinfo('网页已更新,需再次定位....')
        else:
            for i in today_conditions:
                i_soup = BeautifulSoup(str(i), 'lxml')
                text_content = i_soup.text.strip()
                better_text_content = textwrap.wrap(text_content)
                # logger.info(better_text_content)
                if '今天' in text_content:
                    logger.info(better_text_content)
                    return text_content
                else:
                    pass
    else:
        logger.info(r.status_code)

def subprocess_process():
    sub_driver = subprocess.Popen('cmd',shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,creationflags=subprocess.CREATE_NEW_CONSOLE)
    sub_driver.stdin.write(b'e: \n')
    sub_driver.stdin.write(b'cd python_projects \n')
    sub_driver.stdin.write(b'cd better_goods_choose \n')
    sub_driver.stdin.write(b'cd better_goods_choose \n')
    sub_driver.stdin.write(b'cd spiders \n')
    sub_driver.stdin.write(b'dir \n')
    sub_driver.stdin.write(b'exit \n')
    # sub_driver.stdin.write(b'scrapy crawl better_goods_choose \n')
    sub_driver.stdin.flush()
    sub_driver.wait()
    spider_names =  sub_driver.stdout.readlines()

    file_name_source = []
    file_names = []
    for name in spider_names:
        name =name.decode('gbk')
        # logger.info(name)
        # logger.info('######################################')
        if '.py' in name:
            file_name_source.append(name)
        else:
            pass
    # logger.info(file_names)
    for a in file_name_source:
        each_py_name_source = a.split()[-1]
        each_py_name_source = each_py_name_source.replace('.py','').strip()
        # logger.info(each_py_name_source)
        # logger.info('$$$$$$$$$$$$$$$$$$$$$$')
        if '__init__' in each_py_name_source:
            pass
        else:
            file_names.append(each_py_name_source)
    ############获取爬虫文件名后构建指令##############
    ############获取爬虫文件名后构建指令##############
    ############获取爬虫文件名后构建指令##############

    logger.info(file_names)
    for name in file_names:
        subprocess.run(
            ['scrapy', 'crawl',name],
            cwd= r'E:\python_projects\better_goods_choose\better_goods_choose',
        )


def make_up_search_url():
    def quit_make_up_page():
        if messagebox.askyesno('tips','确认退出当前页面？'):
            make_url_root.destroy()
    def inner_make_up_search_url():
        if len(get_search_content.get()) ==0:
            messagebox.showwarning('error','invalid input')
        else:
            if messagebox.askyesno('tips','当前搜索的内容为:{}\n是否继续？'.format(get_search_content.get())):
                necessary_param = quote(get_search_content.get())
                make_url_root.destroy()
                #############构造路径#######################
                default_path = r'E:\python_projects\better_goods_choose\better_goods_choose\spiders'
                file_name = 'search_history'
                make_up_full_path = os.path.join(default_path,file_name)
                logger.debug(f'make_up_full_path:{make_up_full_path}')
                with open(f'{make_up_full_path}.json','w') as f:
                    history_content = {
                        # 'quote_content': unquote(necessary_param),
                        'after_quote':necessary_param,
                        'dang_dang_net' : 'https://search.dangdang.com/?key={}&act=input'.format(necessary_param),
                        'jd_net' : 'https://search.jd.com/Search?keyword={}'.format(necessary_param),
                        'taobao_net' : 'https://new-s.taobao.com/?q={}'.format(necessary_param),
                        ##############在此添加对应网址####################
                    }
                    write_content = json.dumps(history_content,ensure_ascii=False)
                    f.write(write_content)

                limited_search_dict['search_content'] = get_search_content.get()
                logger.info('链接信息已存储成功。。。。')
                make_url_root.withdraw()
                make_url_root.destroy()



    make_url_root = tkinter.Tk()
    make_url_root.title('自主搜索')

    tkinter.Label(make_url_root,text='搜索内容:').grid(row=0,column=0,columnspan=2,sticky=tkinter.W)
    get_search_content = ttk.Entry(make_url_root,width=40)
    get_search_content.grid(row=0,column=2,columnspan=2,sticky=tkinter.W)

    ttk.Button(make_url_root,text='下一步',command=inner_make_up_search_url).grid(row=1,column=0,columnspan=2,sticky=tkinter.W)
    quit_button = ttk.Button(make_url_root,text='quit',command=quit_make_up_page)
    quit_button.grid(row=1,column=2,columnspan=2,sticky=tkinter.W)

    make_url_root.mainloop()


def appium_guideline():
    def get_search_content():
        def inner_get_search_content():
            appium_root.destroy()
            appium_root.quit()
            if search_entry.get() is None:
                messagebox.showwarning('error','invalid input')
            else:
                if messagebox.askyesno('tips',f'确认?\n你搜索的内容为:{search_entry.get()}\n是否继续?'):
                    messagebox.showinfo('tips','进程即将开始....\n需要的时间较长......\n点击确认以继续....')
                    appium_schedule(schedule_search_content=search_entry.get())
                    search_root.destroy()

        search_root = tkinter.Tk()
        search_root.title('搜索窗口')
        ttk.Label(search_root, text='搜索内容:').grid(row=1, column=0, columnspan=2)
        search_entry = ttk.Entry(search_root)
        search_entry.grid(row=1, column=2, columnspan=4)
        ttk.Button(search_root,text='next',command=inner_get_search_content).grid(row=2,column=0,columnspan=2)

        search_root.mainloop()

    def quit_appium_guideline():
        if messagebox.askyesno('tip','确认退出当前页面?'):
            appium_root.destroy()

    appium_root = tkinter.Tk()
    appium_root.title('手机端指引')

    ttk.Button(appium_root,text='search',command=get_search_content).pack(side=tkinter.LEFT)
    ttk.Button(appium_root,text='quit',command=quit_appium_guideline).pack(side=tkinter.RIGHT)

    appium_root.mainloop()



def main():
    ###########初始化搜索结果###############
    with open('goods_messages.txt', 'w', encoding='utf-8') as f:
        f.write('')
    ###########初始化搜索结果###############
    messagebox.showinfo('请先登录','后才可进行相关进程.....')
    init()
    def inner_main():
        with open('verify.json', 'r') as f:
            loads_data = json.load(f)
            logger.info(loads_data)

            logger.info(f'{first_input.get()},{second_input.get()}')

            if len(first_input.get()) == 0 or len(second_input.get()) == 0:
                messagebox.showwarning('error', 'invalid input! try again')
            else:
                if messagebox.askyesno('tips', '确定登录?'):
                    first_input_ = hashlib.sha256(str(first_input.get()).strip().encode()).hexdigest()
                    second_input_ = hashlib.sha256(str(second_input.get()).strip().encode()).hexdigest()
                    if loads_data['name'] == first_input_ and loads_data['code'] == second_input_:
                        logger.info('已成功登录.....')
                        messagebox.showinfo('登陆成功!', f"欢迎使用! 用户:{first_input.get()}\n今天的天气是:{get_weather()}\n祝你有个好心情!")
                        root.destroy()

                        make_up_search_url()
                        subprocess_process()
                        if messagebox.askyesno('提示','电脑端已爬取完毕,是否进行手机端?'):
                            appium_guideline()

                    else:
                        logger.info('未完成登录.....')
                        messagebox.showwarning('登陆失败', '账号或密码错误,请重试!')

    root = tkinter.Tk()
    root.title('登录界面')

    tkinter.Label(root,text='当前时间为:{}'.format(local_time)).grid(row=0,column=0,columnspan=4)
    tkinter.Label(root,text='user:').grid(row=1,column=0,columnspan=2)
    first_input = ttk.Entry()
    first_input.grid(row=1,column=2,columnspan=4)

    tkinter.Label(root,text='password:').grid(row=2,column=0,columnspan=2)
    second_input = ttk.Entry(show='*')
    second_input.grid(row=2,column=2,columnspan=4)

    ensure_login = ttk.Button(root,text='login',command=inner_main)
    ensure_login.grid(row=3,column=0,columnspan=2)

    quit_login = ttk.Button(root,text='quit',command=root.destroy)
    quit_login.grid(row=3,column=2,columnspan=2)

    root.mainloop()

def necessary_main():
    if messagebox.askyesno('tips', '相关信息已保存成功!是否打开?'):
        subprocess.run(
            r'E:\python_projects\better_goods_choose\better_goods_choose\goods_messages.txt',
        )
    else:
        messagebox.showinfo('提示',r'文件储存的路径是: E:\python_projects\better_goods_choose\better_goods_choose\goods_messages.txt')

if __name__ == '__main__':
    # main()
    # get_weather()
    # subprocess_process()
    # make_up_search_url()
    # soft_url()
    main()
    # necessary_main()
    # appium_guideline()




