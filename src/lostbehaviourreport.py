#!/usr/bin/env python
# coding=utf-8

import os
import json
from util import validate, daterange, formatdate, betweenday, append_line
from common import get_firstopen_usercount, get_lost_usercount
from query import querysql

def add_map_key_count(map, key):
    if key == None:
        key = 0
    map[key] = map.get(key, 0) + 1

def print_map(level, map_name, map):
    print "level: ", level, " ", map_name
    for key, value in map.items():
        print key, ",", value

def generate_lostbehaviour_report_at_date(report_lines, platform, date, end_date):
    print("generate_lostbehaviour_report_at_date ", date)
    if date == end_date:
        return
    level = 7
    behaviour_results = querysql("./sql/behaviour_of_lost_users.sql", platform, date, end_date, level)
    compound_count_map = {}
    buy_count_map = {}
    max_stage = {}
    tap_count = {}
    ad_view_count = {}
    for k in range(len(behaviour_results)):
        behaviour_result = behaviour_results[k]
        add_map_key_count(compound_count_map, behaviour_result.compound_count)
        add_map_key_count(buy_count_map, behaviour_result.buy_count)
        add_map_key_count(max_stage, behaviour_result.max_stage)
        add_map_key_count(tap_count, behaviour_result.tap_count)
        add_map_key_count(ad_view_count, behaviour_result.ad_view_count)
    print_map(level, "合成次数分布", compound_count_map)
    print_map(level, "商店购买次数分布", buy_count_map)
    print_map(level, "关卡分布", max_stage)
    print_map(level, "点击次数分布", tap_count)
    print_map(level, "观看广告次数分布", ad_view_count)

def generate_lostbehaviour_report(platform, start_date, end_date):
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    output = "output/lostuser_behaviour_report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        report_lines = []
        for single_date in daterange(start_date, end_date, True):
            generate_lostbehaviour_report_at_date(report_lines, platform, single_date, end_date)
        reportstring = '\n'.join(report_lines)
        out.write(reportstring)
        out.close()
