#!/usr/bin/env python
# coding=utf-8

from query import querysql

def get_firstopen_usercount(platform, date):
    firstopen_results = querysql("./sql/firstopen_user_id.sql", platform, date)
    firstopen_usercount = sum(1 for _ in firstopen_results)
    return firstopen_usercount

def get_lost_usercount(platform, start_date, end_date):
    lost_user_ids = querysql("./sql/lost_user_id.sql", platform, start_date, end_date)
    current_lost_usercount = sum(1 for _ in lost_user_ids)
    return current_lost_usercount

def get_retention_usercount(platform, start_date, end_date):
    retention_user_ids = querysql("./sql/retention_user_id.sql", platform, start_date, end_date)
    current_retention_usercount = sum(1 for _ in retention_user_ids)
    return current_retention_usercount
