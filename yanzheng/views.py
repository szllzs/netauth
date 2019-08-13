


from django.views.generic import View
from .form import RegisterForm,LoginForm,RechangForm,ResetPwdForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UserProfile,Cards#,bg
import re
import time
import datetime
import hashlib
from netauth.settings import SECRET_KEY

from apps.utils.mixin_utils import LoginRequiredMinxin

class RegisterView(View):
    """注册"""
    def post(self,request):
        reg_form=RegisterForm(request.POST)
        if reg_form.is_valid():
            uid=request.POST.get('uid','')
            pwd=request.POST.get('pwd','')
            u=UserProfile()
            u.username=uid
            u.password=pwd
            u.save()
            msg="注册成功！"
        else:
            msg=str(reg_form.errors)

        if re.findall("注册成功！",msg):
            return HttpResponse(0)
        elif re.findall("此用户名已经被占用",msg):
            return HttpResponse(1)
        elif re.findall("用户名不能为空",msg):
            return HttpResponse(2)
        elif re.findall("用户名过长",msg):
            return HttpResponse(3)
        elif re.findall("密码不能为空",msg):
            return HttpResponse(4)
        elif re.findall("密码过长",msg):
            return HttpResponse(5)
        else:
            return HttpResponse(6)

class LoginView(View):
    """登录"""
    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            uid=request.POST.get('uid','')
            pwd=request.POST.get('pwd','')
            u=UserProfile.objects.filter(username=uid).first()
            if u.password==pwd:
                if not u.is_ban:
                    u_endtime_stamp=int(time.mktime(u.end_time.timetuple()))
                    nowtime_stamp=int(time.time())
                    if u_endtime_stamp>nowtime_stamp:
                        u.end_time=u.end_time.strftime('%Y-%m-%d %H:%M:%S')
                        msg="登录成功，到期时间："+u.end_time
                    else:
                        msg="该账户已无剩余时间，请充值！"
                else:
                    msg='此账户已经被冻结'
            else:
                msg='密码错误'
        else:
            msg=str(login_form.errors)

        if re.findall("登录成功",msg):
            return HttpResponse(msg)

        elif re.findall("请充值",msg):
            return HttpResponse(11)

        elif re.findall("此账户已经被冻结",msg):
            return HttpResponse(12)

        elif re.findall("密码错误",msg):
            return HttpResponse(13)

        elif re.findall("用户名不能为空",msg):
            return HttpResponse(14)

        elif re.findall("密码不能为空",msg):
            return HttpResponse(15)

        else:
            return HttpResponse(16)

class PingView(View):
    """心跳包"""
    def post(self,request):
        uid = request.POST.get('uid', '')
        pwd = request.POST.get('pwd', '')
        u = UserProfile.objects.filter(username=uid).first()
        u_endtime_stamp = int(time.mktime(u.end_time.timetuple()))
        nowtime_stamp = int(time.time())
        if u_endtime_stamp > nowtime_stamp:
            msg='0'
        else:
            msg ='1'
        return HttpResponse(msg)



#......

class CardView(LoginRequiredMinxin,View):
    """生成卡密"""
    def get(self,request):
        key=request.user.password
        # bgt=bg.objects.all().first()
        # return render(request,'index.html',{'bgt':bgt,'key':key})
        return render(request,'index.html',{'key':key})

    def post(self,request):
        key=request.POST.get('key','')
        if key==request.user.password:
            nums = request.POST.get('nums', '')
            if nums.isdigit():
                n=abs(int(nums))
                u=request.POST.get('unit','')
                for i in range(n):
                    j = str(int(time.time()))
                    k = str(i)
                    l = j + k + SECRET_KEY
                    i = hashlib.sha256()
                    i.update(l.encode('utf8'))
                    card=Cards()
                    card.kacode=i.hexdigest()
                    card.user_id = request.user.id
                    if u=='0':
                        card.time=3600
                    elif u=='1':
                        card.time = 3600*24
                    elif u=='2':
                        card.time = 3600*24*7
                    elif u=='3':
                        card.time = 3600*24*31
                    elif u=='4':
                        card.time = 3600*24*31*3
                    elif u=='5':
                        card.time = 3600*24*31*6
                    elif u=='6':
                        card.time = 3600*24*31*12
                    card.save()
                return redirect('/xadmin/yanzheng/cards/')
            else:
                msg='生产张数必须是整数'
        else:
            msg='验证失败'
        return render(request,'index.html',{'msg':msg})

class RechargeView(View):
    """充值"""

    def post(self, request):
        rechange_form = RechangForm(request.POST)
        if rechange_form.is_valid():
            code = request.POST.get('code', '')
            card = Cards.objects.filter(kacode=code).last()
            if not card.is_used:
                t = card.time
                uid = request.POST.get('uid', '')
                u = UserProfile.objects.filter(username=uid).first()
                u_endtime_stamp = int(time.mktime(u.end_time.timetuple()))
                nowtime_stamp = int(time.time())
                # 如果此账户本来的到期时间还没到，在他的到期时间基础上加时间，否则在现在的基础上加时间
                if u_endtime_stamp > nowtime_stamp:
                    end_time = t + u_endtime_stamp
                    u.end_time = datetime.datetime.fromtimestamp(end_time)
                else:
                    end_time = t + nowtime_stamp
                    u.end_time = datetime.datetime.fromtimestamp(end_time)
                msg = u.end_time.strftime('%Y-%m-%d %H:%M:%S')
                card.is_used = True
                card.user = u
                card.save()
                u.save()
                msg = '充值成功！到期时间为：' + msg
            else:
                msg = '此充值卡已使用过了！'
        else:
            msg = str(rechange_form.errors)

        if re.findall("充值成功", msg):
            return HttpResponse(msg)
        elif re.findall("此充值卡已使用过了！", msg):
            return HttpResponse(21)
        elif re.findall("此用户名不存在", msg):
            return HttpResponse(22)
        elif re.findall("用户名不能为空", msg):
            return HttpResponse(23)
        elif re.findall("卡密不能为空", msg):
            return HttpResponse(24)
        else:
            return HttpResponse(25)

class ResetPwdView(View):
    """重置密码"""
    def post(self,request):
        resetpwd_form=ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            uid=request.POST.get('uid','')
            u=UserProfile.objects.filter(username=uid).first()
            if u.password==request.POST.get('pwd1',''):
                u.password=request.POST.get('pwd2','')
                u.save()
                msg='修改密码成功！'
            else:
                msg='旧密码错误'
        else:
            msg=str(resetpwd_form.errors)
        if re.findall("修改密码成功",msg):
            return HttpResponse(30)
        elif re.findall("旧密码错误",msg):
            return HttpResponse(31)
        elif re.findall("此用户名不存在",msg):
            return HttpResponse(32)
        elif re.findall("用户名不能为空",msg):
            return HttpResponse(33)
        elif re.findall("旧密码不能为空",msg):
            return HttpResponse(34)
        elif re.findall("新密码不能为空",msg):
            return HttpResponse(35)
        else:
            return HttpResponse(36)