from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import pickle


def all_menu(request):
    path_all_menu_dat = '../namsigdang_crawler/data/crawling_menu/all_menu.dat'

    file_all_menu_dat = open(path_all_menu_dat, 'rb')
    dic_all_menu = pickle.load(file_all_menu_dat)
    file_all_menu_dat.close()

    test_dic = {}
    test_dic['status'] = 'ok'
    test_dic['utf-8'] = '한글지원'
    test_dic['size'] = len(dic_all_menu) + len(test_dic)

    dic_all_menu.update(test_dic)
    response_data = dic_all_menu

    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")


def classify_menu(request, year, month):
    if month < 10:
        month = "0" + str(month)

    test_dic = {}
    test_dic['status'] = 'ok'
    test_dic['utf-8'] = '한글지원'
    test_dic['year'] = year
    test_dic['month'] = month
    test_dic['size'] = None

    path_menu_dat = '../namsigdang_crawler/data/crawling_menu/year_{y}/month_{m}/{y}_{m}_menu.dat'.format(y=year,
                                                                                                          m=month)

    file_menu_dat = open(path_menu_dat, 'rb')
    dic_menu = pickle.load(file_menu_dat)
    file_menu_dat.close()

    test_dic['size'] = len(dic_menu) + len(test_dic)

    dic_menu.update(test_dic)
    response_data = dic_menu

    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
