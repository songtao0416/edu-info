# -*- coding: utf-8 -*-
from WeChat_search_url import get_wechat_main
from WeChat_gzh_url import get_wechat_gzh_main
import base_list
import time
from WeChat_mysql import mysql_main
from email_neibu import send_email_NB
from email_url import email_url_main

# 微信数据爬取主函数,独自运行
def WeChat_Main_DZ():
    start = time.clock()
    search_keys = base_list.keywords
    # search_keys = ["香港"]
    gzh_list = '华中师范大学'
    # 根据关键词获取wechat的data
    search_count = get_wechat_main(search_keys)
    # 根据关键词再指定公众号中搜索data
    gzh_count = 0
    # gzh_count = get_wechat_gzh_main(search_keys, gzh_list)
    wechat_count = search_count + gzh_count
    print("*" * 20, "共插入数据%s条" % wechat_count, "*" * 20)
    # 计算程序爬取用时
    end = time.clock()
    today_time_s = end - start
    wechat_time = str(round(today_time_s / 3600, 2)) + '小时'
    # 发送邮件
    send_email_NB(wechat_time, wechat_count)
    email_url_main(wechat_time, wechat_count, wechat_count)

# 微信数据爬取主函数,辅助运行
def WeChat_Main():
    # 获取关键词和公众号列表
    search_keys = base_list.keywords
    # search_keys = ["香港"]
    gzh_list = '华中师范大学'
    # 根据关键词获取wechat的data
    search_count = get_wechat_main(search_keys)
    # 根据关键词再指定公众号中搜索data
    gzh_count = 0
    # gzh_count = get_wechat_gzh_main(search_keys, gzh_list)
    wechat_count = search_count + gzh_count
    print("*" * 20, "共插入数据%s条" % wechat_count, "*" * 20)
    return wechat_count


# WeChat_Main_DZ()
