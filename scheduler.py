#!/usr/bin/env python
# coding=utf-8

from src.report import generate_report
from src.util import us_end_date
from apscheduler.schedulers.background import BackgroundScheduler

def report():
    end_date = us_end_date()
    generate_report("ANDROID", "20190329", end_date)
    generate_report("IOS", "20190329", end_date)

if __name__ == '__main__':
    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()
    # 添加调度任务
    # 调度方法为 report，触发器选择 cron(周期性)，每日晚上10点
    scheduler.add_job(report, 'cron', hour=22)
    # 启动调度任务
    scheduler.start()
