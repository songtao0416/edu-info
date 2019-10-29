# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import xlrd
from xlutils.copy import copy
from snownlp import SnowNLP
import os
import base_list
import time

# 读取 all_data 表数据
def open_all_data(all_path):
    path = all_path
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    data_list = []
    for i in range(0, int(sheet.nrows)):
        data_list.append(sheet.cell(i, 6).value)
    print("成功读取")
    return data_list

# 存储到all_data的xls表中
def save_xls(path,tags_list,sen_list,sen2_list, ab_list):
    book1 = xlrd.open_workbook(path)
    book2 = copy(book1)
    sheet = book2.get_sheet(0)
    for i in range(0, len(tags_list)):
        sheet.write(i+1, 7, tags_list[i])   # 从list[0]开始遍历，但xls中[0]行为标题
        sheet.write(i+1, 8, sen_list[i])
        sheet.write(i+1, 9, sen2_list[i])
        sheet.write(i+1, 10, ab_list[i])
        book2.save(path)

# 获取关键词
def get_topkey(data_list):
    tags_list = []
    j = 10
    for i in range(1, len(data_list)):      # data_list[0]为列标题，故从[1]开始遍历
        # content = jieba.cut(data)
        data = data_list[i]
        tags = jieba.analyse.textrank(data, topK=j)
        tags = ','.join(tags)
        print(tags)
        tags_list.append(tags)
    print("关键词获取成功")
    return tags_list

# 对正文进行情感分析
def get_emoji(data_list):
    sen_list = []
    sen2_list = []
    for i in range(1, len(data_list)):
        data = data_list[i]
        if data != '':
            em = SnowNLP(data)
            # 获取全文的情感属性
            sen = em.sentiments
            sen_list.append(sen)
            # 设定，0-0.5为负面，0.5-0.8为中性，0.8-1为正面
            if sen >= 0.5:
                if sen >= 0.8:
                    sen2_list.append("正面情感")
                else:
                    sen2_list.append('中性情感')
            else:
                sen2_list.append("负面情感")
        else:
            sen_list.append("null")
            sen2_list.append("null")
    print("情感分析成功")
    return sen_list, sen2_list

# 提取自动摘要
def get_abstract(data_list):
    ab_list = []

    for i in range(1, len(data_list)):
        data = data_list[i]
        if data != '':
            em = SnowNLP(data)
            # 获取自动摘要
            ab = em.summary(5)
            ab = '。'.join(ab)
            ab_list.append(ab)
            print(ab)
        else:
            ab_list.append("null")
    print("自动摘要成功")
    return ab_list


# 主函数
def topkey(all_path):
    data_list = open_all_data(all_path)             # 打开all_data表获取正文
    tags_list = get_topkey(data_list)            # 提取关键词
    (sen_list, sen2_list) = get_emoji(data_list)                 # 获取全文情感属性
    ab_list = get_abstract(data_list)                         # 获取自动摘要
    save_xls(all_path, tags_list, sen_list, sen2_list, ab_list)         # 保存结果到all_data中


# start = time.clock()
# keywords = base_list.keywords
# for i in range(1, len(keywords)):
#     skeyword = keywords[i]
#     print(skeyword)
#     for keyword in skeyword:
#         mkpath = os.getcwd() + '/' + keyword + '--爬取结果'
#         all_path = mkpath + '/（总数据）' + keyword + '.csv.xls'
#         print(all_path)
#         topkey(all_path)
# end = time.clock()
# print("关键词分析用时:",end-start,"秒")