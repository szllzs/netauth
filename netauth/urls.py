"""netauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.views.static import serve
from netauth.settings import MEDIA_ROOT
from yanzheng.views import RegisterView
import xadmin
from yanzheng.views import RegisterView,LoginView
from yanzheng.views import RegisterView,LoginView,PingView
from yanzheng.views import RegisterView,LoginView,PingView,CardView,RechargeView,ResetPwdView

urlpatterns = [
    path('admin/', admin.site.urls),
    #配置上传文件的访问处理函数
    path('xadmin/', xadmin.site.urls),
    path('register',RegisterView.as_view()),
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    path('login',LoginView.as_view()),
    path('ping',PingView.as_view()),
    path('card',CardView.as_view(),name='card'),
    path('recharge', RechargeView.as_view()),
    path('resetpwd', ResetPwdView.as_view()),
]