# 이 파일은 파이썬언어로 제작해야하며 이제 카카오톡 API 에 응답을 해주는 핵심 부분입니다.
# 또한 이 파일을 응용하셔야 입맛대로 카카오톡 봇 수정이 가능합니다.

# https://github.com/plusfriend/auto_reply 를 보시면 카카오 API에서 어떻게 개발해야하는지 알려주고 있습니다.
# 먼저 Home Keyboard API 요청에 대답을 해줘야 합니다.


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import pickle


#  KAKAO API 에서 keyboard 부분을 보면 이용자가 최초로 채팅방에 들어올 때 호출 한다고 합니다
# 그러면 이 라인은 이용자가 들어와서 keyboard 부분을 호출하면 위에 설정한 urls.py 파일이 자동으로 views.py 에 이부분으로 넘겨줍니다
# 이 라인의 기능은 buttons 타입으로 버튼 2개를 생성합니다 즉 사용자가 처음으로 들어오면 버튼1,버튼2 이렇게 버튼2개가 생성됩니다.
def all_menu(request):
    
    # return JsonResponse({
    #     'status':'ok',
    #     'buttons':['android app namsigdang', '버튼1','버튼2']
    # })
    
    path_all_menu_dat = './namsigdang_crawler/data/crawling_menu/all_menu.dat'

    
    file_all_menu_dat = open(path_all_menu_dat, 'rb')
    dic_all_menu = pickle.load(file_all_menu_dat)
    file_all_menu_dat.close()
    
    test_dic = {}
    test_dic['status'] = 'ok'
    test_dic['utf-8'] = '한글 성공!!'
    test_dic['갯수'] = None
    
    test_dic['갯수'] = len(dic_all_menu)+ len(test_dic)


    
    
    dic_all_menu.update(test_dic)

    
    response_data = dic_all_menu
    

    
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")



def classify_menu(request, year, month):
    # return JsonResponse({
    #     'status':'ok',
    #     'buttons':['android app namsigdang', '버튼1','버튼2']
    # })
    
    
    if month < 10:
        month = "0" + str(month)
    

    test_dic = {}
    test_dic['status'] = 'ok'
    test_dic['utf-8'] = '한글 성공!!'
    test_dic['년도'] = year
    test_dic['월'] = month
    test_dic['갯수'] = None

    
    
    
    path_menu_dat = './namsigdang_crawler/namsigdang_crawler_2.0/data/crawling_menu/year_{y}/month_{m}/{y}_{m}_menu.dat'.format(y = year, m = month)



    
    file_menu_dat = open(path_menu_dat, 'rb')
    dic_menu = pickle.load(file_menu_dat)
    file_menu_dat.close()
    
    test_dic['갯수'] = len(dic_menu)+ len(test_dic)

    
    dic_menu.update(test_dic)
    
    

    
    
    
    



    response_data = dic_menu
    

    
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")