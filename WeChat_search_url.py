# 先搜狗微信获取URL、公众号，两种
# 再针对URL获取内容
# 添加到数据库中,爬完一个关键词就存一个,防止反爬
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import datetime
from WeChat_get_data import get_data
from WeChat_mysql import mysql_main
import base_list

# 模拟器打开微信，搜索关键词，获取URL
def open_url(key_word):
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
    time.sleep(15)
    # 获取打开的多个窗口句柄
    windows = driver.window_handles
    # 切换到当前最新打开的窗口
    driver.switch_to.window(windows[-1])
    # # # 切换到资讯
    # c_elem = driver.find_element_by_class_name('s_tab_inner').find_element_by_xpath("//a[contains(text(),'资讯')]")
    # c_elem.click()
    # time.sleep(1)       # 等待时间过短，会导致返回的内容为none，且网速有影响，故设置在5-10s

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
            # 发布获取时间
            for tm in k2.find_all('span',  class_='s2'):
                tm = tm.text.strip()
                res = r'(?<=\)\))\S+'
                # list_tm数据类型为list
                list_tm = re.findall(res, tm)
                str_tm = ''.join(list_tm)
                today_t = str(datetime.date.today())
                if '小时前' in str_tm:
                    str_tm = today_t
                if '分钟前' in str_tm:
                    str_tm = today_t
                time_list.append(str_tm)
        # 获取url和title
        for k3 in k1.find_all('h3'):
            for k in k3.find_all('a'):
                url_list.append(k["data-share"])
                title_list.append(k.text.strip())
    # 翻页，每页10条信息
    # try:
    #     print("正在翻页")
    #     a = driver.find_element_by_link_text('下一页')
    #     a.click()
    #     time.sleep(2)
    #     # 报道url在ul中的li中的h3中，分别遍历获取URL和Title
    #     for k1 in soup.find_all('ul', class_='news-list'):
    #         # 获取公众号名称
    #         for k2 in k1.find_all('div', class_='s-p'):
    #             for au in k2.find_all('a', class_='account'):
    #                 author_list.append(au.text.strip())
    #             # 发布获取时间
    #             for tm in k2.find_all('span', class_='s2'):
    #                 tm = tm.text.strip()
    #                 res = r'(?<=\)\))\S+'
    #                 # list_tm数据类型为list
    #                 list_tm = re.findall(res, tm)
    #                 str_tm = ''.join(list_tm)
    #                 today_t = str(datetime.date.today())
    #                 if '小时前' in str_tm:
    #                     str_tm = today_t
    #                 if '分钟前' in str_tm:
    #                     str_tm = today_t
    #                 time_list.append(str_tm)
    #         # 获取url和title
    #         for k3 in k1.find_all('h3'):
    #             for k in k3.find_all('a'):
    #                 url_list.append(k["data-share"])
    #                 title_list.append(k.text.strip())
    # except:
    #     driver.refresh()
    #     print("翻页：erro")
    #     print("*" * 100)
    print(title_list)
    print(author_list)
    print(time_list)
    print("一共爬取%s条:" % len(url_list))
    driver.close()
    return url_list, title_list, author_list, time_list

# 公众号名称转换
def get_author(author_list_old):
    author_list = []
    for au in author_list_old:
        au_str = "微信公众号:" + au
        author_list.append(au_str)
    return author_list

# 搜索wechat的主函数
def get_wechat_main(keys):
    count_url = 0
    # 遍历关键词搜索
    for search_types in keys:
        print("*" * 20, "正在搜索：", search_types, "*" * 20)
        for key_word in search_types:
            print("*" * 20, "正在搜索：%s------防止反爬,等待10s------" % key_word,"*" * 20)
            time.sleep(30)
            try:
                (url_list, title_list, author_list_old, time_list) = open_url(key_word)
                author_list = get_author(author_list_old)
                if url_list == []:
                    break
                # 获取url中的正文数据
                context_list = []
                for url in url_list:
                    # #     反爬,降低频率,5s
                    #     time.sleep(5)
                    # 防止url无法爬取,返回提示,存入数据库
                    # try:
                    #     (title, all_context) = get_data(url)
                    # except:
                    #     print("请点击链接查看原文")
                    #     all_context = "请点击链接查看原文"
                    all_context = "请点击链接查看原文"
                    context_list.append(all_context)
                    print(url)
                print("*" * 100)
                # 爬完一个key立即存入数据库
                count = mysql_main(author_list, title_list, time_list, url_list, context_list, key_word)
                #  获取微信文章的数量,count_url为int类型
                count_url = count_url + count
                if count == 0:
                    break
            except:
                print("微信爬取错误,反爬")
                break
    return count_url

# 主函数，控制所有
if __name__ == "__main__":
    # h表示设定的小时
    h1 = 11
    h2 = 0
    # 无线循环执行while下函数
    while True:
        # 判断是否达到设定时间，例如0:00
        today_t = str(datetime.date.today())
        print('*' * 20, "微信爬取程序已启动", '*' * 20)
        while True:
            # 获取当前时间，小时
            now = datetime.datetime.now()
            # 导入数据源，关键词10个 网站列表19个。全局变量，不用传递也可使用
            keys = base_list.keywords
            # 到达下午13点，结束内循环，开始爬取数据
            if now.hour == h1:
                start = time.clock()
                get_wechat_main(keys)
                end = time.clock()
                today_time_s = end - start
                print(today_time_s)
                print('*' * 20, "已经爬取至%s数据,%s:00，次日%s：00开始运行" % (today_t, h1, h2), '*' * 20, )
            elif now.hour == h2:
                get_wechat_main(keys)
                print('*' * 20, "已经爬取至%s,%s:00数据，当日%s:00开始运行" % (today_t, h2, h1), '*' * 20, )
            # 不到时间就等十五分钟之后再次检测
            time.sleep(900)


# mysql_main(['author_list1'], ['weixintitle_list1'], ['2019-08-26'], ['weixinurl_list1'], ['context_listcontext_listcontext_listcontext_listcontext_listcontext_listcontext_list'], 'key_word')
# author_list = ['黑龙江省教育厅']
# title_list = ['国务院教育督导办发布5号预警:防治学生欺凌暴力 建设阳光安全校园']
# time_list = ['23分钟前']
# url_list = ['http://weixin.sogou.com/api/share?timestamp=1567050597&signature=qIbwY*nI6KU9tBso4VCd8lYSesxOYgLcHX5tlbqlMR8N6flDHs4LLcFgRw7FjTAOKB3bbPbu7G7NGo2BzR0lfquCj0gzKc1SLQKk5quQA6SWeap4Yl0LQ0C8kOA9WNZXRgKuK**RttozZwZWPXz8ScwrKwIBTca31Hv6UkDPGhUgxwoyJWfw0mCQR8RBPrg6d2FwwnKPm5NFzwjf3k2ESwOktEMZabZEUom5oUIVsF8=']
# context_list = ['国务院教育督导办发布5号预警:防治学生欺凌暴力 建设阳光安全校园']
# key_word = '教育'
# mysql_main(author_list, title_list, time_list, url_list, context_list, key_word)
# mysql_main(['author_list'], ['weixintitle_list'], ['2019-08-26'], ['weixinurl_list'], ['context_listcontext_listcontext_listcontext_listcontext_listcontext_listcontext_list'], 'key_word')