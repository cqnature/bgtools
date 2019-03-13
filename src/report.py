#!/usr/bin/env python

import os
from datetime import timedelta, date, datetime
from query import querysql

max_layer = 36

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y%m%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMMDD")

def daterange(start_date_string, end_date_string, containStart = False):
    start_date = datetime.strptime(start_date_string, "%Y%m%d").date()
    if not containStart:
        start_date = start_date + timedelta(days=1)
    end_date = datetime.strptime(end_date_string, "%Y%m%d").date() + timedelta(days=1)
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n)).strftime("%Y%m%d")

def generate_report(platform, start_date, end_date):
    output = "report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        for single_date in daterange(start_date, end_date, True):
            report_string = generate_report_at_date(platform, single_date, end_date)
            if report_string != None:
                out.write(report_string)
        out.close()

def generate_report_at_date(platform, date, end_date):
    reportstring = ""
    signup_usercount = 0
    with open("./etc/sign_up_user.csv") as file:
        firstopen_results = querysql("./sql/firstopen_user_id.sql", platform, date)
        firstopen_usercount = sum(1 for _ in firstopen_results)
        signup_results = querysql("./sql/signup_user_id.sql", platform, date)
        signup_usercount = sum(1 for _ in signup_results)
        if signup_usercount == 0 or firstopen_usercount == 0:
            return None;
        content = file.read()
        reportstring += content.format(platform, date, firstopen_usercount, signup_usercount, 100*float(signup_usercount)/float(firstopen_usercount))
        print("reportstring", reportstring)
        file.close()
    with open("./etc/lost_user_details.csv") as file:
        lines = file.readlines()
        reportstring += lines[0]
        report_lines = []
        signup_layers_progress_lines = [x.strip() for x in lines[1:4]]
        signup_layers_progress_results = querysql("./sql/signup_layers_progress.sql", platform, date)
        currentLayerIndex = 1
        activate_manto_user_count = 0
        signup_layers_progress_lines[0] = signup_layers_progress_lines[0].format(date)
        signup_layers_progress_lines[2] = signup_layers_progress_lines[2].format(signup_usercount, 100)
        signup_base_datas = []
        for k in range(1, signup_layers_progress_results[0].max_layer):
            signup_base_datas.append([k, 0, 0])
        for row in signup_layers_progress_results:
            for k in range(currentLayerIndex + 1, row.max_layer + 1):
                if k == row.max_layer:
                    signup_base_datas.append([k, row.user_count, 100*float(row.user_count)/float(signup_usercount)])
                else:
                    signup_base_datas.append([k, 0, 0])
                activate_manto_user_count += row.user_count
            currentLayerIndex = row.max_layer
        for k in range(currentLayerIndex + 1, max_layer + 1):
            signup_base_datas.append([k, 0, 0])
        activate_manto_one_count = signup_usercount - activate_manto_user_count
        signup_base_datas[0][1] = activate_manto_one_count
        signup_base_datas[0][2] = 100*float(activate_manto_one_count)/float(signup_usercount)
        for k in range(len(signup_base_datas)):
            data = signup_base_datas[k]
            signup_layers_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
        report_lines.extend(signup_layers_progress_lines)

        currentIndex = 1
        lost_base_datas = []
        lost_base_usercount = 0
        lost_base_day = ''
        for single_date in daterange(date, end_date):
            lost_day_results = querysql("./sql/layer_progress_of_lost_users.sql", platform, date, single_date)
            if currentIndex == 1:
                lost_day1_progress_lines = [x.strip() for x in lines[4:7]]
                currentLayerIndex = 1
                for k in range(1, lost_day_results[0].max_layer):
                    lost_base_datas.append((k, 0, 0))
                for row in lost_day_results:
                    for k in range(currentLayerIndex + 1, row.max_layer + 1):
                        if k == row.max_layer:
                            lost_base_datas.append([k, row.user_count, 100*float(row.user_count)/float(signup_usercount)])
                        else:
                            lost_base_datas.append([k, 0, 0])
                    currentLayerIndex = row.max_layer
                for k in range(currentLayerIndex + 1, max_layer + 1):
                    lost_base_datas.append([k, 0, 0])
                lost_base_usercount = sum(t[1] for t in lost_base_datas)
                lost_day1_progress_lines[0] = lost_day1_progress_lines[0].format(single_date)
                lost_day1_progress_lines[2] = lost_day1_progress_lines[2].format(lost_base_usercount, 100* float(lost_base_usercount)/float(signup_usercount))
                lost_base_day = single_date
                for k in range(len(lost_base_datas)):
                    data = lost_base_datas[k]
                    lost_day1_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
                for k in range(len(report_lines)):
                    report_lines[k] = report_lines[k] + lost_day1_progress_lines[k]
            else:
                current_lost_datas = []
                lost_day_progress_lines = [x.strip() for x in lines[7:]]
                currentLayerIndex = 1
                for k in range(1, lost_day_results[0].max_layer):
                    current_lost_datas.append((k, 0, 0))
                for row in lost_day_results:
                    for k in range(currentLayerIndex + 1, row.max_layer + 1):
                        if k == row.max_layer:
                            current_lost_datas.append([k, row.user_count, 100*float(row.user_count)/float(signup_usercount)])
                        else:
                            current_lost_datas.append([k, 0, 0])
                    currentLayerIndex = row.max_layer
                for k in range(currentLayerIndex + 1, max_layer + 1):
                    current_lost_datas.append([k, 0, 0])
                current_lost_usercount = sum(t[1] for t in current_lost_datas)
                lost_base_usercount = current_lost_usercount
                current_lost_usercount -= lost_base_usercount
                lost_day_progress_lines[0] = lost_day_progress_lines[0].format(single_date, lost_base_day)
                lost_day_progress_lines[2] = lost_day_progress_lines[2].format(current_lost_usercount, 100*float(current_lost_usercount)/float(signup_usercount))
                lost_base_day = single_date
                for k in range(len(current_lost_datas)):
                    data = current_lost_datas[k]
                    base_data = lost_base_datas[k]
                    lost_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1] - base_data[1], data[2] - base_data[2]))
                for k in range(len(report_lines)):
                    report_lines[k] = report_lines[k] + lost_day_progress_lines[k]
                lost_base_datas = current_lost_datas
            currentIndex += 1
        reportstring += '\n'.join(report_lines)
        reportstring += '\n\n'
        file.close()
    return reportstring

# Use like this: python unpacker.py [Image Path or Image Name(but no suffix)] [Texture uuid]
if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print("""
        You must pass platform(IOS/ANDROID) as the first parameter,
        report start date(YYYYMMDD) as second parameter,
        report end date(YYYYMMDD) as third parameter
        """)
        exit(1)
    # filename = sys.argv[1]
    platform = sys.argv[1]
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    generate_report(platform, start_date, end_date)
