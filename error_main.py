import time
import datetime
from email_report import send_mail
from check_ping import check_ping
from email_url import email_url_main

def get_data():
    send_mail(today_time, today_i)
    time.sleep(1800)
    email_url_main(today_time, today_i)

# 当主程序出错时，请输入条数即可
today_time = '2.91小时'
today_i = '14'
get_data()

