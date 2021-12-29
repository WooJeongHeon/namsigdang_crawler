import pickle

path_all_menu_dat = './crawling_menu/all_menu.dat'

dic_all_menu = {"code": "success", "msg": "error none",

                "eu20180219a": "",
                "eu20180219b": "흑미밥,떡만두국,애호박전,참나물생채,김치,요플레",
                "eu20180219c": "차조밥,순두부찌개,돈육갈비찜,콩나물무침,김치",
                "eu20180220a": "북어채맑은국,어묵햄조림,진미채볶음,김치",
                "eu20180220b": "혼합잡곡밥,건새우아욱국,닭엿장조림,오이부추무침,김치,사과",
                "eu20180220c": "발아현미밥,감자호박찌개,갈치무조림,베이컨숙주볶음,김치",
                }

file_all_menu_dat_new = open(path_all_menu_dat, 'wb')
pickle.dump(dic_all_menu, file_all_menu_dat_new)
file_all_menu_dat_new.close()
