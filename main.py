#!/usr/bin/env python
# coding=utf-8

from src.query import querysql
from src.report import generate_report

if __name__ == '__main__':
    generate_report("ANDROID", "20190317", "20190326")
    # generate_report("IOS", "20190315", "20190321")
