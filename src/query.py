#!/usr/bin/env python
import os
from google.cloud import bigquery

def querysql(filename, *parameter):
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
