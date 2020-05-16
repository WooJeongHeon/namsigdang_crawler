"""namsigdang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# android_app 폴더의 views파일을 import 하겠다는 소리입니다 여기서 android_app 부분은 위에서 설정한 어플리케이션 폴더이름 입니다.
import android_app.views
import kakao_chatbot.views

# 이 부분부터 요청이 들어오면 어디로 보내줄지 설정하는 부분입니다
urlpatterns = [
#     'admin/' 경로로 요청이 들어오면 admin.site.urls 로 보낸다는 뜻입니다
    path('admin/', admin.site.urls),
# #     kakao API 에서 keyboard 요청이 오면 이것을 3번라인에서 import 해준 views파일의 keyboard부분으로 보내준다는 의미입니다.
#     path('keyboard',kakao_chatbot.views.keyboard),
# #      kakao API 에서 message 요청이 오면 이것을 3번라인에서 import 해준 views파일의 answer 부분으로 보내준다는 의미입니다.
#     path('message',kakao_chatbot.views.answer),
    
#     path('post',kakao_chatbot.views.InsertFunc),
#     path('init',kakao_chatbot.views.on_init),


    # path('data',android_app.views.print_json_data),
    path('eunpyeong/menu/', include('android_app.urls')), # 주소 뒤에 eu/menu/가 오면 android_app.urls로 가라
    
]
