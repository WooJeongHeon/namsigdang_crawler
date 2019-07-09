# 이 파일은 파이썬언어로 제작해야하며 이제 카카오톡 API 에 응답을 해주는 핵심 부분입니다.
# 또한 이 파일을 응용하셔야 입맛대로 카카오톡 봇 수정이 가능합니다.

# https://github.com/plusfriend/auto_reply 를 보시면 카카오 API에서 어떻게 개발해야하는지 알려주고 있습니다.
# 먼저 Home Keyboard API 요청에 대답을 해줘야 합니다.


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json


#  KAKAO API 에서 keyboard 부분을 보면 이용자가 최초로 채팅방에 들어올 때 호출 한다고 합니다
# 그러면 이 라인은 이용자가 들어와서 keyboard 부분을 호출하면 위에 설정한 urls.py 파일이 자동으로 views.py 에 이부분으로 넘겨줍니다
# 이 라인의 기능은 buttons 타입으로 버튼 2개를 생성합니다 즉 사용자가 처음으로 들어오면 버튼1,버튼2 이렇게 버튼2개가 생성됩니다.
def print_json_data(request):
    
    # return JsonResponse({
    #     'status':'ok',
    #     'buttons':['android app namsigdang', '버튼1','버튼2']
    # })
    
    response_data = {}
    response_data['status'] = 'ok'
    response_data['utf-8'] = '한글 성공!!'

    
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")