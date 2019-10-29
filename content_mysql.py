# -*- coding: utf-8 -*-
# 将xls中的data数据转存到mysql中
# 连接本地数据库

import pymysql
import csv
import os
import re
from main import *
import sys
import time
import xlrd
import base_list


# 读取 统计 表数据
def open_count(keyword,count_path):
    path = count_path
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    id_list = []
    name_list = []
    nums_list = []
    right_list = []
    for i in range(0, int(sheet.nrows)):
        print(type((sheet.cell(i, 0).value)))
        id_list.append(sheet.cell(i, 0).value)
        name_list.append(sheet.cell(i, 1).value)
        nums_list.append(sheet.cell(i, 2).value)
        right_list.append(sheet.cell(i, 3).value)
    print("%s数据Count读取成功"%keyword)
    return id_list, name_list, nums_list, right_list

# 读取 总数据 表数据
def open_alldata(keyword,all_path):
    path = all_path
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    id_list = []
    web_list = []
    name_list = []
    name2_list = []
    time_list = []
    url_list = []
    data_list = []
    for i in range(0, int(sheet.nrows)):
        id_list.append(sheet.cell(i, 0).value)
        web_list.append(sheet.cell(i, 1).value)
        name_list.append(sheet.cell(i, 2).value)
        name2_list.append(sheet.cell(i, 3).value)
        time_list.append(sheet.cell(i, 4).value)
        url_list.append(sheet.cell(i, 5).value)
        data_list.append(sheet.cell(i, 6).value)
    print("%s数据all_data读取成功" % keyword)
    return id_list, web_list,name_list,name2_list,time_list,url_list,data_list

#  连接数据库
def content_sql():
    global db,cursor
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "yst123456", "skd",charset="utf8")
    # db = pymysql.connect("localhost", "root", "yst123456", "skd")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor= db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    # data = cursor.fetchall()
    print("Database version : %s " % data)
    return cursor

#  数据库查询
def select_sql():
    sql = """SELECT * FROM count """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            name = row[1]
            nums = row[2]
            right_nums = row[3]
            # 打印结果
            print("id=%s,name=%s,nums=%s,right_nums=%s" % \
                  (id, name,nums,right_nums))
    except:
        print("Error: unable to fecth data")

#  count表插入数据  sql
def insert_sql_count(id_list,name_list,nums_list,right_list,keyword):
    content_sql()  # 连接mysql
    # 插入中文时，%s 要改为'%s',且插入的列数量要和数据库相同
    for i in range(1, len(id_list)):
        print(id_list[i], keyword, name_list[i], nums_list[i], right_list[i])
        sql = "INSERT INTO count VALUES ('0', %s,'%s','%s','%s','%s')"%(id_list[i],keyword,name_list[i],nums_list[i],right_list[i])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
           # 如果发生错误则回滚
           print('*'*20,"第%d条插入失败"%i,'*'*20)
           db.rollback()

# all_data表插入数据  sql
def insert_sql_data(id_list, web_list,name_list,name2_list,time_list,url_list,data_list,keyword):
    content_sql()  # 连接mysql
    # 插入中文时，%s 要改为'%s',且插入的列数量要和数据库相同
    i=0
    for i in range(1, len(id_list)):
        sql = "INSERT INTO all_data VALUES ('0','%s','%s','%s','%s','%s','%s','%s','%s')" % (id_list[i], web_list[i], name_list[i],name2_list[i], time_list[i], url_list[i], data_list[i],keyword)
        try:
            if len(data_list[i]) >= 100000:
                print("字数太多，超过10w，pass")
                continue
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            if i % 100 == 0 :
                time.sleep(1)
        except:
            # 如果发生错误则回滚
            print('*' * 20, "第%d条插入失败"%i, '*' * 20)
            db.rollback()
    print("*"*20,"在all_data中共插入%d条数据"%i,"*"*20)

# 数据库更新
def update_sql():
    sql = "UPDATE count SET web_name = 'Bob' WHERE web_id = 1"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        print('*' * 20, "修改失败", '*' * 20)
        db.rollback()

#  数据库删除
def delete_sql():
    # SQL 删除语句
    sql = "DELETE FROM count WHERE id  = 1"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        print('*' * 20, "删除失败", '*' * 20)
        db.rollback()

# 读取 统计xls 数据，写入数据库
def get_count(keyword,count_path):
    (id_list, name_list, nums_list, right_list) = open_count(keyword,count_path)
    # 插入数据
    insert_sql_count(id_list, name_list, nums_list, right_list,keyword)
    db.close()

# 读取 总数据xls 数据，写入数据库
def get_all_data(keyword,all_path):
    (id_list, web_list,name_list,name2_list,time_list,url_list,data_list) = open_alldata(keyword,all_path)
    # 插入数据
    insert_sql_data(id_list, web_list,name_list,name2_list,time_list,url_list,data_list,keyword)
    db.close()


# 关闭数据库连接
if __name__ == "__main__":
# def coon_sql(keyword):
    keywords = base_list.keywords
    for i in range(1, len(keywords)):
        keyword = keywords[i]
        mkpath = os.getcwd() +'/'+ keyword + '--爬取结果'
        count_path = mkpath + '/（统计）'+keyword+'.xls'
        all_path = mkpath + '/（总数据）'+keyword+'.csv.xls'
        get_count(keyword, count_path)
        # get_all_data(keyword, all_path)
