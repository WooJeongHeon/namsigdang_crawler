#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import os
import re
import pickle
import copy
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from data_path import project_path, path_dir_data, path_dir_data_log, path_dir_data_all_log, path_all_log, \
    path_error_log, \
    path_change_DB_log, path_dir_data_crawling_menu, path_this_week_menu_csv, path_backup_menu_csv, path_all_menu_txt, \
    path_all_menu_dat, path_dir_data_account, path_account
from make_log import write_log, slack_msg
from environment_composition import create_env, check_all_menu_dat, check_account
from my_date import my_date, day_of_the_week, today_date, today_year, today_month
from firebase_db import fb_cred, fb_db


def def_sleep():
    sleep_time_def = 5

    if sleep_time_def < 60:
        write_log(str(sleep_time_def) + "초 쉬기")
    else:
        write_log(str(sleep_time_def // 60) + "분 " + str(sleep_time_def % 60) + "초 쉬기")

    sleep(sleep_time_def)
    write_log("/")


# main Program
try:
    start_time = time.time()  # 시작 시간 저장

    create_env()

    if not check_all_menu_dat():  # all_menu_dat이 존재하지 않을때
        print("check_all_menu_dat: False")

    my_id, my_pw = check_account()

    write_log(f"데이터 수집을 시작합니다.", send_slack=True)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 창 숨기기
    options.add_argument('window-size=1920x1080')
    options.add_argument("--disable-gpu")  # 그래픽 가속 비활성화 (일부 버전에서 크롬 GPU 버그 이슈가 있음)
    options.add_argument("lang=ko_KR")  # 한국어
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')  # 리소스에 대한 액세스를 방지
    options.add_argument('--disable-dev-shm-usage')  # dev/shm을 공유하지 않음 (메모리 부족으로 인한 오류 방지)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    write_log("크롬 드라이버 실행 완료")

    write_log("1초 쉬기..")
    sleep(1)

    driver.get("http://portal.ndhs.or.kr/index")
    write_log("남도학숙 사이트에 들어갔습니다.")

    driver.implicitly_wait(3)
    def_sleep()

    driver.find_element(By.XPATH,
                        '/html/body/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/form/ul/li[2]/a').click()
    def_sleep()

    stuUserId = driver.find_element(By.ID, 'stuUserId')
    stuUserId.send_keys(my_id)
    write_log("아이디 입력 완료")
    def_sleep()

    stuPassword = driver.find_element(By.ID, 'stuPassword')
    stuPassword.send_keys(my_pw)
    write_log("비밀번호 입력 완료")
    def_sleep()

    driver.find_element(By.XPATH, '//*[@id="student"]/div/div[2]/button').click()  # Login 버튼 클릭
    write_log("로그인 버튼 클릭 완료")

    sleep(1)
    def_sleep()

    # WebDriverWait(driver, 5).until(EC.alert_is_present())  # (팝업창) 5초
    # driver.switch_to.alert.accept()  # 팝업창 확인 클릭
    # write_log("팝업창 확인 클릭 완료")
    #
    # write_log("3초 쉬기..")
    # sleep(3)
    #
    # def_sleep()

    # driver.find_element(By.XPATH,'//*[@id="sidebarButton"]/span').click()  # 메뉴 클릭 완료
    # write_all_log_file("메뉴 클릭 완료")
    # sleep(1)
    # def_sleep()

    # driver.find_element(By.XPATH,'//*[@id="left-meun"]/div[1]/ul/li[3]/a/span').click()  # 학생생활지원 클릭 완료
    # write_all_log_file("\'학생생활지원\' 클릭 완료")
    # sleep(1)
    # def_sleep()

    # driver.find_element(By.XPATH,'//*[@id="li_menu_Q0102"]/a').click()  # 식단표 클릭 완료
    # write_all_log_file("\'식단표\' 클릭 완료")
    # def_sleep()

    # driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[3]/div[3]/div/div[2]/ul/li[1]/a').click()
    # driver.implicitly_wait(1)

    driver.get("http://portal.ndhs.or.kr/studentLifeSupport/carte/list")
    write_log("식단표 페이지로 이동했습니다.")

    driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/h4/button[1]/i').click()  # 이전 주 보기 클릭
    write_log("\'이전주 보기\' 클릭 완료")
    sleep(1)
    def_sleep()

    # 4번 반복!!
    for i in range(1, 5):

        html = BeautifulSoup(driver.page_source, 'lxml')

        food = html.find_all('tr', attrs={'style': 'height:80px'})
        write_log("{'style': 'height:80px'} 검색 완료")

        tag_list = ['</th>', '<td>', '<tr style="height:80px">', '</tr>', '</td>', '<th>', '<th style="color:red;">',
                    '\n', '\t']
        food_list = []
        for food_ in food:
            temp_list = []
            for food__ in food_:
                if food__ != '\n':
                    for tag in tag_list:
                        food__ = re.sub(tag, '', str(food__))

                    food__ = re.sub('&amp;', '&', str(food__))  # &amp를 &로 변환

                    temp_list.append(food__)
            food_list.append(temp_list)

        file = open(path_this_week_menu_csv, 'w', encoding='euc-kr', newline='')
        writer = csv.writer(file)
        compare_list = []
        regex_temp = re.compile('(?P<year>\d+)년+ (?P<month>\d+)월+ (?P<day>\d+)일')

        # print("\n\n======================\n" + str(food_list) + "\n\n======================\n\n")

        for food_element in food_list:
            term = ""
            for term_ in regex_temp.findall(food_element[0])[0]:
                term = term + str(term_)
            writer.writerow([term, food_element[1], food_element[2], food_element[3]])  # i.e) 20180910, 아침, 점심, 저녁
            compare_list.append([term, food_element[1], food_element[2], food_element[3]])
        file.close()

        # write_all_log_file("compare_list: " + str(compare_list))

        write_log("\'" + path_this_week_menu_csv + "\' 쓰기 완료")

        dic_parsing_menu = {}  # dic_menu 파일 초기화

        backup_file = open(path_backup_menu_csv, 'a', encoding='euc-kr', newline='')
        backup_writer = csv.writer(backup_file)
        for data in compare_list:
            backup_writer.writerow([data[0], data[1], data[2], data[3]])

            dic_parsing_menu["eu" + data[0] + "a"] = data[1]  # eu20180514a
            dic_parsing_menu["eu" + data[0] + "b"] = data[2]
            dic_parsing_menu["eu" + data[0] + "c"] = data[3]
        backup_file.close()

        write_log("\'" + path_backup_menu_csv + "\' 쓰기 완료")
        write_log("\n---<dic_parsing_menu>---\n" + str(dic_parsing_menu) + "\n-------------------------")

        # # dictionary 만들기 (this_week_menu.csv 읽어와서 만들기)
        # file = open(path_this_week_menu_csv, 'r', encoding='euc-kr')
        # reader = csv.reader(file)

        # dic_parsing_menu = {}  # dic_menu 파일 초기화
        # # eu20180514c
        # for data in reader:
        #     dic_parsing_menu["eu" + data[0] + "a"] = data[1]
        #     dic_parsing_menu["eu" + data[0] + "b"] = data[2]
        #     dic_parsing_menu["eu" + data[0] + "c"] = data[3]
        # file.close()
        # write_all_log_file("dic_parsing_menu: " + str(dic_parsing_menu))

        file_all_menu_dat_old = open(path_all_menu_dat, 'rb')
        dic_all_menu = pickle.load(file_all_menu_dat_old)
        write_log(path_all_menu_dat + "을 불러왔습니다.")
        file_all_menu_dat_old.close()

        # 변동사항 확인하기 위해 dic_all_menu_old로 깊은 복사하여 백업.
        dic_all_menu_old = copy.deepcopy(dic_all_menu)

        dic_all_menu.update(dic_parsing_menu)
        write_log("크롤링한 데이터를 업데이트 했습니다.")

        file_all_menu_dat_new = open(path_all_menu_dat, 'wb')
        pickle.dump(dic_all_menu, file_all_menu_dat_new)
        write_log(path_all_menu_dat + "을 새로 작성했습니다.")
        file_all_menu_dat_new.close()

        # --------------------------------------------------------------------------------------
        # 날짜별로 DB 분류해서 따로 저장
        # --------------------------------------------------------------------------------------
        error_dic = {}
        for y in sorted(dic_parsing_menu):
            if y[0:2] == "eu":
                path_classify_dir_year = path_dir_data_crawling_menu + '/year_{}'.format(y[2:6])
                path_classify_dir_month = path_classify_dir_year + '/month_{}'.format(y[6:8])
                path_classify = path_classify_dir_month + '/{}_menu.dat'.format(y[2:6] + "_" + y[6:8])

                # 경로가 존재하지 않으면 새로 생성
                if not os.path.isdir(path_classify_dir_year):
                    os.mkdir(path_classify_dir_year)
                    write_log(path_classify_dir_year + "경로가 없어 새로 생성 했습니다.")

                # 경로가 존재하지 않으면 새로 생성
                if not os.path.isdir(path_classify_dir_month):
                    os.mkdir(path_classify_dir_month)
                    write_log(path_classify_dir_month + "경로가 없어 새로 생성 했습니다.")

                # 파일이 존재하지 않을 경우 빈 파일 생성
                if not os.path.exists(path_classify):
                    blank_dic = {}
                    f = open(path_classify, 'wb')
                    pickle.dump(blank_dic, f)
                    f.close()
                    write_log(path_classify + "파일이 없어 새로 생성합니다.")

                # 날짜별로 분류된 .dat 파일의 딕셔너리를 classified_dic로 저장
                file_classified_dic_old = open(path_classify, 'rb')
                classified_dic = pickle.load(file_classified_dic_old)
                file_classified_dic_old.close()

                classified_dic[y] = dic_parsing_menu[y]

                # 새로 .dat에 저장
                file_classified_dic_new = open(path_classify, 'wb')
                pickle.dump(classified_dic, file_classified_dic_new)
                file_classified_dic_new.close()

                # firestore에 메뉴 저장
                try:
                    fb_ref_eun_menu = fb_db.collection('menu').document('Eunpyeong').collection(
                        f'year_{y[2:6]}').document(f'month_{y[6:8]}')
                    fb_ref_eun_menu.set({y: dic_parsing_menu[y]}, merge=True)

                except Exception as e:
                    error = str(e)
                    write_log("\n\n\t***firestore에 메뉴 저장 중 에러 발생", send_slack=True)
                    write_log(log_text=error + "\n", log_files=[path_all_log, path_error_log], send_slack=True)


            else:
                write_log("조건에 만족하지 않아 날짜별 DB분류에 제외하였습니다.")
                write_log("y[0:2]: {}".format(y[0:2]))
                write_log("key값:{}".format(y))
                error_dic[y] = dic_parsing_menu[y]

        write_log("날짜별로 분류해 DB에 저장하였습니다.")

        if len(error_dic) != 0:
            write_log("--<날짜별 DB분류에 제외된 dic>--\n" + str(error_dic))

        #     --------------------------------------------------------------------------------------

        if dic_all_menu == dic_all_menu_old:
            write_log("기존 DB(all_menu.dat)의 변동사항이 없습니다.")
        else:
            write_log("\n***********기존 DB(all_menu.dat)가 새롭게 변경되었습니다!!!***********")
            keys = "(업데이트메뉴) 차집합 (기존메뉴) [keys]: >>" + str(set(dic_all_menu.keys()) - set(dic_all_menu_old.keys()))
            values = "(업데이트메뉴) 차집합 (기존메뉴) [values]: >>" + str(
                set(dic_all_menu.values()) - set(dic_all_menu_old.values()))
            write_log(keys)
            write_log(values + "\n********************************************\n")

            write_log(log_text=f"기존 DB가 새롭게 변경되었습니다.\n변경 요일: {day_of_the_week()}\n{keys}\n{values}\n\n",
                      log_files=[path_all_log, path_change_DB_log], send_slack=True)

            # firestore에 메뉴 변동사항 저장
            try:

                fb_ref_eun_update_info = fb_db.collection('event').document(
                    "Eunpyeong_menu_update_info").collection(f'year_{today_year()}').document(
                    f'month_{today_month()}')
                fb_ref_eun_update_info.set(
                    {today_date(): {"day_of_the_week()": day_of_the_week(), "update_keys": keys,
                                    "update_values": values}}, merge=True)

                write_log("firestore에 변동사항 정보를 기록하였습니다.")


            except Exception as e:
                error = str(e)
                write_log("\n\n\t***firestore에 메뉴 변동사항 저장 중 에러 발생", send_slack=True)
                write_log(log_text=error + "\n", log_files=[path_all_log, path_error_log], send_slack=True)

        driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/h4/button[2]/i').click()  # 다음주 보기 클릭
        write_log("\'다음주 보기\' 클릭 완료 (" + str(i) + "/ 4)")
        sleep(1)
        def_sleep()

    # all_menu.txt파일 새로 생성
    str_all_menu = str(dic_all_menu)
    file_all_menu_txt = open(path_all_menu_txt, 'w')
    file_all_menu_txt.writelines(str_all_menu)
    file_all_menu_txt.close()
    write_log(path_all_menu_txt + "를 새로 생성하였습니다.")

    running_time = time.time() - start_time  # 현재시각 - 시작시간 = 실행 시간
    running_time = round(running_time, 3)

    write_log(f"성공적으로 크롤링을 마쳤습니다!! (실행시간: {running_time}sec)", send_slack=True)

    driver.close()

    write_log("\n")
    write_log("====================================================")
    write_log("====================================================\n")



except Exception as e:
    error = str(e)
    write_log("\n\n\t***에러가 발생하였습니다ㅠㅠ", send_slack=True)
    write_log(log_text=error + "\n", log_files=[path_all_log, path_error_log], send_slack=True)
