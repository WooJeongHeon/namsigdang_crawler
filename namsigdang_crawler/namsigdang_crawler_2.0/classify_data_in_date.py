# -*- coding: utf-8 -*- 
import pickle
import os

path_all_menu_dat = './data/crawling_menu/all_menu.dat'


file_all_menu_dat_old = open(path_all_menu_dat, 'rb')
dic_all_menu = pickle.load(file_all_menu_dat_old)
file_all_menu_dat_old.close()



for y in sorted(dic_all_menu):
    # print("\"" + y + "\": \"" + dic_all_menu[y] + "\",")
    
    
    if y[0:2] == "eu":        
    
        path_classify = './data/crawling_menu/year_{}/month_{}/{}_menu.dat'.format(y[2:6], y[6:8], y[2:6] + "_" + y[6:8])
        print(path_classify)
        path_classify_dir = './data/crawling_menu/year_{}/month_{}'.format(y[2:6], y[6:8])

        print(path_classify_dir)



        if not os.path.isdir(path_classify_dir):
            print("no")

            os.mkdir(path_classify_dir)
            print("폴더 새로 생성")
        else:
            print("ok")


        if not os.path.exists(path_classify):
            blank_dic = {}
            f = open(path_classify, 'wb')
            pickle.dump(blank_dic, f)
            f.close()

            print(path_classify + "파일이 없어 새로 생성합니다.")



        file_classified_dic_old = open(path_classify, 'rb')
        classified_dic = pickle.load(file_classified_dic_old)
        file_classified_dic_old.close()



        classified_dic.update(dic_all_menu)


        file_classified_dic_new = open(path_classify, 'wb')
        pickle.dump(classified_dic, file_classified_dic_new)
        file_classified_dic_new.close()
        
        
    else:
        print("조건에 만족하지 않습니다.")
        print("y[0:2]: {}".format(y[0:2]))
        print("key값:{}".format(y))

    
    




