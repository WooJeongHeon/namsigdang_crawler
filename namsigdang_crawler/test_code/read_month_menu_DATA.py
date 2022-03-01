# -*- coding: utf-8 -*- 
import pickle

path_month_menu_dat = '../data/crawling_menu/year_2019/month_06/2019_06_menu.dat'


file_all_menu_dat_old = open(path_month_menu_dat, 'rb')
dic_all_menu = pickle.load(file_all_menu_dat_old)
file_all_menu_dat_old.close()

print(dic_all_menu)

# print("{")
# for y in sorted(dic_all_menu):
#     print("\"" + y + "\": \"" + dic_all_menu[y] + "\",")
# print("}")
