# -*- coding: utf-8 -*-
# 在指定公众号中搜索关键词，获取data
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import datetime
from WeChat_get_data import get_data
from WeChat_mysql import mysql_main

# 模拟器打开微信，搜索关键词，获取URL
def open_url(key_word, gzh_name):
    driver = webdriver.Chrome("I:\安装包\Chrome6503325146x86\GoogleChrome_65.0.3325.146_x86\ChromePortable\App\Google Chrome\chromedriver.exe")  # 调用chrome浏览器
    driver.maximize_window()  # 窗口最大化
    # 搜狗微信网站
    website = 'https://weixin.sogou.com/'
    driver.get(website)
    time.sleep(1)
    # 开始定位，模拟输入，id对应标签的id，检查可知
    elem = driver.find_element_by_id("query")
    elem.send_keys(key_word)
    elem.send_keys(Keys.ENTER)
    time.sleep(2)
    # 获取打开的多个窗口句柄
    windows = driver.window_handles
    # 切换到当前最新打开的窗口,等待后重新获取drive
    now_handle = driver.current_window_handle
    driver.switch_to.window(now_handle)
    tool = driver.find_element_by_class_name("tool").find_element_by_link_text('搜索工具')
    tool.click()
    time.sleep(1)
    driver.find_element_by_id("search").click()
    time.sleep(1)
    # 公众号内搜索
    gzh = driver.find_element_by_class_name('s-sea')
    gzh.send_keys(gzh_name)
    gzh.send_keys(Keys.ENTER)

    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    url_list = []
    title_list = []
    author_list = []
    time_list = []
    # 报道url在ul中的li中的h3中，分别遍历获取URL和Title
    for k1 in soup.find_all('ul', class_='news-list'):
        # 获取公众号名称
        for k2 in k1.find_all('div', class_='s-p'):
            for au in k2.find_all('a', class_='account'):
                author_list.append(au.text.strip())
            for tm in k2.find_all('span', class_='s2'):
                tm = tm.text.strip()
                res = r'(?<=\)\))\S+'
                tm = re.findall(res, tm)
                today_t = str(datetime.date.today())
                if '小时前' in tm:
                    tm = today_t
                time_list.append(tm)
        # 获取url和title
        for k3 in k1.find_all('h3'):
            for k in k3.find_all('a'):
                url_list.append(k["data-share"])
                title_list.append(k.text.strip())
    # 翻页，每页10条信息
    try:
        print("正在翻页")
        a = driver.find_element_by_link_text('下一页')
        a.click()
        time.sleep(2)
        for k1 in soup.find_all('ul', class_='news-list'):
            # 获取公众号名称
            for k2 in k1.find_all('div', class_='s-p'):
                for au in k2.find_all('a', class_='account'):
                    author_list.append(au.text.strip())
                for tm in k2.find_all('span', class_='s2'):
                    tm = tm.text.strip()
                    res = r'(?<=\)\))\S+'
                    tm = re.findall(res, tm)
                    today_t = str(datetime.date.today())
                    if '小时前' in tm:
                        tm = today_t
                    time_list.append(tm)
            # 获取url和title
            for k3 in k1.find_all('h3'):
                for k in k3.find_all('a'):
                    url_list.append(k["data-share"])
                    title_list.append(k.text.strip())
    except:
        driver.refresh()
        print("翻页：erro")
        print("*" * 100)
    print(url_list)
    print(title_list)
    print(author_list)
    print(time_list)
    print(len(url_list))
    driver.close()
    return url_list, title_list, author_list, time_list

# 公众号名称转换
def get_author(author_list_old):
    author_list = []
    for au in author_list_old:
        au_str = "微信公众号:" + au
        author_list.append(au_str)
    return author_list

# 搜索指定公众号的主函数
def get_wechat_gzh_main(keys):
    count_url = 0
    # 遍历关键词搜索
    for search_types in keys:
        for key_word in search_types:
            print("*" * 20, "正在搜索：%s,防止反爬,等待5s" % key_word, "*" * 20)
            time.sleep(5)
            (url_list, title_list, author_list_old, time_list) = open_url(key_word,"")
            author_list = get_author(author_list_old)
            # 获取url中的正文数据
            context_list = []
            for url in url_list:
                (title, all_context) = get_data(url)
                context_list.append(all_context)
                print(url)
            print("*" * 100)
            # 爬完一个key立即存入数据库
            count = mysql_main(author_list, title_list, time_list, url_list, context_list, key_word)
            #  获取微信文章的数量
            count_url = count_url + count
    return count_url

