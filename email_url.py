#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header
import pymysql
from check_ping import check_ping

# 正常邮件发送
def send_email(subject, cont):
    # @subject:邮件主题
    # @msg :邮件内容
    # @toaddrs:收信人的邮箱地址
    # @fromaddr:发信人的邮箱地址
    # @smtpaddr :smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    # @password :发信人的邮箱密码
    fromaddr = 'yst_super@163.com'
    # 邮箱顺序为：刘俊贵，曹高辉，虞松涛
    toaddrs = ['liujungui2002@163.com', 'bolue@qq.com', '963668943@qq.com']
    # toaddrs = [ '963668943@qq.com']
    # 三个参数：第一个为文本内容，第二y
    # 个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(cont, 'html', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = fromaddr
    message['To'] = ','.join(toaddrs)
    # 测试网络连接
    check_ping()
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        username = 'yst_super@163.com'
        password = 'yst123456'  # 授权码
        smtp.login(username, password)
        smtp.sendmail(fromaddr, toaddrs, message.as_string())
        smtp.quit()
        print("汇报邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# 主函数，编辑邮件内容
def edit_email(today_time, today_i, ids, titles, urls, sources):
    # 获取当日时间
    today_t = str(datetime.date.today())
    # 获取爬取的微信文章数据
    (wechat_ids, wechat_titles, wechat_urls, wechat_sources, today_wechat) = select_sql_wechat()

    # 邮件标题
    subject = "%s教育决策信息平台爬取报告" % today_t
    # 获取真实推送数量
    today_i_real = len(titles) + len(wechat_titles)
    # 媒体报道数据转入html中
    d =''
    for (id, title, url, source ) in zip(ids, titles, urls, sources):
        d = d +"""
            <tr>
                <td>""" + str(id)+ """</td>
                <td>《""" + str(title) + """》</td>
                <td>""" + str(url) + """</td>
                <td>""" + str(source) + """</td>
            </tr>
        """
    # 微信文章数据转入html中
    d_wechat = ''
    for (wechat_id, wechat_title, wechat_url, wechat_source ) in zip(wechat_ids, wechat_titles, wechat_urls, wechat_sources):
        d_wechat = d_wechat +"""
            <tr>
                <td>""" + str(wechat_id)+ """</td>
                <td>《""" + str(wechat_title) + """》</td>
                <td>""" + str(wechat_url) + """</td>
                <td>""" + str(wechat_source) + """</td>
            </tr>
        """
    # 微博文章数据转入html中
    d_weibo = ''
    # for (weibo_id, weibo_title, weibo_url, weibo_source ) in zip(weibo_ids, weibo_titles, weibo_urls, weibo_sources):
    #     d_weibo = d_weibo +"""
    #         <tr>
    #             <td>""" + str(wechat_id)+ """</td>
    #             <td>《""" + str(wechat_title) + """》</td>
    #             <td>""" + str(wechat_url) + """</td>
    #             <td>""" + str(wechat_source) + """</td>
    #         </tr>
    #     """
    #     编辑邮件正文
    cont = """
        <h2>Hi,今日爬取情况如下：</h2>
        <h3><span style="font-family: 微软雅黑;">（1）数据爬取统计</span></h3>
        <table border="1">
          <tr>
            <th>爬取时间</th>
            <th>媒体报道</th>
            <th>微信文章</th>
            <th>微博话题</th>
            <th>今日推送</th>
            <th>爬取用时</th>
          </tr>
          <tr>
            <td>""" + str(today_t) + """</td>
            <td>""" + str(today_i) + """篇</td>
            <td>""" + str(today_wechat) + """篇</td>
            <td>""" + str(today_wechat) + """篇</td>
            <td>""" + str(today_i_real) + """篇</td>
            <td>""" + str(today_time) + """</td>
          </tr>
        </table>
        <p></p>
        <h3><span style="font-family: 微软雅黑;">（2）今日爬取媒体报道：</span></h3>
        <table border="2">
          <tr>
            <th>文章序号</th>
            <th>文章标题</th>
            <th>文章链接</th>
            <th>文章来源</th>
          </tr>
          """+d+"""
        </table>
        
        <h3><span style="font-family: 微软雅黑;">（3）今日爬取微信文章：</span></h3>
        <table border="2">
          <tr>
            <th>文章序号</th>
            <th>文章标题</th>
            <th>文章链接</th>
            <th>公众号名称</th>
          </tr>
          """+d_wechat+"""
        </table>

        <h3><span style="font-family: 微软雅黑;">（4）今日爬取微博信息：</span></h3>
        <table border="2">
          <tr>
            <th>文章序号</th>
            <th>文章标题</th>
            <th>文章链接</th>
            <th>微博账号</th>
          </tr>
          """+d_weibo+"""
        </table>

        <p></p>
        <h3><span style="font-family: 微软雅黑;">（5）快速通道</span></h3>
        <p><a href="http://edu-web.tmsb2b.com/index/main/edu">点击进入教育决策信息平台首页</a></p>
        <p><strong>账号：</strong>edu123edu</p>
        <p><strong>密码：</strong>123456</p>
        <h3>（自动邮件，请勿回复）</h3>

    """
    # 发送邮件
    send_email(subject, cont)

# 标题去重
def del_copy(db_ids, db_titles, db_urls, db_sources):
    db_titles_rel = []
    for title in db_titles:
        print(title)

    pass


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

# 查询当日爬取的媒体报道内容
def select_sql():
    print("正在查询今日媒体爬取数量")
    content_sql()
    today = str(datetime.date.today())
    try:
        # 查询发布时间，返回标题/原文链接/来源
        sql = "SELECT TITLE,ORIGINAL_LINK,SOURCE,RELEASE_DATETIME FROM originallink WHERE SOURCE_REAL = '"+today+"'"
        db_ids = []
        db_titles = []
        db_urls = []
        db_sources =[]
        db_datetime = []
        # try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # print("结果",results)
        # row为tuple类型
        i = 0
        today1 = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        today2 = (datetime.datetime.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        # 获取今日发布的媒体信息
        for row in results:
            # 过滤微信文章
            if 'weixin' not in str(row[1]):
                # 获取发布时间为今日的信息
                if str(row[3]) == today:
                    i += 1
                    db_ids.append(str(i))
                    db_titles.append(row[0])
                    db_urls.append(row[1])
                    db_sources.append(row[2])
                    db_datetime.append(row[3])
        # 今日信息少于10条，则继续推送第二日信息
        if i <= 10:
            for row in results:
                # 过滤微信文章
                if 'weixin' not in str(row[1]):
                    if str(row[3]) == today1:
                        i += 1
                        db_ids.append(str(i))
                        db_titles.append(row[0])
                        db_urls.append(row[1])
                        db_sources.append(row[2])
                        db_datetime.append(row[3])
        # 近两日信息少于10条，则继续推送第三日信息
        if i <= 10:
            for row in results:
                # 过滤微信文章
                if 'weixin' not in str(row[1]):
                    if str(row[3]) == today2:
                        i += 1
                        db_ids.append(str(i))
                        db_titles.append(row[0])
                        db_urls.append(row[1])
                        db_sources.append(row[2])
                        db_datetime.append(row[3])
        # 标题去重
        # del_copy(db_ids, db_titles, db_urls, db_sources)
        return db_ids, db_titles, db_urls, db_sources
    except:
        # 发生错误时回滚
        print("媒体:今日爬取查询错误")
        db.rollback()

# 查询当日爬取的微信文章内容
def select_sql_wechat():
    print("正在查询今日微信爬取数量")
    content_sql()
    today = str(datetime.date.today())
    try:
        # 查询发布时间，返回标题/原文链接/来源
        sql = "SELECT TITLE,ORIGINAL_LINK,SOURCE,RELEASE_DATETIME FROM originallink WHERE SOURCE_REAL = '"+today+"'"
        db_ids = []
        db_titles = []
        db_urls = []
        db_sources =[]
        db_datetime = []
        # try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        wechat_count = len(results)
        # print("结果",results)
        # row为tuple类型
        i = 0
        today1 = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        today2 = (datetime.datetime.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        # 遍历今日爬取的所有数据,选择微信文章
        for row in results:
            # 通过url中的weixin过滤信息
            if 'weixin' in str(row[1]):
                print(row)
                # 获取发布时间为今日的信息
                if str(row[3]) == today:
                    i += 1
                    db_ids.append(str(i))
                    db_titles.append(row[0])
                    db_urls.append(row[1])
                    db_sources.append(row[2])
                    db_datetime.append(row[3])
        # 今日信息少于10条，则继续推送第二日信息
        if i <= 10:
            for row in results:
                # 通过url中的weixin过滤信息
                if 'weixin' in str(row[1]):
                    if str(row[3]) == today1:
                        i += 1
                        db_ids.append(str(i))
                        db_titles.append(row[0])
                        db_urls.append(row[1])
                        db_sources.append(row[2])
                        db_datetime.append(row[3])
        # 近两日信息少于10条，则继续推送第三日信息
        if i <= 10:
            for row in results:
                # 通过url中的weixin过滤信息
                if 'weixin' in str(row[1]):
                    if str(row[3]) == today2:
                        i += 1
                        db_ids.append(str(i))
                        db_titles.append(row[0])
                        db_urls.append(row[1])
                        db_sources.append(row[2])
                        db_datetime.append(row[3])
        # 标题去重
        # del_copy(db_ids, db_titles, db_urls, db_sources)
        return db_ids, db_titles, db_urls, db_sources, wechat_count
    except:
        # 发生错误时回滚
        print("微信:今日爬取查询错误")
        db.rollback()

# 主函数，需要传入当日爬取用时和爬取数量
def email_url_main(today_time, today_i):
    # 获取数据库中今日爬取的文章
    (db_ids, db_titles, db_urls, db_sources) = select_sql()
    # 编辑邮件正文内容
    edit_email(today_time, today_i, db_ids, db_titles, db_urls,db_sources)

# 人工备用通道，手动推送,爬取用时,媒体数据数量,微信数据数量
# email_url_main('3.89小时',362)
