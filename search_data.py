# -*- coding: utf-8 -*-
# 根据url获取不同网站的data，包括文章标题、发布时间、全文内容

import csv
import urllib
import re
from bs4 import BeautifulSoup
from lxml import html
import urllib.request
import time
import html5lib
from newspaper import Article

# 获取DBURL，去重
def get_dburls():
    db_urls = []
    path = '(URL)DB.csv'
    dburl_csv_reader = csv.reader(open(path, encoding='utf-8'))
    for row in dburl_csv_reader:
        db_urls.append(row[1])
    return db_urls

# 从csv中获取url的list和title的list和time的list
def get_url_list(url_adds,mkpath):
    # 获取数据库中的db_urls，去重
    db_urls = get_dburls()
    path = mkpath + '/(URL)'+ url_adds + '.csv'
    csv_reader = csv.reader(open(path,encoding='utf-8'))
    url_list = []
    title_list = []
    ptime_list = []
    for row in csv_reader:
        if row[2] not in db_urls:
            row_time = row[3].strip('[]')
            row_url = row[2].strip('[]')
            row_title = row[1].strip('[]')
            url_list.append(row_url)
            title_list.append(row_title)
            ptime_list.append(row_time)
    return url_list, title_list, ptime_list

# # 通过url，定位标签，获取信息，包括标题、时间、内容
# def url_text(url):
#     try:
#         # 通过url获取网页内容，返回r
#         # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'}
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
#         req = urllib.request.Request(url, headers=headers)
#         file = urllib.request.urlopen(req, timeout=5)
#         r = file.read()
#         soup = BeautifulSoup(r, "html5lib")
#         etree = html.etree
#         et_html = etree.HTML(r)
#         # 定位h1，获取文章标题
#         title = 'null'
#         try:
#             h1 = soup.find_all('h1')
#             for x in h1:
#                 title = x.text.strip()
#         except:
#             print("无法获取标题")
#
#         # # 获取发布时间，不同网页发布时间的标签有差异,故用正则表达式获取
#         # try:
#         #     t1 = et_html.xpath("//text()")
#         #     pattern = re.compile(r"(\d{4}\S\d{1,2}\S\d{1,2})")
#         #     page_time = re.search(pattern, ''.join(t1)).group(0)
#         # except:
#         #     page_time = "null"
#         #     print("无法获取时间")
#
#         # # 查找所有class属性为hd的div标签下的p标签,获取全部文本
#         # all_co1 = soup.find_all('p')
#         # all_co2 = soup.find_all('td')
#         # all_co3 = soup.find_all('u')
#         # all_context = []
#         # for all_y1 in all_co1:
#         #     all_context.append(str(all_y1.text).strip())
#         # for all_y2 in all_co2:
#         #     all_context.append(str(all_y2.text).strip())
#         # for all_y3 in all_co3:
#         #     all_context.append(str(all_y3.text).strip())
#         # all_context = list(filter(None, all_context))
#
#         all_context = r.decode('utf-8')
#         # r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
#         r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@★、…【】？[\\]^_`{|}~]+'
#         all_context = re.sub(r1, '', ''.join(all_context))
#
#         # 去掉空格
#         # all_context = all_context.replace(' ', '')
#         # all_context = all_context.replace('	', '')  #两个空格不一样
#         # all_context = all_context.replace('\n', '')
#         return title, all_context
#     except:
#         print("网址无法打开")
#         return "网址无法打开", ''
# newspaper爬取url的新闻内容
def url_newspaper(url):
    try:
        news = Article(url, language='zh')
        news.download()  # 先下载
        news.parse()  # 再解析
        title = news.title
        all_context = news.text
        # print(news.text)  # 新闻正文
        # print(news.title)  # 新闻标题
        # print(news.html)   #未修改的原始HTML
        # print(news.authors)  # 新闻作者
        # print(news.top_image) #本文的“最佳图像”的URL
        # print(news.movies)  #本文电影url
        # print(news.keywords)  # 新闻关键词
        # print(news.summary)  # 从文章主体txt中生成的摘要
        # print(news.images) #本文中的所有图像url
        return title, all_context
    except:
        print("网址无法打开--newspaper")
        return "网址无法打开", ''
    pass

# main调用的主函数
def search_data(url_adds, s_name, all_path, mkpath, all_writer):
    (url_list, title_list, ptime_list) = get_url_list(url_adds,mkpath)    # 从csv中获取url
    print("全部url读取成功")
    # 遍历url，获取网页内容，返回data
    rel_count = 0
    j1 = 1
    for i in range(1, len(url_list)):
        try:
            # 只爬取2019年的文章
            if '2019' in ptime_list[i]:
            #if 1 == 1:
                url = url_list[i].strip("''")   # 去掉''，保留url
                print(url)
                # (title, all_context) = url_text(url)       # beautiful读取url中的内容
                (title, all_context) =url_newspaper(url)     # newspaper读取url中的内容
                if all_context != '':
                    if len(all_context) > 20:
                        all_writer.writerow((j1, s_name, title_list[i], title, ptime_list[i], url, all_context))
                        print("第%d条url爬取成功" % i)
                        j1 += 1
        except:
            print("第%d条URL读取失败" % i)
        rel_count = j1
    print("%s全部url爬取完毕" % url_adds)
    return rel_count