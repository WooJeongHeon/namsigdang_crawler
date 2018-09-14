from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from namdo_crowler import account
import csv
import re

class namtochrome:
    def backup_csv_remove_overlap(self, list):
        path_backup_food = 'Food\\backup_food.csv'
        backup_file = open(path_backup_food, 'a', encoding='euc-kr', newline='')
        backup_writer = csv.writer(backup_file)
        for data in list:
            backup_writer.writerow([data[0], data[1], data[2], data[3]])
        backup_file.close()

    def launch(self):
        path_food = 'Food\\food.csv'

        driver = webdriver.Chrome('chromedriver.exe')
        driver.get("http://portal.ndhs.or.kr/index")
        driver.implicitly_wait(3)

        menu = driver.find_element_by_xpath(
            '/html/body/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/form/ul/li[2]/a').click()

        id = driver.find_element_by_id('stuUserId')
        acc = account.Account()
        id_pw = acc.account_load()
        id.send_keys(id_pw[0])
        pw = driver.find_element_by_id('stuPassword')
        pw.send_keys(id_pw[1])

        driver.find_element_by_xpath('//*[@id="student"]/div/div[2]/button').click()
        sleep(4)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[3]/div/div[2]/ul/li[1]/a').click()
        driver.implicitly_wait(1)

        html = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()
        food = html.find_all('tr', attrs={'style': 'height:80px'})

        tag_list = ['</th>', '<td>', '<tr style="height:80px">', '</tr>', '</td>', '<th>', '<th style="color:red;">','\n','\t']
        food_list = []
        for food_ in food:
            temp_list = []
            for food__ in food_:
                if food__ != '\n':
                    for tag in tag_list:
                        food__ = re.sub(tag, '', str(food__))
                    temp_list.append(food__)
            food_list.append(temp_list)

        """food_list = []
        tag_list = ['</th>', '<td>', '<tr style="height:80px">', '</tr>', '</td>', '<th>', '<th style="color:red;">', '\n', '\t']
        for food_item in temp_food_list:
            for tag in tag_list:
                food_item = re.sub(tag, '', food_item)
                food_item.strip()
            food_list.append(food_item)

        print(food_list)

        regex = re.compile('\w+')
        complete_food_list = []

        for food_ in food_list:
            complete_food_list.append(regex.findall(food_))
        print(complete_food_list)"""

        file = open(path_food, 'w', encoding='euc-kr', newline='')
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
        print(compare_list)
        namtochrome.backup_csv_remove_overlap(self, compare_list)