#!/usr/bin/env python
# coding=utf-8

from lostplantreport import generate_lostplant_report
from retentionplantreport import generate_retentionplant_report
from stagereport import generate_stage_report
from adsreport import generate_ads_report
from totaladsreport import generate_total_ads_report

def generate_report(platform, start_date, end_date):
    # generate_lostplant_report(platform, start_date, end_date)
    # generate_retentionplant_report(platform, start_date, end_date)
    # generate_stage_report(platform, start_date, end_date)
    # generate_ads_report(platform, start_date, end_date)
    generate_total_ads_report(platform, start_date, end_date)
