# -*- coding: utf-8 -*-

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



# 检查是否联网，并进行联网
def check_ping():
    return1 = os.system('ping www.baidu.com')
    ping_num = 0
    if return1:
        print('*' * 50, '网络断开，正在联网', '*' * 50)
        url = 'http://10.220.250.50/0.htm'
        name = '2017112839@cmcc'
        password = '16003x'
        try:
            driver = webdriver.Chrome(
                "I:\安装包\Chrome6503325146x86\GoogleChrome_65.0.3325.146_x86\ChromePortable\App\Google Chrome\chromedriver.exe")  # 调用chrome浏览器
            driver.maximize_window()  # 窗口最大化
            driver.get(url)
            time.sleep(1)
            driver.refresh()  # 刷新方法 refresh
            # 开始定位，模拟输入，id对应标签的id，检查可知
            zh_elem = driver.find_element_by_id("lg00")
            zh_elem.send_keys(name)
            mm_elem = driver.find_element_by_id("lg01")
            mm_elem.send_keys(password)
            dl_elem = driver.find_element_by_id("lg02")
            dl_elem.click()
            check_ping()
        except:
            ping_num += 1
            time.sleep(600)
            if ping_num == 10:
                time.sleep(600)
                print('*' * 50, '学校网络太差，十分钟后尝试重连', '*' * 50)
            if ping_num == 100:
                return 'null'
            check_ping()
    else:
        print('*' * 50, '网络已连接', '*' * 50)
