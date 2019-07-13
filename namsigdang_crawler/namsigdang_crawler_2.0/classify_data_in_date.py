# -*- coding: utf-8 -*- 
import pickle
import os

path_all_menu_dat = './data/crawling_menu/all_menu.dat'


file_all_menu_dat_old = open(path_all_menu_dat, 'rb')
dic_all_menu = pickle.load(file_all_menu_dat_old)
file_all_menu_dat_old.close()



for y in sorted(dic_all_menu):
    # print("\"" + y + "\": \"" + dic_all_menu[y] + "\",")
    
    path_classify = './data/crawling_menu/year_{}/month_{}/{}_menu.dat'.format(y[2:6], y[6:8], y[2:6] + "_" + y[6:8])
    print(path_classify)
    path_classify_dir = './data/crawling_menu/year_{}/month_{}'.format(y[2:6], y[6:8])
    
    print(path_classify_dir)

    
    
    if not os.path.isdir(path_classify_dir):
        os.mkdir(path_classify_dir)
        print("폴더 새로 생성")

        
    if not os.path.exists(path_classify):
        logfile = open(path_classify, 'w')
        logfile.close()
        print(path_classify + "파일이 없어 새로 생성합니다.")
    
    
    
    # file_classified_dic = open(path_classify, 'rb')
    # classified_dic = pickle.load(file_classified_dic)
    # file_classified_dic.close()


    # classified_dic.update(dic_all_menu)
    
    
    




