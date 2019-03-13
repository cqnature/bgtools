#!/usr/bin/env python
# coding=utf-8

from src.query import querysql
from src.report import generate_report

if __name__ == '__main__':
    generate_report("ANDROID", "20190305", "20190312")
    generate_report("IOS", "20190305", "20190312")
