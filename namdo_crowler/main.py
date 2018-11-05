from datetime import date
from time import sleep
from namdo import *
from dictionary_load import *
import calendar
import csv
import datetime
import os

chrome = namtochrome()
dictionary_load = dataload()
path_log = 'Data\\log.txt'
path_food = 'Food\\food.csv'

if os.path.exists(path_log):
    pass
else:
    print("log 파일이 없어 새로 생성합니다.")
    logfile = open(path_log, 'w')
    logfile.close()

while (True):
    try:
        print("데이터 수집을 시작합니다")
        weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        my_date = date.today()
        today = calendar.day_name[my_date.weekday()]
        today_date = str(datetime.datetime.now())

        if today == weekday[0]:  # 특정 요일에만 데이터를 가져옴
            chrome.launch()
            file = open(path_food, 'r', encoding='euc-kr')
            reader = csv.reader(file)
            bool_data_state = False

            for data in reader:
                # print(data[0][0:4], today_date[0:4], data[0][4:6], today_date[5:7], data[0][6:8], today_date[8:10])

                if data[0][0:4] == today_date[0:4] and data[0][4:6] == today_date[5:7] and data[0][6:8] == today_date[
                                                                                                           8:10]:  # 다운 받은 데이터와 날짜가 일치하는 경우
                    bool_data_state = True
                    dictionary_load.load()
                    print(str(datetime.datetime.now()) + ": " + "데이터를 불러 왔습니다.")
                    logfile = open(path_log, 'a')
                    logfile.writelines(str(datetime.datetime.now()) + ": " + "데이터를 불러 왔습니다.\n")
                    logfile.close()
                    file.close()
                    sleep(86400 * 5)

            if bool_data_state:
                print(data[0][0:4], today_date[0:4], data[0][4:6], today_date[5:7], data[0][6:8], today_date[8:10])
                print(str(datetime.datetime.now()) + ": " + "데이터를 불러왔지만 날짜에 일치하는 데이터가 없습니다.")
                logfile = open(path_log, 'a')
                logfile.writelines(str(datetime.datetime.now()) + ": " + "데이터를 불러왔지만 날짜에 일치하는 데이터가 없습니다.\n")
                logfile.close()
                file.close()
                sleep(3600)

        else:
            logfile = open(path_log, 'a')
            print(str(datetime.datetime.now()) + ": " + "요일에 일치하는 데이터가 없습니다.")
            logfile.writelines(str(datetime.datetime.now()) + ": " + "요일에 일치하는 데이터가 없습니다.\n")
            logfile.close()
            sleep(3600)

    except Exception as ex:
        error = str(ex)
        logfile = open(path_log, 'a')
        print(str(datetime.datetime.now()) + ": " + error)
        logfile.writelines(str(datetime.datetime.now()) + ": " + error + "\n")
        logfile.close()
