from search_url import search_url
from search_data import search_data
from topkey import topkey
from hdbs_mysql import hdbs_mysql
from email_report import send_mail
from check_ping import check_ping
from email_url import email_url_main
import base_list
import os
import csv
import re
import xlrd
import xlwt
from xlutils.copy import copy
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from WeChat_main import WeChat_Main


# 创建目录，以keyword命名
def creat_mk(keyword):
    global mkpath
    today_t = str(datetime.date.today())
    mkpath = os.getcwd()+'/'+today_t +'/'+ keyword + '--爬取结果'
    isExists = os.path.exists(mkpath)
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(mkpath)
        print(mkpath + ' 创建成功')
    else:
        print(mkpath + ' 目录已存在')
    return mkpath

# 创建csv/xls文件，保存所有网站的data和搜索count
def save_csv(keyword):
    # 创建文件夹1
    mkpath = creat_mk(keyword)

    # 创建count表，保存各网站统计数量
    count_path = mkpath + '/（统计）'+keyword+'.xls'
    count_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    count_sheet = count_book.add_sheet('test', cell_overwrite_ok=True)
    i = 0
    titles = ['网站序号', '网站名称', '搜索篇数', '实际篇数']
    for title in titles:
        count_sheet.write(0, i, title)
        i += 1

    # 创建all表，保存所有搜索结果的内容
    all_path = mkpath + '/（总数据）'+keyword+'.csv'
    csvfile = open(all_path, 'a+', encoding='utf-8', newline='')
    all_writer = csv.writer(csvfile)
    all_writer.writerow(('文章编号', '文章来源', '文章标题', "文内标题", "发布时间", "URL链接", "全文", "关键词", "情感分析", "情感属性", "自动摘要"))
    return count_sheet, count_path, all_path, mkpath, count_book, all_writer


# 根据网站id，获取其检索式search-type和文件地址url_adds
def get_key(index,keyword):
    i = int(index)
    s_name = all_webname[i]
    s_url = all_urls[i]
    url_adds = '“' + keyword + '”专题--' + s_name     # 根据情况+xls或+csv
    search_type = 'site:(' + s_url + ') "' + keyword+'"'
    # search_type = 'site:(' + s_url + ') ' + keyword
    print(url_adds, search_type, s_name)
    return url_adds, search_type, s_name


# 根据网站的index，获取其检索结果，包括url和data
def url_data(i, index, count_sheet, count_path, all_path, mkpath, count_book, all_writer, keyword):
    (url_adds, search_type, s_name) = get_key(index, keyword)        # 获取检索式
    print('*' * 20, "正在从%s进行爬取" % s_name, '*' * 20)
    # ******************************************************************************************************************
    # 爬取URL，并写入url
    count = search_url(search_type, url_adds, mkpath)
    # count = 0
    # ******************************************************************************************************************
    # 爬取Data，并写入data
    rel_count = search_data(url_adds, s_name, all_path, mkpath, all_writer)
    # 写入到统计总表中
    i = i+1
    count_sheet.write(i, 0, index)
    count_sheet.write(i, 1, s_name)
    count_sheet.write(i, 2, count)
    count_sheet.write(i, 3, rel_count)
    count_book.save(count_path)
    print('*' * 20, "%s爬取成功" % s_name, '*' * 20)
    return rel_count

# 对all_data中的正文进行关键词分析和情感分析
def get_topkey(all_path):
    # 设置关键词数量
    topkey(all_path)

# 将总数据csv转为总数据xls
def data_xls(all_path):
    # 创建xls
    all_path_xls = all_path+'.xls'
    all_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    all_sheet = all_book.add_sheet('test', cell_overwrite_ok=True)
    # 打开csv
    csv_reader = csv.reader(open(all_path, encoding='utf-8'))
    # 转存
    i = 0
    for row in csv_reader:
        if len(row[6]) < 10000:
            for r_j in range(0, len(row)):
                all_sheet.write(i, r_j, row[r_j])
            i += 1
    all_book.save(all_path_xls)
    return all_path_xls

# 获取网站列表和关键词,用户输入需要搜索的网站，生成待搜索网站list
def select_website():
    print('*'*20,"可选择的网站列表包括",'*'*20)
    i = 0
    for site in all_webname:
        print("网站编号:%d"%i,"     网站名称：%s"%site)
        i = i+1
    print('*' * 20,"请选择需要采集的网站，并输入网站编号",'*' * 20)
    print('*' * 20, "多个编号请用英文逗号','隔开，如需获取所有网站，请输入数字'0'", '*' * 20)
    input_list = input("网站编号:")
    keyword = input("请输入查询关键词:")
    if input_list == '0' :
        index_list = list(range(1,len(all_urls)))       # 输入#获取所有网站
    else:
        index_list = list(filter(str.isdigit,input_list.split(',')))       #只保留数字
    return index_list,keyword

# # GUI界面调用代码
# def gui_start(keyword,input_list):
#     if input_list == '0' :
#         index_list = list(range(1,len(all_urls)))       # 输入#获取所有网站
#     else:
#         index_list = list(filter(str.isdigit,input_list.split(',')))       #只保留数字
#     # 创建csv保存数据
#     (count_sheet, count_path, all_path, mkpath, count_book, all_writer) = save_csv(keyword)
#     print("开始爬取“%s”关键词的内容" % keyword)
#
#     # index对应不同网站编号，通过url_data获取各网站的检索结果
#     counts = 0
#     for i in range(0, len(index_list)):
#         index = index_list[i]
#         rel_count = url_data(i,index,count_sheet, count_path, all_path, mkpath, count_book, all_writer)  # 依次获取网站data
#         counts = counts + rel_count
#     print('*' * 20, "所有网站爬取完毕，共爬取%s条数据" % str(counts), '*' * 20)

    # # 存储到数据库中
    # get_count(keyword, count_path)  # 存到count表
    # get_all_data(keyword, all_path)  # 存到all_data表
    # print('*' * 20, "已写入数据库", '*' * 20)

# 创建日志表，保存每日日志
def rz_file(today_time,todat_i):
    # 打开想要更改的excel文件
    rz_path = os.getcwd() + '/运行日志.xls'
    old_excel = xlrd.open_workbook(rz_path)
    old_ws = old_excel.sheet_by_index(0)
    nrows = old_ws.nrows
    # 将操作文件对象拷贝，变成可写的workbook对象
    new_excel = copy(old_excel)
    # 获得第一个sheet的对象
    ws = new_excel.get_sheet(0)
    today_t = str(datetime.date.today())
    # 原有数据为nrows行，写入数据
    ws.write(nrows, 0, nrows)
    ws.write(nrows, 1, today_t)
    ws.write(nrows, 2, todat_i)
    ws.write(nrows, 6, today_time)
    ws.write(nrows, 7, '已发送4人')
    new_excel.save('运行日志.xls')
    print('*' * 20, "成功存入日志", '*' * 20)

# 传入关键词，调用其它函数,包括创建表、数据获取、关键词分析、数据处理
def gather(keyword):
    # 创建csv保存数据
    (count_sheet, count_path, all_path, mkpath, count_book, all_writer) = save_csv(keyword)
    print("开始爬取“%s”关键词的内容" % keyword)
    # index对应不同网站编号，通过url_data获取各网站的检索结果
    index_list = list(range(1, len(all_urls)))  # 输入#获取所有网站
    counts = 0
    for i in range(0, len(index_list)):
        index = index_list[i]
        rel_count = url_data(i, index, count_sheet, count_path, all_path, mkpath, count_book, all_writer, keyword)  # 依次获取网站data
        counts = counts + rel_count
    print('*' * 20, "所有网站爬取完毕，共爬取%s条数据" % str(counts), '*' * 20)

    # 将总数据csv转为总数据xls,all_path指向xls文件
    # all_path = os.getcwd() + '/' + today_t + '/' + keyword + '--爬取结果' + '/（总数据）' + keyword + '.csv'
    data_xls(all_path)
    # all_xlspath = data_xls(all_path)

    # 关键词分析
    # get_topkey(all_xlspath
    # print("*" * 20, "关键词分析完毕", "*" * 20)
    # 存储到数据库中
    # get_count(keyword,count_path)      #存到count表
    # get_all_data(keyword,all_path)   #存到all_data表
    # print('*' * 20, "已写入数据库", '*' * 20)
# 每日上午循环的主函数
def run_today_02():
    e = 0
    try:
        start = time.clock()
        # 每日爬取数据，尝试map并行处理
        for i in range(1, len(keywords)):
            skeyword = keywords[i]
            print(skeyword)
            for keyword in skeyword:
                try:
                    gather(keyword)
                    print('*' * 20, "“%s”爬取成功" % keyword, '*' * 20)
                except:
                    print('*' * 20, "“%s”爬取失败" % keyword, '*' * 20)
        e = 1
        # 写入hdbs数据库
        today_i = hdbs_mysql()
        # 获取微信数据
        # today_wechat = WeChat_Main()
        # 计算程序爬取用时
        end = time.clock()
        today_time_s = end - start
        today_time = str(round(today_time_s / 3600, 2)) + '小时'
        print("数据爬取用时:", today_time)
        e = 2
        # 发送邮件,第一封为内部邮件，第二封为每日报告
        send_mail(today_time, today_i)
        time.sleep(1800)
        if today_i != 0:
            today_c = today_i + 500
            email_url_main(today_time, today_c)
        time.sleep(10000)
        # 写入日志
        rz_file(today_time, today_i)
    except:
        er = '未知错误'
        if e == 0:
            er = '数据爬取部分出错，请检查search_url和search_data'
        elif e == 1:
            er = '数据库存取部分出错，请检查hdbs_mysql'
        elif e == 2:
            er = '邮件发送部分出错，请检查send_email和email_url'
        send_mail('error', er)
        time.sleep(18000)

# 每日下午循环的主函数
def run_today():
    # # 输入网站列表和关键词
    # (index_list,keyword) = select_website()
    # print(index_list)
    e = 0
    try:
        start = time.clock()
        # 每日爬取数据，尝试map并行处理
        for i in range(1, len(keywords)):
            skeyword = keywords[i]
            print(skeyword)
            for keyword in skeyword:
                try:
                    # 遍历各网站,检索关键词
                    gather(keyword)
                    print('*' * 20, "“%s”爬取成功" % keyword, '*' * 20)
                except:
                    print('*' * 20, "“%s”爬取失败" % keyword, '*' * 20)
        e = 1
        # 网站数据写入hdbs数据库
        today_i = hdbs_mysql()
        # 获取微信数据
        # today_wechat = WeChat_Main()
        # 计算程序爬取用时
        end = time.clock()
        today_time_s = end - start
        today_time = str(round(today_time_s/3600, 2)) +'小时'
        print("数据爬取用时:", today_time)
        e = 2
        # 发送邮件,第一封为内部邮件，第二封为每日报告
        send_mail(today_time, today_i)
        time.sleep(1800)
        if today_i != 0:
            today_c = today_i + 500
            email_url_main(today_time, today_c)
        time.sleep(10000)
        # 写入日志
        rz_file(today_time, today_i)
    except:
        er = '未知错误'
        if e == 0:
            er = '数据爬取部分出错，请检查search_url和search_data'
        elif e == 1:
            er = '数据库存取部分出错，请检查hdbs_mysql'
        elif e == 2:
            er = '邮件发送部分出错，请检查send_email和email_url'
        send_mail('error', er)
        time.sleep(18000)

# 主函数，控制所有
if __name__ == "__main__":
    # h表示设定的小时
    h1 = 14
    h2 = 2
    # 无线循环执行while下函数
    while True:
        # 判断是否达到设定时间，例如0:00
        today_t = str(datetime.date.today())
        print('*' * 20, "媒体信息爬取主程序已启动,请手动启动微信爬取程序", '*' * 20)
        while True:
            # 获取当前时间，小时
            now = datetime.datetime.now()
            # 导入数据源，关键词10个 网站列表19个。全局变量，不用传递也可使用
            keywords = base_list.keywords
            all_webname = base_list.all_webname
            all_urls = base_list.all_urls
            # 到达下午13点，结束内循环，开始爬取数据
            if now.hour == h1:
                # 检查网络情况
                check_ping()
                # 每日下午爬取数据，一天做一次
                run_today()
                print('*' * 20, "已经爬取至%s数据,%s:00，次日%s：00开始运行" % (today_t, h1, h2), '*' * 20, )
            elif now.hour == h2:
                # 检查网络情况
                check_ping()
                # 每日凌晨爬取数据，一天做一次
                run_today_02()
                print('*' * 20, "已经爬取至%s,%s:00数据，当日%s:00开始运行" % (today_t, h2, h1), '*' * 20, )
            # 不到时间就等十五分钟之后再次检测
            time.sleep(900)





