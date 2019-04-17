#!/usr/bin/env python
# coding=utf-8
import os
import json

from lostplantreport import generate_lostplant_report
from retentionplantreport import generate_retentionplant_report
from stagereport import generate_stage_report
from retentionadsreport import generate_retention_ads_report
from newadsreport import generate_new_ads_report
from totaladsreport import generate_total_ads_report
from lostbehaviourreport import generate_lostbehaviour_report
from retentionbehaviourreport import generate_retentionbehaviour_report
from iapbehaviourreport import generate_iap_behaviour_report
from mailreport import generate_mail_report

def load_config():
    with open("./config/config.json") as file:
        file_config = json.load(file)
        set_env_from_config(file_config, "GOOGLE_APPLICATION_CREDENTIALS")
        set_env_from_config(file_config, "https_proxy")
        set_env_from_config(file_config, "http_proxy")
        set_env_from_config(file_config, "all_proxy")
        file.close()

def set_env_from_config(config, key):
    if config.has_key(key):
        os.environ[key] = config[key]

def generate_report(platform, start_date, end_date):
    load_config()
    generate_mail_report(platform, start_date, end_date)
    # generate_lostplant_report(platform, start_date, end_date)
    # generate_retentionplant_report(platform, start_date, end_date)
    # generate_stage_report(platform, start_date, end_date)
    # generate_retention_ads_report(platform, start_date, end_date)
    # generate_new_ads_report(platform, start_date, end_date)
    # generate_total_ads_report(platform, start_date, end_date)
    # generate_iap_behaviour_report(platform, start_date, end_date)
    # generate_lostbehaviour_report(platform, start_date, end_date)
    # generate_retentionbehaviour_report(platform, start_date, end_date)
