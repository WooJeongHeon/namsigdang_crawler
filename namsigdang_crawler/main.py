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
import copy

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def make_path_dir(path_dir, bool):
    if not os.path.isdir(path_dir):
        os.mkdir(path_dir)

        if bool:
            write_all_log_file(path_dir + "경로가 없어 새로 생성 했습니다.")


def make_path_file(path_file):
    if not os.path.exists(path_file):
        logfile = open(path_file, 'w')
        logfile.close()
        write_all_log_file(path_file + "파일이 없어 새로 생성합니다.")


def write_all_log_file(logText):
    print(str(datetime.datetime.now()) + ": " + logText)

    logfile = open(path_all_log, 'a')
    logfile.writelines(str(datetime.datetime.now()) + ": " + logText + "\n")
    logfile.close()


def write_error_log_file(logText):
    logfile = open(path_error_log, 'a')
    logfile.writelines(str(datetime.datetime.now()) + ": " + logText + "\n")
    logfile.close()


def def_sleep():
    sleep_time_def = 8

    if sleep_time_def < 60:
        write_all_log_file(str(sleep_time_def) + "초 쉬기")
    else:
        write_all_log_file(str(sleep_time_def // 60) + "분 " + str(sleep_time_def % 60) + "초 쉬기")

    sleep(sleep_time_def)


# main Program

repeat_time = 0

while (True):

    try:
        repeat_time += 1

        my_date = datetime.date.today()  # 2019-04-07
        day_of_the_week = calendar.day_name[my_date.weekday()]  # Sunday
        my_date = str(my_date) + "-" + str(day_of_the_week)
        today_date = str(datetime.datetime.now())  # 2019-04-07 16:45:15.103445

        # Window path

        # path_dir_data = 'data'
        # path_dir_data_log = 'data\\log'
        # path_dir_data_all_log = 'data\\log\\all_log'
        # path_all_log = 'data\\log\\all_log\\all_log(' + my_date + ').txt'
        # path_error_log = 'data\\log\\error_log.txt'
        # path_change_DB_log = 'data\\log\\change_DB_log.txt'
        #
        # path_dir_data_crawling_menu = 'data\\crawling_menu'
        # path_this_week_menu_csv = 'data\\crawling_menu\\this_week_menu.csv'
        # path_backup_menu_csv = 'data\\crawling_menu\\backup_menu.csv'
        # path_all_menu_txt = 'data\\crawling_menu\\all_menu.txt'
        # path_all_menu_dat = 'data\\crawling_menu\\all_menu.dat'
        #
        # path_dir_data_account = 'data\\account'
        # path_account = 'data\\account\\account.txt'

        # Linux Server path

        path_dir_data = './data'
        path_dir_data_log = './data/log'
        path_dir_data_all_log = './data/log/all_log'
        path_all_log = './data/log/all_log/'+my_date[0:4]+'_year/'+my_date[5:7]+'_month/all_log(' + my_date + ').txt'
        path_error_log = './data/log/error_log.txt'
        path_change_DB_log = './data/log/change_DB_log.txt'

        path_dir_data_crawling_menu = './data/crawling_menu'
        path_this_week_menu_csv = './data/crawling_menu/this_week_menu.csv'
        path_backup_menu_csv = './data/crawling_menu/backup_menu.csv'
        path_all_menu_txt = './data/crawling_menu/all_menu.txt'
        path_all_menu_dat = './data/crawling_menu/all_menu.dat'

        path_dir_data_account = './data/account'
        path_account = './data/account/account.txt'

        make_path_dir(path_dir_data, False) # 아직 로그 경로가 없어 로그생성 False
        make_path_dir(path_dir_data_log, False)
        make_path_dir(path_dir_data_all_log, False)
        make_path_dir('./data/log/all_log/'+my_date[0:4]+'_year', False)
        make_path_dir('./data/log/all_log/'+my_date[0:4]+'_year/'+my_date[5:7]+'_month', True)
        make_path_dir(path_dir_data_account, True)
        make_path_dir(path_dir_data_crawling_menu, True)
        

        make_path_file(path_all_log)
        make_path_file(path_error_log)
        make_path_file(path_change_DB_log)

        write_all_log_file(str(repeat_time) + "회째 실행!")

        if not os.path.exists(path_all_menu_dat):
            write_all_log_file("\n\n\'" + path_all_menu_dat + "\' 파일이 없습니다.\n추가해 주세요!\n프로그램을 종료합니다.")
            break

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
        options.add_argument('headless') # 창 
        options.add_argument('window-size=1920x1080')
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        
        
        # WJH_running_server/namsigdang/namsigdang_crawler/namsigdang_crawler_2.0/setup_files/ChromeDriver_73.0.3683.68/chromedriver_linux64/chromedriver


        driver = webdriver.Chrome('./setup_files/ChromeDriver_73.0.3683.68/chromedriver_linux64/chromedriver', chrome_options=options)
        # driver = webdriver.Chrome('chromedriver.exe')
        write_all_log_file("크롬 드라이버 실행 완료")
        
        write_all_log_file("1초 쉬기..")
        sleep(1)
        

        driver.get("http://portal.ndhs.or.kr/index")
        write_all_log_file("남도학숙 사이트에 들어갔습니다.")

        driver.implicitly_wait(3)
        def_sleep()

        menu = driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/form/ul/li[2]/a').click()
        def_sleep()

        stuUserId = driver.find_element_by_id('stuUserId')
        stuUserId.send_keys(id)
        write_all_log_file("아이디 입력 완료")
        def_sleep()

        stuPassword = driver.find_element_by_id('stuPassword')
        stuPassword.send_keys(pw)
        write_all_log_file("비밀번호 입력 완료")
        def_sleep()

        driver.find_element_by_xpath('//*[@id="student"]/div/div[2]/button').click()  # Login 버튼 클릭
        write_all_log_file("로그인 버튼 클릭 완료")

        sleep(1)
        def_sleep()

        # WebDriverWait(driver, 5).until(EC.alert_is_present())  # (팝업창) 5초
        # driver.switch_to.alert.accept()  # 팝업창 확인 클릭
        # write_all_log_file("팝업창 확인 클릭 완료")

        # write_all_log_file("3초 쉬기..")
        # sleep(3)

        # def_sleep()

        # driver.find_element_by_xpath('//*[@id="sidebarButton"]/span').click()  # 메뉴 클릭 완료
        # write_all_log_file("메뉴 클릭 완료")
        # sleep(1)
        # def_sleep()

        # driver.find_element_by_xpath('//*[@id="left-meun"]/div[1]/ul/li[3]/a/span').click()  # 학생생활지원 클릭 완료
        # write_all_log_file("\'학생생활지원\' 클릭 완료")
        # sleep(1)
        # def_sleep()

        # driver.find_element_by_xpath('//*[@id="li_menu_Q0102"]/a').click()  # 식단표 클릭 완료
        # write_all_log_file("\'식단표\' 클릭 완료")
        # def_sleep()

        # driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[3]/div/div[2]/ul/li[1]/a').click()
        # driver.implicitly_wait(1)
        
        driver.get("http://portal.ndhs.or.kr/studentLifeSupport/carte/list")
        write_all_log_file("식단표 페이지로 이동했습니다.")

        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/h4/button[1]/i').click()  # 이전 주 보기 클릭
        write_all_log_file("\'이전주 보기\' 클릭 완료")
        sleep(1)
        def_sleep()

#         4번 반복!!
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
            
            # print("\n\n======================\n" + str(food_list) + "\n\n======================\n\n")

            for food_element in food_list:
                term = ""
                for term_ in regex_temp.findall(food_element[0])[0]:
                    term = term + str(term_)
                writer.writerow([term, food_element[1], food_element[2], food_element[3]])  # i.e) 20180910, 아침, 점심, 저녁
                compare_list.append([term, food_element[1], food_element[2], food_element[3]])
            file.close()
            
            # write_all_log_file("compare_list: " + str(compare_list))

            write_all_log_file("\'" + path_this_week_menu_csv + "\' 쓰기 완료")
            
            dic_parsing_menu = {}  # dic_menu 파일 초기화


            backup_file = open(path_backup_menu_csv, 'a', encoding='euc-kr', newline='')
            backup_writer = csv.writer(backup_file)
            for data in compare_list:
                backup_writer.writerow([data[0], data[1], data[2], data[3]])
                
                dic_parsing_menu["eu" + data[0] + "a"] = data[1] # eu20180514a
                dic_parsing_menu["eu" + data[0] + "b"] = data[2]
                dic_parsing_menu["eu" + data[0] + "c"] = data[3]
            backup_file.close()

            write_all_log_file("\'" + path_backup_menu_csv + "\' 쓰기 완료")
            write_all_log_file("\n---<dic_parsing_menu>---\n" + str(dic_parsing_menu) + "\n-------------------------")

            
            
            # # dictionary 만들기 (this_week_menu.csv 읽어와서 만드는 방법)
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
            write_all_log_file(path_all_menu_dat + "을 불러왔습니다.")
            file_all_menu_dat_old.close()

#          변동사항 확인하기 위해 dic_all_menu_old로 깊은 복사하여 백업.
            dic_all_menu_old = copy.deepcopy(dic_all_menu)

            dic_all_menu.update(dic_parsing_menu)
            write_all_log_file("크롤링한 데이터를 업데이트 했습니다.")
            
            
            
            file_all_menu_dat_new = open(path_all_menu_dat, 'wb')
            pickle.dump(dic_all_menu, file_all_menu_dat_new)
            write_all_log_file(path_all_menu_dat + "을 새로 작성했습니다.")
            file_all_menu_dat_new.close()
            

# --------------------------------------------------------------------------------------
# 날짜별로 DB 분류해서 따로 저장
# --------------------------------------------------------------------------------------
            error_dic = {}
            for y in sorted(dic_parsing_menu):   
                if y[0:2] == "eu":        
                    path_classify_dir_year = './data/crawling_menu/year_{}'.format(y[2:6])
                    path_classify_dir_month = './data/crawling_menu/year_{}/month_{}'.format(y[2:6], y[6:8])
                    path_classify = './data/crawling_menu/year_{}/month_{}/{}_menu.dat'.format(y[2:6], y[6:8], y[2:6] + "_" + y[6:8])

#                   경로가 존재하지 않으면 새로 생성
                    if not os.path.isdir(path_classify_dir_year):
                        os.mkdir(path_classify_dir_year)
                        write_all_log_file(path_classify_dir_year + "경로가 없어 새로 생성 했습니다.")
                
#                   경로가 존재하지 않으면 새로 생성
                    if not os.path.isdir(path_classify_dir_month):
                        os.mkdir(path_classify_dir_month)
                        write_all_log_file(path_classify_dir_month + "경로가 없어 새로 생성 했습니다.")

#                 파일이 존재하지 않을 경우 빈 파일 생성
                    if not os.path.exists(path_classify):
                        blank_dic = {}
                        f = open(path_classify, 'wb')
                        pickle.dump(blank_dic, f)
                        f.close()
                        write_all_log_file(path_classify + "파일이 없어 새로 생성합니다.")


#                 날짜별로 분류된 .dat 파일의 딕셔너리를 classified_dic로 저장
                    file_classified_dic_old = open(path_classify, 'rb')
                    classified_dic = pickle.load(file_classified_dic_old)
                    file_classified_dic_old.close()




                    classified_dic[y] = dic_parsing_menu[y]


#                 새로 .dat에 저장
                    file_classified_dic_new = open(path_classify, 'wb')
                    pickle.dump(classified_dic, file_classified_dic_new)
                    file_classified_dic_new.close()



                else:
                    write_all_log_file("조건에 만족하지 않아 날짜별 DB분류에 제외하였습니다.")
                    write_all_log_file("y[0:2]: {}".format(y[0:2]))
                    write_all_log_file("key값:{}".format(y))
                    error_dic[y] = dic_parsing_menu[y]

            write_all_log_file("DB를 날짜별로 분류해 저장하였습니다.")
            
            if len(error_dic) !=0:
                write_all_log_file("--<날짜별 DB분류에 제외된 dic>--\n" + str(error_dic))

#     --------------------------------------------------------------------------------------
            
            if dic_all_menu == dic_all_menu_old:
                write_all_log_file("기존 DB(all_menu.dat)의 변동사항이 없습니다.")
            else:
                write_all_log_file("\n***********기존 DB(all_menu.dat)가 새롭게 변경되었습니다!!!***********")
                keys = "(업데이트메뉴) 차집합 (기존메뉴) [keys]: >>" + str(set(dic_all_menu.keys())-set(dic_all_menu_old.keys()))
                values = "(업데이트메뉴) 차집합 (기존메뉴) [values]: >>" + str(set(dic_all_menu.values())-set(dic_all_menu_old.values()))
                write_all_log_file(keys)
                write_all_log_file(values + "\n********************************************\n")
        
                file_change_DB_log = open(path_change_DB_log, 'a')
                file_change_DB_log.writelines(
                        "[" + day_of_the_week + "]" + str(datetime.datetime.now()) + ": " + "기존 DB가 새롭게 변경되었습니다." + "\n")
                file_change_DB_log.writelines(keys + "\n")
                file_change_DB_log.writelines(values + "\n" + "\n")
                file_change_DB_log.close()
                
                write_all_log_file("\'{}\'에 DB의 변동사항을 기록했습니다.".format(path_change_DB_log))               
            
            
            

                
                

            

            driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/h4/button[2]/i').click()  # 다음주 보기 클릭
            write_all_log_file("\'다음주 보기\' 클릭 완료 (" + str(i) + "/ 4)")
            sleep(1)
            def_sleep()

#        all_menu.txt파일 새로 생성
        str_all_menu = str(dic_all_menu)
        file_all_menu_txt = open(path_all_menu_txt, 'w')
        file_all_menu_txt.writelines(str_all_menu)
        file_all_menu_txt.close()
        write_all_log_file(path_all_menu_txt + "를 새로 생성하였습니다.")

        write_all_log_file("[" + str(repeat_time) + "회째]: 성공적으로 크롤링을 마쳤습니다!!")

        driver.close()

        write_all_log_file("1시간 휴식..")
        sleep(60 * 60)
        write_all_log_file("/")

        random_time_sleep = random.randrange(60 * 60 * 10)

        if random_time_sleep < 60:
            write_all_log_file(str(random_time_sleep) + "초 추가로 휴식.. (랜덤 결과)")
            
        elif random_time_sleep < 60*60:
            write_all_log_file(str(random_time_sleep // 60) + "분 " + str(random_time_sleep % 60) + "초 추가로 휴식.. (랜덤 결과)")
            
        else:
            write_all_log_file(str(random_time_sleep // (60*60)) + "시간 " + str(random_time_sleep // 60) + "분 " + str(random_time_sleep % 60) + "초 추가로 휴식.. (랜덤 결과)")


        sleep(random_time_sleep)
        write_all_log_file("/")

        write_all_log_file("\n====================================================")
        write_all_log_file("====================================================\n")



    except Exception as e:
        error = str(e)
        write_all_log_file("\n\n\t***에러가 발생하였습니다ㅠㅠ")
        write_all_log_file(error + "\n")
        write_error_log_file(error + "\n")
        
        random_time_sleep = random.randrange(60 * 60 * 5)

        if random_time_sleep < 60:
            write_all_log_file(str(random_time_sleep) + "초 추가로 휴식.. (랜덤 결과) - 에러 휴식")
            
        elif random_time_sleep < 60*60:
            write_all_log_file(str(random_time_sleep // 60) + "분 " + str(random_time_sleep % 60) + "초 추가로 휴식.. (랜덤 결과)-에러휴식")
            
        else:
            write_all_log_file(str(random_time_sleep // (60*60)) + "시간 " + str(random_time_sleep // 60) + "분 " + str(random_time_sleep % 60) + "초 추가로 휴식.. (랜덤 결과)-에러휴식")

        sleep(random_time_sleep)
        write_all_log_file("/")
        
        
