#!/usr/bin/env python
# coding=utf-8

# import datetime
from src.query import querysql
from src.report import generate_report
from src.mail import send_mail
# def count_date(start_date_string, end_date_string):
#     start_date = datetime.datetime.strptime(start_date_string, "%Y%m%d").date()
#     end_date = datetime.datetime.strptime(end_date_string, "%Y%m%d").date()
#     current_date = start_date
#     while current_date <= end_date:
#         print("current_date", current_date)
#         current_date += datetime.timedelta(days=1)

if __name__ == '__main__':
    # results = querysql("./sql/signup_user_id.sql", "ANDROID", "20190305")
    # print(sum(1 for _ in results))
    # signup_layers_progress_results = querysql("./sql/signup_layers_progress.sql", "ANDROID", "20190305")
    # for row in signup_layers_progress_results:
    #     print("{} : {} views".format(row.max_layer, row.user_count))
    # generate_report("ANDROID", "20190409", "20190411")
    # generate_report("IOS", "20190305", "20190312")

    # #邮件正文内容
    # mail_body = """
    #  <p>你好，Python 邮件发送测试...</p>
    #  <p>这是使用python登录qq邮箱发送HTML格式和图片的测试邮件：</p>
    #  <p><a href='http://www.yiibai.com'>易百教程</a></p>
    #  <p>图片演示：</p>
    #  <p>![](cid:send_image)</p>
    # """
    # send_mail("测试标题", mail_body)
