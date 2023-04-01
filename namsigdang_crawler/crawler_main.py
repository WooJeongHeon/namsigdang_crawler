#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time
import html

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from slack import slack_msg
from firebase_db import fb_db
from data.account import portal_account
import constants.web_element as element
import constants.campus_key as campus_key


def def_sleep(sleep_time_def=1.2):
    if sleep_time_def < 60:
        print(f"sleep {sleep_time_def}sec", end=" ")
    else:
        print(f"sleep {sleep_time_def // 60}min {sleep_time_def % 60}sec", end=" ")
    time.sleep(sleep_time_def)
    print("..done")


headless_options = webdriver.ChromeOptions()
headless_options.add_argument('--headless')  # 창 숨기기
headless_options.add_argument('--no-sandbox')  # 리소스에 대한 액세스를 방지
headless_options.add_argument("--disable-gpu")  # 그래픽 가속 비활성화 (일부 버전에서 크롬 GPU 버그 이슈가 있음)
headless_options.add_argument("--window-size=1280x1696")
headless_options.add_argument("--single-process")
headless_options.add_argument("--disable-dev-shm-usage")  # dev/shm을 공유하지 않음 (메모리 부족으로 인한 오류 방지)
headless_options.add_argument("--disable-dev-tools")
headless_options.add_argument("--no-zygote")
headless_options.add_argument(
    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')


def get_driver_default():
    driver = webdriver.Chrome()
    return driver


def get_driver_local():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver


def get_driver_python_docker():
    chromedriver_docker = "/home/namsigdang-crawler/chromedriver/chromedriver"
    driver = webdriver.Chrome(chromedriver_docker, options=headless_options)

    return driver


def get_driver_aws_lambda_docker():
    headless_options.binary_location = '/opt/chrome/chrome'
    driver = webdriver.Chrome("/opt/chromedriver", options=headless_options)
    return driver


def get_driver_aws_lambda_layer():
    chromedriver_aws_lambda = "/opt/python/bin/chromedriver"
    driver = webdriver.Chrome(chromedriver_aws_lambda, options=headless_options)
    return driver


# main Program
def namsigdang_crawler(chrome_driver_option):
    try:
        start_time = time.time()  # 시작 시간 저장

        my_id = portal_account.eunpyeong_id
        my_pw = portal_account.eunpyeong_pw

        slack_msg(f"데이터 수집을 시작합니다.")

        driver_options = {
            "default": get_driver_default,
            "local": get_driver_local,
            "python_docker": get_driver_python_docker,
            "aws_lambda_docker": get_driver_aws_lambda_docker,
            "aws_lambda_layer": get_driver_aws_lambda_layer,
        }

        driver = driver_options.get(chrome_driver_option, lambda: Exception("chrome_driver_option is not valid"))()
        if isinstance(driver, Exception):
            raise driver

        print("크롬 드라이버 실행 완료")
        def_sleep(1)

        driver.get("http://portal.ndhs.or.kr/index")
        print("남도학숙 사이트에 들어갔습니다.")

        driver.implicitly_wait(3)
        def_sleep()

        driver.find_element(By.XPATH, element.staff).click()
        def_sleep()

        stuUserId = driver.find_element(By.ID, element.staff_id)
        stuUserId.send_keys(my_id)
        print("아이디 입력 완료")
        def_sleep()

        stuPassword = driver.find_element(By.ID, element.staff_pw)
        stuPassword.send_keys(my_pw)
        print("비밀번호 입력 완료")
        def_sleep()

        driver.find_element(By.XPATH, element.staff_login_btn).click()  # Login 버튼 클릭
        print("로그인 버튼 클릭 완료")

        def_sleep(1)
        def_sleep()

        # WebDriverWait(driver, 5).until(EC.alert_is_present())  # (팝업창) 5초
        # driver.switch_to.alert.accept()  # 팝업창 확인 클릭
        # print("팝업창 확인 클릭 완료")
        #
        # print("3초 쉬기..")
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

        driver.get(element.menu_url)
        print("식단표 페이지로 이동했습니다.")

        driver.find_element(By.XPATH, element.before_week_btn).click()  # 이전 주 보기 클릭
        print("\'이전주 보기\' 클릭 완료")
        def_sleep(0.6)
        def_sleep()

        repeat = 4  # 4번 반복!!
        for i in range(repeat):

            menu_html = BeautifulSoup(driver.page_source, 'html.parser')

            dic_parsing_menu = {}  # dic_menu 파일 초기화

            for tr in menu_html.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) > 0:
                    date_str = tr.th.get_text().strip()
                    date = re.findall(r'\d+', date_str)  # 숫자만 추출
                    date = ''.join(date)  # 리스트를 문자열로 변환
                    for meal_index, td in enumerate(tds):
                        if meal_index > 2:
                            raise Exception("Error occurred in parsing menu")
                        meal = chr(ord('a') + meal_index)  # a, b, c 순서로 문자 생성
                        key = campus_key.eunpyeong_code + date + meal  # key를 생성
                        dic_parsing_menu[key] = html.unescape(td.get_text().strip())

            print("dic_parsing_menu:", dic_parsing_menu)

            error_dic = {}
            for y in sorted(dic_parsing_menu):
                if y[0:2] == campus_key.eunpyeong_code:

                    # firestore에 메뉴 저장
                    try:
                        fb_ref_eun_menu = fb_db.collection('menu').document(
                            campus_key.firebase_eunpyeong_document).collection(f'year_{y[2:6]}').document(
                            f'month_{y[6:8]}')
                        fb_ref_eun_menu.set({y: dic_parsing_menu[y]}, merge=True)

                    except Exception as e:
                        error = str(e)
                        slack_msg("`firestore에 메뉴 저장 중 에러 발생`")
                        slack_msg(error + "\n")


                else:
                    print("조건에 만족하지 않아 날짜별 DB분류에 제외하였습니다.")
                    print("y[0:2]: {}".format(y[0:2]))
                    print("key값:{}".format(y))
                    error_dic[y] = dic_parsing_menu[y]

            print("날짜별로 분류해 DB에 저장하였습니다.")

            if len(error_dic) != 0:
                print("--<날짜별 DB분류에 제외된 dic>--\n" + str(error_dic))

            #     --------------------------------------------------------------------------------------

            driver.find_element(By.XPATH, element.after_week_btn).click()  # 다음주 보기 클릭
            print(f"\'다음주 보기\' 클릭 완료 ({i + 1}/{repeat})")
            def_sleep(0.6)
            def_sleep()

        running_time = time.time() - start_time  # 현재시각 - 시작시간 = 실행 시간
        running_time = round(running_time, 3)

        driver.close()  # 브라우저 화면만 닫습니다.

        slack_msg(f"성공적으로 크롤링을 마쳤습니다!! (실행시간: {running_time}sec)")





    except Exception as e:
        error = str(e)
        slack_msg("\n\n\t***에러가 발생하였습니다ㅠㅠ")
        slack_msg(error + "\n")

    # finally:
    #     driver.quit()  # 브라우저를 닫고, 프로세스도 종료합니다.


if __name__ == '__main__':
    chrome_driver_option = "default"
    namsigdang_crawler(chrome_driver_option)
