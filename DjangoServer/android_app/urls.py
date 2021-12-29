"""my_site_prj URL Configuration
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:year>/<int:month>/', views.classify_menu),  # <int:year>/: 정수값을 입력받고 입력받은 값을 year라고 함

    path('all', views.all_menu),
    path('', views.all_menu),  # 파라미터가 없으면 views.all_menu에서 처리

]
