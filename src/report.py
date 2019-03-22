#!/usr/bin/env python
# coding=utf-8

from plantreport import generate_plant_report
from stagereport import generate_stage_report
from adsreport import generate_ads_report

def generate_report(platform, start_date, end_date):
    generate_plant_report(platform, start_date, end_date)
    generate_stage_report(platform, start_date, end_date)
    generate_ads_report(platform, start_date, end_date)
