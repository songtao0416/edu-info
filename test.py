from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

key = '教育'
url = 'https://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&s_from=input&_sug_=n&_sug_type_=' % key

driver = webdriver.Chrome(
    "I:\安装包\Chrome6503325146x86\GoogleChrome_65.0.3325.146_x86\ChromePortable\App\Google Chrome\chromedriver.exe")  # 调用chrome浏览器
driver.maximize_window()  # 窗口最大化
# 搜狗微信网站
website = 'https://weixin.sogou.com/'
driver.get(url)