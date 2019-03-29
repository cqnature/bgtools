#!/usr/bin/env python
# coding=utf-8

from lostplantreport import generate_lostplant_report
from retentionplantreport import generate_retentionplant_report
from stagereport import generate_stage_report
from retentionadsreport import generate_retention_ads_report
from newadsreport import generate_new_ads_report
from totaladsreport import generate_total_ads_report
from lostbehaviourreport import generate_lostbehaviour_report

def generate_report(platform, start_date, end_date):
    # generate_lostplant_report(platform, start_date, end_date)
    # generate_retentionplant_report(platform, start_date, end_date)
    # generate_stage_report(platform, start_date, end_date)
    # generate_retention_ads_report(platform, start_date, end_date)
    # generate_new_ads_report(platform, start_date, end_date)
    # generate_total_ads_report(platform, start_date, end_date)
    generate_lostbehaviour_report(platform, start_date, end_date)
