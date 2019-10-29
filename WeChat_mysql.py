# -*- coding: utf-8 -*-
# 将wechat数据存入数据库

from check_ping import check_ping
import pymysql
import time
import xlrd
import base_list
import datetime
from xlutils.copy import copy

# 连接数据库
def content_sql():
    global db,cursor
    try:
        # 打开数据库连接
        db = pymysql.connect("sh-cdb-pk4znli4.sql.tencentcdb.com", "hdbs_education", "ThisNotPsw2019",  "hdbs_education" ,port = 63737, charset="utf8")
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
    except:
        # 检查网络连接
        check_ping()
        content_sql()

# 插入数据库
# def insert_sql_data(id_list, web_list,name_list,name2_list,time_list,url_list,data_list,sub_list, key_list):
def insert_sql_data(author_list, title_list, time_list, url_list, context_list, wechat_sub, key_word):
    content_sql()  # 连接mysql
    # 获取当天爬取时间
    pq_time = str(datetime.date.today())
    # 插入中文时，%s 要改为'%s',且插入的列数量要和数据库相同
    count = 0
    for i in range(0, len(url_list)):
        # print(author_list[i], title_list[i], title_list[i], time_list[i], url_list[i], context_list[i], wechat_sub, key_word, pq_time)
        # sql = "INSERT INTO all_data VALUES ('0','%s','%s','%s','%s','%s','%s','%s','%s')" % (id_list[i], web_list[i], name_list[i],name2_list[i], time_list[i], url_list[i], data_list[i],keyword)
        sql = "INSERT INTO originallink (SOURCE,TITLE,SHORT_DESC,RELEASE_DATETIME,ORIGINAL_LINK,CONTENT,SUBJECT_TYPE,SEARCH_WORDS_NAME,SOURCE_REAL) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
              %(author_list[i], title_list[i], title_list[i], time_list[i], url_list[i], context_list[i], wechat_sub, key_word, pq_time)
        try:
            if len(context_list[i]) >= 100000:
                print("字数太多，超过10w")
                continue
            # if len(context_list[i]) <= 10:
            #     print(context_list[i])
            #     print("字数太少, 不足10")
            #     continue
            # 执行sql语句
            print("正在插入第",i)
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            if i % 100 == 0:
                time.sleep(1)
            count += 1
        except:
            # 如果发生错误则回滚
            print('*' * 20, "第%d条插入失败" % i, '*' * 20)
            db.rollback()
    print("*"*20,"在数据库中共插入%d条数据" % count, "*"*20)
    return count

# 主函数
def mysql_main(author_list, title_list, time_list, url_list, context_list, key_list):
    # 调用数据源中的关键词和主题标识码
    wechat_sub =base_list.sub_list[1]
    # 插入到数据库中
    wechat_count = insert_sql_data(author_list, title_list, time_list, url_list, context_list, wechat_sub, key_list)
    return wechat_count