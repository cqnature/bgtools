#!/usr/bin/env python
# coding=utf-8

from src.report import generate_report
from src.util import us_end_date
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='scheduler.log',
                    filemode='a')

def report_prepare():
    print '任务准备执行...'

def report():
    end_date = us_end_date()
    generate_report("ANDROID", "20190329", end_date)
    generate_report("IOS", "20190329", end_date)

def listener(event):
    if event.exception:
        print '任务出错了！！！！！！'
    else:
        print '任务照常运行...'

if __name__ == '__main__':
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors,    job_defaults=job_defaults)
    # 添加调度任务
    # 调度方法为 report，触发器选择 cron(周期性)，每日晚上10点
    scheduler.add_job(report_prepare, 'interval', seconds=3)
    scheduler.add_job(report, 'cron', hour=22)
    scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler._logger = logging
    # 启动调度任务
    scheduler.start()
