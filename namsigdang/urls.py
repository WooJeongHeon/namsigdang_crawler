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
import android_app.views
import kakao_chatbot.views

urlpatterns = [
    path('admin/', admin.site.urls),  # 'admin/' 경로로 요청이 들어오면 admin.site.urls에서 처리
    path('eunpyeong/menu/', include('android_app.urls')),  # 'eu/menu/' 파라미터가 오면 android_app.urls 에서 처리

    # #     kakao API 에서 keyboard 요청이 오면 이것을 3번라인에서 import 해준 views파일의 keyboard부분으로 보내준다는 의미입니다.
    #     path('keyboard',kakao_chatbot.views.keyboard),
    # #      kakao API 에서 message 요청이 오면 이것을 3번라인에서 import 해준 views파일의 answer 부분으로 보내준다는 의미입니다.
    #     path('message',kakao_chatbot.views.answer),

    #     path('post',kakao_chatbot.views.InsertFunc),
    #     path('init',kakao_chatbot.views.on_init),

    # path('data',android_app.views.print_json_data),
]
