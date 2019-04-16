#!/usr/bin/env python
# coding=utf-8

import os
import pytz
from datetime import timedelta, date, datetime

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y%m%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMMDD")

def us_end_date():
    tz = pytz.timezone('America/Los_Angeles')
    end_date = datetime.now(tz) + timedelta(days=-1)
    return end_date.strftime('%Y%m%d')

def daterange(start_date_string, end_date_string, containStart = False):
    start_date = datetime.strptime(start_date_string, "%Y%m%d").date()
    if not containStart:
        start_date = start_date + timedelta(days=1)
    end_date = datetime.strptime(end_date_string, "%Y%m%d").date() + timedelta(days=1)
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n)).strftime("%Y%m%d")

def nextdatestring(date_string):
    next_date = datetime.strptime(date_string, "%Y%m%d").date() + timedelta(days=1)
    return next_date.strftime("%Y%m%d")

def date_add(date_string, days):
    new_date = datetime.strptime(date_string, "%Y%m%d").date() + timedelta(days=days)
    return new_date.strftime("%Y%m%d")

def formatdate(date_string):
    date = datetime.strptime(date_string, "%Y%m%d").date()
    return date.strftime("%m-%d")

def betweenday(start_date_string, end_date_string):
    start_date = datetime.strptime(start_date_string, "%Y%m%d").date()
    end_date = datetime.strptime(end_date_string, "%Y%m%d").date() + timedelta(days=1)
    return int((end_date - start_date).days)

def append_line(report_lines, index, content, appendLine = True):
    if len(report_lines) > index:
        report_lines[index] = report_lines[index] + content if appendLine else content
    else:
        for k in range(len(report_lines), index + 1):
            report_lines.append('')
        report_lines[index] = report_lines[index] + content if appendLine else content
