#!/usr/bin/env python
import os
from google.cloud import bigquery

def querysql(filename, *parameter):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./config/credentials.json"
    os.environ["https_proxy"] = "http://127.0.0.1:6152"
    os.environ["http_proxy"] = "http://127.0.0.1:6152"
    os.environ["all_proxy"] = "socks5://127.0.0.1:6153"
    if os.path.exists(filename) and os.path.isfile(filename):
        client = bigquery.Client()
        with open(filename) as file:
            content = file.read()
            sql = content.format(*parameter)
            query_job = client.query(sql)
            results = query_job.result()  # Waits for job to complete.
            file.close()
        return list(results)
    else:
        print("Make sure you have sql file in path: ", filename)
