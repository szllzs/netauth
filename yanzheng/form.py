from django import forms
from .models import UserProfile


class RegisterForm(forms.Form):
    """注册信息的验证"""
    uid = forms.CharField(required=True,
                          max_length=150,
                          error_messages={
                              'required': '用户名不能为空.',
                              'max_length':'用户名过长！'})

    pwd = forms.CharField(required=True,
                          max_length=128,
                          error_messages={
                              'required': '密码不能为空.',
                              'max_length': "密码过长！"})

    def clean(self):
        """查看用户名是否已经被占用"""

        uid=self.cleaned_data.get('uid','')
        u=UserProfile.objects.filter(username=uid)
        if u:
            raise forms.ValidationError('此用户名已经被占用')
        else:
            return self.cleaned_data

    class LoginForm(forms.Form):
        """登录"""
        uid = forms.CharField(required=True, error_messages={'required': '用户名不能为空.', })
        pwd = forms.CharField(required=True, error_messages={'required': '密码不能为空.', })

class LoginForm(forms.Form):
    """登录"""
    uid = forms.CharField(required=True,error_messages={'required': '用户名不能为空.',})
    pwd = forms.CharField(required=True,error_messages={'required': '密码不能为空.',})



class RechangForm(forms.Form):
    """充值验证"""
    uid = forms.CharField(required=True, error_messages={'required': '用户名不能为空.', })
    code=forms.CharField(required=True, error_messages={'required': '卡密不能为空.', })

    def clean(self):
        """查看用户名是否存在"""

        uid=self.cleaned_data.get('uid','')
        u=UserProfile.objects.filter(username=uid)
        if u:
            return self.cleaned_data
        else:
            raise forms.ValidationError('此用户名不存在')

class ResetPwdForm(forms.Form):
    """重置密码验证"""
    uid = forms.CharField(required=True, error_messages={'required': '用户名不能为空.', })
    pwd1 = forms.CharField(required=True, error_messages={'required': '旧密码不能为空.', })
    pwd2 = forms.CharField(required=True, error_messages={'required': '新密码不能为空.', })
    def clean(self):
        """查看用户名是否存在"""

        uid=self.cleaned_data.get('uid','')
        u=UserProfile.objects.filter(username=uid)
        if u:
            return self.cleaned_data
        else:
            raise forms.ValidationError('此用户名不存在')


