# -*- coding: utf-8 -*-
# 利用百度的高级搜索，在不同网站上，检索关键词的搜索结果，并获取每条搜索结果的标题和URL

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import re
import datetime
from check_ping import check_ping

website = 'https://www.baidu.com'

# 保存到csv中
def open_csv(adds,mkpath):
    path = mkpath + '/(URL)'+adds + '.csv'
    csvfile = open(path, 'a+', encoding='utf-8', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(('文章编号', '文章标题', '文章url', '文章时间'))
    return writer

# 爬取最新URL，打开url，搜索keyword，获取当前页面的href，返回urls
def open_url(search_type):
    driver = webdriver.Chrome("I:\安装包\Chrome6503325146x86\GoogleChrome_65.0.3325.146_x86\ChromePortable\App\Google Chrome\chromedriver.exe") # 调用chrome浏览器
    driver.maximize_window()    #窗口最大化
    driver.get(website)
    time.sleep(1)
    # 开始定位，模拟输入，id对应标签的id，检查可知
    elem = driver.find_element_by_id("kw")
    elem.send_keys(search_type)
    elem.send_keys(Keys.ENTER)
    time.sleep(1)
    # 获取打开的多个窗口句柄
    windows = driver.window_handles
    # 切换到当前最新打开的窗口
    driver.switch_to.window(windows[-1])
    # # 切换到资讯
    c_elem = driver.find_element_by_class_name('s_tab_inner').find_element_by_xpath("//a[contains(text(),'资讯')]")
    c_elem.click()
    time.sleep(1)       # 等待时间过短，会导致返回的内容为none，且网速有影响，故设置在5-10s

    # # 点击按时间排序
    # f_elem = driver.find_element_by_class_name('c-icon')
    # f_elem.click()
    # g_elem = driver.find_element_by_class_name('c-tip-menu').find_element_by_xpath('//ul/li/a[contains(text(),"按时间排序")]')
    # g_elem.click()

    # 获取一天内的文章
    # d_elem = driver.find_element_by_class_name('search_tool_tf')
    # d_elem.click()
    # e_elem = driver.find_element_by_id('c-tips-container').find_element_by_link_text('一天内')
    # e_elem.click()
    # time.sleep(2)


    # 获取搜索到的数量
    count = 'null'
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    try:
        c1 = soup.find_all('span', class_='nums')
        pattern = re.compile(r'\d+\S\d+')
        count = re.search(pattern, str(c1)).group()
    except:
        try:
            c1 = soup.find_all('span', class_='nums')
            pattern = re.compile(r'\d+')
            count = re.search(pattern, str(c1)).group()
        except:
            print("未抓取到count")
    print("总共搜索到%s篇内容" % count)


    # 循环点击下一页翻页,并获取href
    # dict = {'title':'','url':''}
    a_urls = []
    a_titles = []
    a_times = []
    i = 1
    while True:
        # 获取当前搜索页面的内容，html
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        print("正在获取第%d页内容" % i)
        # 读取页面内所有a标签中的href/标题和时间
        for k1 in soup.find_all('h3', class_='c-title'):  # 资讯中class为'c-title'，网页中class为't'
        # for k1 in soup.find_all('h3', class_='t'):  # 资讯中class为'c-title'，网页中class为't'
            try:
                k = k1.find('a')
                # dict['url'] = k["href"]
                # dict['title'] = k.text.strip()
                # dict的之变化后，list中的dict值居然也会变化，dict可能类似指针，dict的浅拷贝和深拷贝,于是换用两个list分别存储url和title
                a_urls.append(k["href"])
                a_titles.append(k.text.strip())
            except:
                print("获取url,erreo")
        # 读取页面所有文章的发布时间
        for k2 in soup.find_all('p', class_='c-author'):      # 资讯中class为'c-author'，网页中class为'newTimeFactor_before_abs'
        # for k2 in soup.find_all('span', class_='newTimeFactor_before_abs'):
            try:
                k = k2.text
                t_pattern = re.compile(r"(\d{4}\S\d{1,2}\S\d{1,2})")
                s1 = re.search(t_pattern, ''.join(k)).group(0)
                s2 = re.sub('年', '-', s1)
                a_time = re.sub('月', '-', s2)
                if a_time == 'null':
                    a_time = str(datetime.date.today())
                a_times.append(a_time)
            except:
                a_time = str(datetime.date.today())
                a_times.append(a_time)
        # 开始翻页
        try:
            a = driver.find_element_by_id('page').find_element_by_partial_link_text('下一页')
            a.click()
            time.sleep(2)
        except:
            print("翻页,erreo")
        i = i + 1
        try:
            if i == 2:  # 获取前2页，约20篇
                break
        except:
            print('最尾页,erreo')
            break
    # 获取爬取的结果数量
    r_count = len(a_urls)
    print("总共搜爬取%d篇内容" %r_count)
    print(driver.title)
    driver.close()
    return a_urls,a_titles,a_times,count

# 爬取历史url
def open_url_old(search_type):
    driver = webdriver.Chrome("I:\安装包\Chrome6503325146x86\GoogleChrome_65.0.3325.146_x86\ChromePortable\App\Google Chrome\chromedriver.exe") # 调用chrome浏览器
    driver.maximize_window()    #窗口最大化
    driver.get(website)
    time.sleep(1)
    # 开始定位，模拟输入，id对应标签的id，检查可知
    elem = driver.find_element_by_id("kw")
    elem.send_keys(search_type)
    elem.send_keys(Keys.ENTER)
    time.sleep(1)
    # 获取打开的多个窗口句柄
    windows = driver.window_handles
    # 切换到当前最新打开的窗口
    driver.switch_to.window(windows[-1])
    time.sleep(1)       # 等待时间过短，会导致返回的内容为none，且网速有影响，故设置在5-10s

    # 循环点击下一页翻页,并获取href
    a_urls = []
    a_titles = []
    a_times = []
    i = 1
    while True:
        # 获取当前搜索页面的内容，html
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        print("正在获取第%d页内容" % i)
        # 读取页面内所有a标签中的href/标题和时间
        for k1 in soup.find_all('h3', class_='t'):  # 资讯中class为'c-title'，网页中class为't'
            try:
                k = k1.find('a')
                a_urls.append(k["href"])
                a_titles.append(k.text.strip())
            except:
                print("获取url,erreo")
        # 读取页面所有文章的发布时间
        for k2 in soup.find_all('span', class_='newTimeFactor_before_abs'):
            try:
                k = k2.text
                t_pattern = re.compile(r"(\d{4}\S\d{1,2}\S\d{1,2})")
                s1 = re.search(t_pattern, ''.join(k)).group(0)
                s2 = re.sub('年', '-', s1)
                a_time = re.sub('月', '-', s2)
                if a_time == 'null':
                    a_time = str(datetime.date.today())
                a_times.append(a_time)
            except:
                a_time = str(datetime.date.today())
                a_times.append(a_time)
        # 开始翻页
        try:
            a = driver.find_element_by_id('page').find_element_by_partial_link_text('下一页')
            a.click()
            time.sleep(2)
        except:
            print("翻页,erreo")
        i = i + 1
        try:
            # 此处为第i页，判断是否存在i+1页，若没有则结束
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            tail_pages = soup.find('div',id='page').find_all('span', class_='pc')
            tail_pagee = []
            for tail_page in tail_pages:
                tail_pagee.append(str(tail_page.get_text()))
            if str(i+1) not in tail_pagee:
                break
        except:
            print('最尾页,erreo')
            break
    # 获取爬取的结果数量
    r_count = len(a_urls)
    print("总共搜爬取%d篇内容" %r_count)
    print(driver.title)
    driver.close()
    return a_urls,a_titles,a_times,r_count

# 正则表达式去掉无效url,去重
def get_urls(a_urls,a_titles,a_times):
    # # 去空值
    # a_urls = list(filter(None, (a_urls,a_titles)))
    # print('空值',a_urls)
    # 去重复
    lis1 = []
    lis2 = []
    lis3 = []
    for i in range(0,len(a_urls)):
        if a_urls[i] not in lis2:
            lis1.append(a_times[i])
            lis2.append(a_urls[i])
            lis3.append(a_titles[i])
    times = lis1
    urls = lis2
    titles = lis3
    return urls,titles,times

# 存储到csv文件中
def save_url(urls,titles,writer,times):
    i = 1
    for s_url in urls:
        writer.writerow((str(i),titles[i-1],s_url,times[i-1]))
        i = i + 1
    return i

def search_url(search_type, url_adds,mkpath):
    writer = open_csv(url_adds,mkpath)
    try:
        # 根据关键词获取所有搜索页面的url
        (a_urls,a_titles,a_times,count) = open_url(search_type)  #只爬取第一页
        #(a_urls, a_titles, a_times, count) = open_url_old(search_type)  # 全部爬取，网页，翻页
    except:
        # 可能是网络断开，重新连接
        check_ping()
        (a_urls, a_titles, a_times, count) = open_url(search_type)
    (urls,titles,times) = get_urls(a_urls,a_titles,a_times)                     #将url进行处理，去重，去无效，去空值
    print(urls)
    save_url(urls,titles,writer,times)              #将url结果保存到csv文件中
    return count
