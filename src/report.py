#!/usr/bin/env python
# coding=utf-8

import os
import json
from datetime import timedelta, date, datetime
from query import querysql

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y%m%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMMDD")

def daterange(start_date_string, end_date_string, containStart = False):
    start_date = datetime.strptime(start_date_string, "%Y%m%d").date()
    if not containStart:
        start_date = start_date + timedelta(days=1)
    end_date = datetime.strptime(end_date_string, "%Y%m%d").date() + timedelta(days=1)
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n)).strftime("%Y%m%d")

def append_line(report_lines, index, content):
    if len(report_lines) > index:
        report_lines[index] = report_lines[index] + content
    else:
        for k in range(len(report_lines), index + 1):
            report_lines.append('')
        report_lines[index] = report_lines[index] + content

def generate_plant_report_at_date(report_lines, platform, date, end_date):
    print("generate_plant_report_at_date ", date)
    max_level = 0
    with open("./etc/food.json") as file:
        file_config = json.load(file)
        max_level = file_config['config']['maxId']
        file.close()

    with open("./etc/plant_progress_of_users.csv") as file:
        firstopen_results = querysql("./sql/firstopen_user_id.sql", platform, date)
        firstopen_usercount = sum(1 for _ in firstopen_results)
        if firstopen_usercount == 0:
            return;

        lineIndex = 0
        lines = file.readlines()
        append_line(report_lines, lineIndex, lines[0].strip().format(date))
        lineIndex += 1
        signup_layers_progress_lines = [x.strip() for x in lines[1:4]]
        signup_layers_progress_results = querysql("./sql/plant_progress_of_signup_users.sql", platform, date)
        currentIndex = 1
        total_level_user_count = 0
        signup_layers_progress_lines[0] = signup_layers_progress_lines[0].format(date)
        signup_layers_progress_lines[2] = signup_layers_progress_lines[2].format(firstopen_usercount, 100)
        signup_base_datas = []
        for k in range(1, signup_layers_progress_results[0].max_level):
            signup_base_datas.append([k, 0, 0])
        for row in signup_layers_progress_results:
            for k in range(currentIndex + 1, row.max_level + 1):
                if k == row.max_level:
                    signup_base_datas.append([k, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)])
                    total_level_user_count += row.user_count
                else:
                    signup_base_datas.append([k, 0, 0])
            currentIndex = row.max_level
        for k in range(currentIndex + 1, max_level + 1):
            signup_base_datas.append([k, 0, 0])
        first_level_user_count = firstopen_usercount - total_level_user_count
        signup_base_datas[0][1] = first_level_user_count
        signup_base_datas[0][2] = 100*float(first_level_user_count)/float(firstopen_usercount)
        for k in range(len(signup_base_datas)):
            data = signup_base_datas[k]
            signup_layers_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
        for k in range(len(signup_layers_progress_lines)):
            append_line(report_lines, lineIndex + k, signup_layers_progress_lines[k])
        lineIndex += len(signup_layers_progress_lines)

        currentDayIndex = 1
        lost_base_datas = []
        lost_base_usercount = 0
        lost_base_day = ''
        lost_day_progress_lines = []
        for single_date in daterange(date, end_date):
            lost_day_results = querysql("./sql/plant_progress_of_lost_users.sql", platform, date, single_date)
            if currentDayIndex == 1:
                lost_day_progress_lines.extend([x.strip() for x in lines[4:8]])
                currentIndex = 1
                for k in range(1, lost_day_results[0].max_level):
                    lost_base_datas.append((k, 0, 0))
                for row in lost_day_results:
                    for k in range(currentIndex + 1, row.max_level + 1):
                        if k == row.max_level:
                            lost_base_datas.append([k, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)])
                        else:
                            lost_base_datas.append([k, 0, 0])
                    currentIndex = row.max_level
                for k in range(currentIndex + 1, max_level + 1):
                    lost_base_datas.append([k, 0, 0])
                lost_base_usercount = sum(t[1] for t in lost_base_datas)
                lost_day_progress_lines[0] = lost_day_progress_lines[0].format(single_date)
                lost_day_progress_lines[3] = lost_day_progress_lines[3].format(lost_base_usercount, 100* float(lost_base_usercount)/float(firstopen_usercount))
                lost_base_day = single_date
                for k in range(len(lost_base_datas)):
                    data = lost_base_datas[k]
                    lost_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
            else:
                current_lost_datas = []
                lost_day_progress_lines.extend([x.strip() for x in lines[8:]])
                currentIndex = 1
                for k in range(1, lost_day_results[0].max_level):
                    current_lost_datas.append((k, 0, 0))
                for row in lost_day_results:
                    for k in range(currentIndex + 1, row.max_level + 1):
                        if k == row.max_level:
                            current_lost_datas.append([k, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)])
                        else:
                            current_lost_datas.append([k, 0, 0])
                    currentIndex = row.max_level
                for k in range(currentIndex + 1, max_level + 1):
                    current_lost_datas.append([k, 0, 0])
                current_lost_usercount = sum(t[1] for t in current_lost_datas)
                origin_lost_base_usercount = lost_base_usercount
                lost_base_usercount = current_lost_usercount
                current_lost_usercount -= origin_lost_base_usercount
                lost_day_progress_lines[0] = lost_day_progress_lines[0].format(single_date, lost_base_day)
                lost_day_progress_lines[3] = lost_day_progress_lines[3].format(current_lost_usercount, 100*float(current_lost_usercount)/float(firstopen_usercount))
                lost_base_day = single_date
                for k in range(len(current_lost_datas)):
                    data = current_lost_datas[k]
                    base_data = lost_base_datas[k]
                    lost_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1] - base_data[1], data[2] - base_data[2]))
                lost_base_datas = current_lost_datas
            # 留存率查询
            lost_user_ids = querysql("./sql/lost_user_id.sql", platform, date, single_date)
            current_lost_usercount = sum(1 for _ in lost_user_ids)
            lost_day_progress_lines[1] = lost_day_progress_lines[1].format(100*float(firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))
            # 数据拼接
            for k in range(len(lost_day_progress_lines)):
                append_line(report_lines, lineIndex + k, lost_day_progress_lines[k])
            report_lines_length = len(lost_day_progress_lines)
            lineIndex += report_lines_length
            # 增加天数索引
            currentDayIndex += 1
            # 清空缓存
            del lost_day_progress_lines[:]
        file.close()

def generate_stage_report_at_date(report_lines, platform, date, end_date):
    print("generate_stage_report_at_date ", date)
    max_level = 0
    with open("./etc/food.json") as file:
        file_config = json.load(file)
        max_level = file_config['config']['maxId']
        file.close()

    with open("./etc/plant_progress_of_users.csv") as file:
        firstopen_results = querysql("./sql/firstopen_user_id.sql", platform, date)
        firstopen_usercount = sum(1 for _ in firstopen_results)
        if firstopen_usercount == 0:
            return;

        lineIndex = 0
        lines = file.readlines()
        append_line(report_lines, lineIndex, lines[0].strip().format(date))
        lineIndex += 1
        signup_layers_progress_lines = [x.strip() for x in lines[1:4]]
        signup_layers_progress_results = querysql("./sql/plant_progress_of_signup_users.sql", platform, date)
        currentIndex = 1
        total_level_user_count = 0
        signup_layers_progress_lines[0] = signup_layers_progress_lines[0].format(date)
        signup_layers_progress_lines[2] = signup_layers_progress_lines[2].format(firstopen_usercount, 100)
        signup_base_datas = []
        for k in range(1, signup_layers_progress_results[0].max_level):
            signup_base_datas.append([k, 0, 0])
        for row in signup_layers_progress_results:
            for k in range(currentIndex + 1, row.max_level + 1):
                if k == row.max_level:
                    signup_base_datas.append([k, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)])
                    total_level_user_count += row.user_count
                else:
                    signup_base_datas.append([k, 0, 0])
            currentIndex = row.max_level
        for k in range(currentIndex + 1, max_level + 1):
            signup_base_datas.append([k, 0, 0])
        first_level_user_count = firstopen_usercount - total_level_user_count
        signup_base_datas[0][1] = first_level_user_count
        signup_base_datas[0][2] = 100*float(first_level_user_count)/float(firstopen_usercount)
        for k in range(len(signup_base_datas)):
            data = signup_base_datas[k]
            signup_layers_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
        for k in range(len(signup_layers_progress_lines)):
            append_line(report_lines, lineIndex + k, signup_layers_progress_lines[k])
        lineIndex += len(signup_layers_progress_lines)

        currentDayIndex = 1
        lost_base_datas = []
        lost_base_usercount = 0
        lost_base_day = ''
        lost_day_progress_lines = []
        for single_date in daterange(date, end_date):
            lost_day_results = querysql("./sql/plant_progress_of_lost_users.sql", platform, date, single_date)
            if currentDayIndex == 1:
                lost_day_progress_lines.extend([x.strip() for x in lines[4:8]])
                currentIndex = 1
                for k in range(1, lost_day_results[0].max_level):
                    lost_base_datas.append((k, 0, 0))
                for row in lost_day_results:
                    for k in range(currentIndex + 1, row.max_level + 1):
                        if k == row.max_level:
                            lost_base_datas.append([k, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)])
                        else:
                            lost_base_datas.append([k, 0, 0])
                    currentIndex = row.max_level
                for k in range(currentIndex + 1, max_level + 1):
                    lost_base_datas.append([k, 0, 0])
                lost_base_usercount = sum(t[1] for t in lost_base_datas)
                lost_day_progress_lines[0] = lost_day_progress_lines[0].format(single_date)
                lost_day_progress_lines[3] = lost_day_progress_lines[3].format(lost_base_usercount, 100* float(lost_base_usercount)/float(firstopen_usercount))
                lost_base_day = single_date
                for k in range(len(lost_base_datas)):
                    data = lost_base_datas[k]
                    lost_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
            else:
                current_lost_datas = []
                lost_day_progress_lines.extend([x.strip() for x in lines[8:]])
                currentIndex = 1
                for k in range(1, lost_day_results[0].max_level):
                    current_lost_datas.append((k, 0, 0))
                for row in lost_day_results:
                    for k in range(currentIndex + 1, row.max_level + 1):
                        if k == row.max_level:
                            current_lost_datas.append([k, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)])
                        else:
                            current_lost_datas.append([k, 0, 0])
                    currentIndex = row.max_level
                for k in range(currentIndex + 1, max_level + 1):
                    current_lost_datas.append([k, 0, 0])
                current_lost_usercount = sum(t[1] for t in current_lost_datas)
                origin_lost_base_usercount = lost_base_usercount
                lost_base_usercount = current_lost_usercount
                current_lost_usercount -= origin_lost_base_usercount
                lost_day_progress_lines[0] = lost_day_progress_lines[0].format(single_date, lost_base_day)
                lost_day_progress_lines[3] = lost_day_progress_lines[3].format(current_lost_usercount, 100*float(current_lost_usercount)/float(firstopen_usercount))
                lost_base_day = single_date
                for k in range(len(current_lost_datas)):
                    data = current_lost_datas[k]
                    base_data = lost_base_datas[k]
                    lost_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1] - base_data[1], data[2] - base_data[2]))
                lost_base_datas = current_lost_datas
            # 留存率查询
            lost_user_ids = querysql("./sql/lost_user_id.sql", platform, date, single_date)
            current_lost_usercount = sum(1 for _ in lost_user_ids)
            lost_day_progress_lines[1] = lost_day_progress_lines[1].format(100*float(firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))
            # 数据拼接
            for k in range(len(lost_day_progress_lines)):
                append_line(report_lines, lineIndex + k, lost_day_progress_lines[k])
            report_lines_length = len(lost_day_progress_lines)
            lineIndex += report_lines_length
            # 增加天数索引
            currentDayIndex += 1
            # 清空缓存
            del lost_day_progress_lines[:]
        file.close()

def generate_report(platform, start_date, end_date):
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    output = "output/plant_report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        report_lines = []
        for single_date in daterange(start_date, end_date, True):
            generate_plant_report_at_date(report_lines, platform, single_date, end_date)
        reportstring = '\n'.join(report_lines)
        out.write(reportstring)
        out.close()

    output = "output/stage_report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        report_lines = []
        for single_date in daterange(start_date, end_date, True):
            generate_stage_report_at_date(report_lines, platform, single_date, end_date)
        reportstring = '\n'.join(report_lines)
        out.write(reportstring)
        out.close()
