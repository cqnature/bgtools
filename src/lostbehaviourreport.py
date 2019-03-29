#!/usr/bin/env python
# coding=utf-8

import os
import json
from util import validate, daterange, formatdate, betweenday, append_line
from common import get_firstopen_usercount, get_lost_usercount
from query import querysql

def generate_lostbehaviour_report_at_date(report_lines, platform, date, end_date):
    print("generate_lostbehaviour_report_at_date ", date)
    if date == end_date:
        return
    behaviour_results = querysql("./sql/behaviour_of_lost_users.sql", platform, date, end_date, 8)
    for k in range(len(behaviour_results)):
        behaviour_result = behaviour_results[k]
        print "max_level ", behaviour_result.max_level, " user_pseudo_id ", behaviour_result.user_pseudo_id, " compound_count ", behaviour_result.compound_count, " buy_count ", behaviour_result.buy_count, " max_stage ", behaviour_result.max_stage, " tap_count ", behaviour_result.tap_count, " ad_view_count ", behaviour_result.ad_view_count

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
