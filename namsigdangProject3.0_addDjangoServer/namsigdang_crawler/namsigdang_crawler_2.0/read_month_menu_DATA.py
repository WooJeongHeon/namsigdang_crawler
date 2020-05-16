# -*- coding: utf-8 -*- 
import pickle

# path_month_menu_dat = '/workspace/namsigdang/namsigdang/namsigdang_crawler/namsigdang_crawler_2.0/data/crawling_menu/all_menu.dat'
path_month_menu_dat = './data/crawling_menu/year_2019/month_06/2019_06_menu.dat'

dic_all_menu={}

file_all_menu_dat_old = open(path_month_menu_dat, 'rb')
dic_all_menu = pickle.load(file_all_menu_dat_old)
file_all_menu_dat_old.close()

print("{")

for y in sorted(dic_all_menu):
    print("\"" + y + "\": \"" + dic_all_menu[y] + "\",")

print("}")

