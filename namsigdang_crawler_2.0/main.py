from time import sleep
import calendar
import csv
import datetime
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pickle
import random

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def write_all_log_file(logText):
    print(today_date + ": " + logText)

    logfile = open(path_all_log, 'a')
    logfile.writelines(today_date + ": " + logText + "\n")
    logfile.close()


def write_error_log_file(logText):
    logfile = open(path_error_log, 'a')
    logfile.writelines(today_date + ": " + logText + "\n")
    logfile.close()


# main Program

repeat_time = 0

while (True):

    try:
        repeat_time += 1
        print(str(repeat_time) + "회째 실행!")

        path_all_log = './data/log/all_log.txt'
        path_error_log = './data/log/error_log.txt'
        path_change_DB_log = './data/log/change_DB_log.txt'
        path_this_week_menu_csv = './data/crawling_menu/this_week_menu.csv'
        path_backup_menu_csv = './data/crawling_menu/backup_menu.csv'
        path_all_menu_txt = './data/crawling_menu/all_menu.txt'
        path_account = './data/account/account.txt'
        path_all_menu_dat = './data/crawling_menu/all_menu.dat'

        my_date = datetime.date.today()  # 2019-04-07
        day_of_the_week = calendar.day_name[my_date.weekday()]  # Sunday
        today_date = str(datetime.datetime.now())  # 2019-04-07 16:45:15.103445

        if not os.path.exists(path_all_log):
            logfile = open(path_all_log, 'w')
            logfile.close()
            write_all_log_file(path_all_log + "파일이 없어 새로 생성합니다.")

        if not os.path.exists(path_error_log):
            logfile = open(path_error_log, 'w')
            logfile.close()
            write_all_log_file(path_error_log + "파일이 없어 새로 생성합니다.")

        if not os.path.exists(path_change_DB_log):
            logfile = open(path_change_DB_log, 'w')
            logfile.close()
            write_all_log_file(path_change_DB_log + "파일이 없어 새로 생성합니다.")

        if not os.path.exists(path_account):
            write_all_log_file("계정 파일이 없어 새로 생성합니다.")
            accountfile = open(path_account, 'w')
            accountfile.writelines(input("ID를 입력하세요: "))
            accountfile.writelines("\n")
            accountfile.writelines(input("PW를 입력하세요: "))
            accountfile.close()
        file = open(path_account, 'r')
        reader = file.readlines()
        account_list = []
        for data in reader:
            account_list.append(data.replace('\n', ''))
        id = account_list[0]
        pw = account_list[1]

        write_all_log_file("데이터 수집을 시작합니다.")

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("--disable-gpu")
        # options.add_argument("disable-gpu")


        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome('chromedriver', chrome_options=options)

        driver.get("http://portal.ndhs.or.kr/index")
        write_all_log_file("남도학숙 사이트에 들어갔습니다.")

        driver.implicitly_wait(3)

        menu = driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/form/ul/li[2]/a').click()

        stuUserId = driver.find_element_by_id('stuUserId')
        stuUserId.send_keys(id)
        write_all_log_file("아이디 입력 완료")

        stuPassword = driver.find_element_by_id('stuPassword')
        stuPassword.send_keys(pw)
        write_all_log_file("비밀번호 입력 완료")

        driver.find_element_by_xpath('//*[@id="student"]/div/div[2]/button').click()  # Login 버튼 클릭
        write_all_log_file("로그인 버튼 클릭 완료")

        sleep(1)

        WebDriverWait(driver, 5).until(EC.alert_is_present())  # (팝업창) 5초
        driver.switch_to.alert.accept()  # 팝업창 확인 클릭
        write_all_log_file("팝업창 확인 클릭 완료")

        sleep(1)

        # driver.find_element_by_xpath('//*[@id="sidebarButton"]/span').click()  # 메뉴 클릭 완료
        # write_all_log_file("메뉴 클릭 완료")
        # sleep(1)

        driver.find_element_by_xpath('//*[@id="left-meun"]/div[1]/ul/li[3]/a/span').click()  # 학생생활지원 클릭 완료
        write_all_log_file("\'학생생활지원\' 클릭 완료")
        sleep(1)

        driver.find_element_by_xpath('//*[@id="li_menu_Q0102"]/a').click()  # 식단표 클릭 완료
        write_all_log_file("\'식단표\' 클릭 완료")

        # driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[3]/div/div[2]/ul/li[1]/a').click()
        # driver.implicitly_wait(1)

        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/h4/button[1]/i').click()  # 이전 주 보기 클릭
        write_all_log_file("\'이전주 보기\' 클릭 완료")
        sleep(1)

        for i in range(1, 5):

            html = BeautifulSoup(driver.page_source, 'lxml')

            food = html.find_all('tr', attrs={'style': 'height:80px'})
            write_all_log_file("{'style': 'height:80px'} 검색 완료")

            tag_list = ['</th>', '<td>', '<tr style="height:80px">', '</tr>', '</td>', '<th>',
                        '<th style="color:red;">',
                        '\n', '\t']
            food_list = []
            for food_ in food:
                temp_list = []
                for food__ in food_:
                    if food__ != '\n':
                        for tag in tag_list:
                            food__ = re.sub(tag, '', str(food__))
                        temp_list.append(food__)
                food_list.append(temp_list)

            file = open(path_this_week_menu_csv, 'w', encoding='euc-kr', newline='')
            writer = csv.writer(file)
            compare_list = []
            regex_temp = re.compile('(?P<year>\d+)년+ (?P<month>\d+)월+ (?P<day>\d+)일')

            for food_element in food_list:
                term = ""
                for term_ in regex_temp.findall(food_element[0])[0]:
                    term = term + str(term_)
                writer.writerow([term, food_element[1], food_element[2], food_element[3]])  # i.e) 20180910, 아침, 점심, 저녁
                compare_list.append([term, food_element[1], food_element[2], food_element[3]])
            file.close()
            write_all_log_file("compare_list: " + str(compare_list))

            write_all_log_file("\'" + path_this_week_menu_csv + "\' 쓰기 완료")

            backup_file = open(path_backup_menu_csv, 'a', encoding='euc-kr', newline='')
            backup_writer = csv.writer(backup_file)
            for data in compare_list:
                backup_writer.writerow([data[0], data[1], data[2], data[3]])
            backup_file.close()

            write_all_log_file("\'" + path_backup_menu_csv + "\' 쓰기 완료")

            # dictionary 만들기
            file = open(path_this_week_menu_csv, 'r', encoding='euc-kr')
            reader = csv.reader(file)

            dic_parsing_menu = {}  # dic_menu 파일 초기화
            # eu20180514c
            for data in reader:
                dic_parsing_menu["eu" + data[0] + "a"] = data[1]
                dic_parsing_menu["eu" + data[0] + "b"] = data[2]
                dic_parsing_menu["eu" + data[0] + "c"] = data[3]
            file.close()

            write_all_log_file("dic_parsing_menu: " + str(dic_parsing_menu))

            file_all_menu_dat_old = open(path_all_menu_dat, 'rb')
            dic_all_menu = pickle.load(file_all_menu_dat_old)
            write_all_log_file(path_all_menu_dat + "을 불러왔습니다.")
            file_all_menu_dat_old.close()

            # dic_all_menu_old = dic_all_menu

            dic_all_menu.update(dic_parsing_menu)
            write_all_log_file("크롤링한 데이터를 업데이트 했습니다.")

            # if dic_all_menu_old == dic_all_menu:
            #     write_all_log_file("기존 DB의 변동사항이 없습니다.")
            # else:
            #     write_all_log_file("기존 DB가 새롭게 변경되었습니다.")
            #
            #     file_change_DB_log = open(path_change_DB_log, 'a')
            #     file_change_DB_log.writelines(
            #         "[" + day_of_the_week + "]" + today_date + ": " + "기존 DB가 새롭게 변경되었습니다." + "\n")
            #     file_change_DB_log.close()

            file_all_menu_dat_new = open(path_all_menu_dat, 'wb')
            pickle.dump(dic_all_menu, file_all_menu_dat_new)
            write_all_log_file(path_all_menu_dat + "을 새로 작성했습니다.")
            file_all_menu_dat_new.close()

            driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/h4/button[2]/i').click()  # 다음주 보기 클릭
            write_all_log_file("\'다음주 보기\' 클릭 완료 (" + str(i) + "/ 4)")
            sleep(1)

        str_all_menu = str(dic_all_menu)

        file_all_menu_txt = open(path_all_menu_txt, 'w')
        file_all_menu_txt.writelines(str_all_menu)
        file_all_menu_txt.close()
        write_all_log_file(path_all_menu_txt + "를 새로 생성하였습니다.")

        write_all_log_file("[" + str(repeat_time) + "회째]: 성공적으로 크롤링을 마쳤습니다!!")

        driver.close()

        write_all_log_file("1hour 휴식..")
        sleep(60*60)

        random_time_sleep = random.randrange(60*60)
        write_all_log_file(str(random_time_sleep) + "초 추가로 휴식.. (랜덤 결과)")
        sleep(random_time_sleep)

        write_all_log_file("\n====================================================\n")



    except Exception as e:
        error = str(e)
        write_all_log_file("\n\n\t***에러가 발생하였습니다ㅠㅠ")
        write_all_log_file(error + "\n")

        write_error_log_file(error + "\n")
