#!/usr/bin/env python
# coding=utf-8

from src.query import querysql
from src.report import generate_report
from src.util import us_end_date

if __name__ == '__main__':
    end_date = us_end_date()
    generate_report("ANDROID", "20190412", end_date)
    # generate_report("IOS", "20190329", end_date)
