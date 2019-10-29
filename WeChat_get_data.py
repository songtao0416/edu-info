# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import xlrd
import urllib.request
import re
import csv
import os
import time
import html5lib
from newspaper import Article

# newspaper爬取url的新闻内容
def get_data(url):
    try:
        news = Article(url, language='zh')
        news.download()  # 先下载
        news.parse()  # 再解析
        print(url)
        title = news.title
        all_context = news.text
        # author = news.authors
        # print(news.text)  # 新闻正文
        # print(news.title)  # 新闻标题
        # print(news.html)   #未修改的原始HTML
        # print(news.authors)  # 新闻作者
        # print(news.top_image) #本文的“最佳图像”的URL
        # print(news.movies)  #本文电影url
        # print(news.keywords)  # 新闻关键词
        # print(news.summary)  # 从文章主体txt中生成的摘要
        # print(news.images) #本文中的所有图像url
        print(title)
        return title, all_context
    except:
        print("网址无法打开--newspaper")
        return "网址无法打开", ''

# 测试
# get_data('https://weixin.sogou.com/api/share?timestamp=1566896054&signature=qIbwY*nI6KU9tBso4VCd8lYSesxOYgLcHX5tlbqlMR8N6flDHs4LLcFgRw7FjTAOcf9HI0jKJrB8J9KmC8rjWnpTSael79DBIpylkcvAFDIAroEOq31hwYdO7K7YGNlidqnw8UagjhPBiOHhWq2dCPXnSmJCSn-hFbOAgakfdkac9pzyrIdcKO2sYdgSPtkjqWbZfPpH2sdHIdwYjNO2VoInFyjUwl7A9bYNSA9W52Y=')
# get_data('https://shouyou.3dmgame.com/gl/126303.html')