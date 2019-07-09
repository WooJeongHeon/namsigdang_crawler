# 이 파일은 파이썬언어로 제작해야하며 이제 카카오톡 API 에 응답을 해주는 핵심 부분입니다.
# 또한 이 파일을 응용하셔야 입맛대로 카카오톡 봇 수정이 가능합니다.

# https://github.com/plusfriend/auto_reply 를 보시면 카카오 API에서 어떻게 개발해야하는지 알려주고 있습니다.
# 먼저 Home Keyboard API 요청에 대답을 해줘야 합니다.


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


#  KAKAO API 에서 keyboard 부분을 보면 이용자가 최초로 채팅방에 들어올 때 호출 한다고 합니다
# 그러면 이 라인은 이용자가 들어와서 keyboard 부분을 호출하면 위에 설정한 urls.py 파일이 자동으로 views.py 에 이부분으로 넘겨줍니다
# 이 라인의 기능은 buttons 타입으로 버튼 2개를 생성합니다 즉 사용자가 처음으로 들어오면 버튼1,버튼2 이렇게 버튼2개가 생성됩니다.
def keyboard(request):
    
    return JsonResponse({
        'type':'buttons',
        'buttons':['kakao_chatbot_button', '버튼1','버튼2']
    })


# KAKAO API 에서 메세지 수신 및 자동 응답 API 부분을 보시면 아실수 있듯 keyboard 에서 누른 버튼의 응답을 설정하는 부분입니다
# 간단한 if 문이네요 버튼1이 눌리면 button1 내용을 설정하고 출력 + keyboard 값 전송
# keyboard 값을 전송하는 이유는 버튼을 누르면 26~28 라인만 있어도 출력은 됩니다만 출력되고 나서 버튼이 사라집니다 왜나하면 버튼을 뿌려주는 keyboard 값은 최초 1회만 주고 다시 안 주었기 때문입니다. 그래서 29~31 라인에서 keyboard 값을 값이 줌으로써 메세지 출력 + 버튼이 다시 생깁니다.
@csrf_exempt
def answer(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']
    
    if datacontent == '버튼1':
        button1 = "버튼1을 누르셨습니다."
        
        return JsonResponse({
                'message': {
                    'text': button1
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['버튼1','버튼2']
                }
 
            })
    
    elif datacontent == '버튼2':
        button2 = "버튼2을 누르셨습니다."
        
        return JsonResponse({
                'message': {
                    'text': button2
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['버튼1','버튼2']
                }
 
            })