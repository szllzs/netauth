from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class UserProfile(AbstractUser):
    is_ban=models.BooleanField(default=False,verbose_name='是否被禁')
    end_time=models.DateTimeField(default=datetime.now, verbose_name='到期时间')

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.username


class Cards(models.Model):

    """充值卡"""
    user=models.ForeignKey(UserProfile,verbose_name='使用者',on_delete=models.CASCADE)
    kacode=models.CharField(max_length=50,verbose_name='卡密',default='')
    time=models.IntegerField(default=3600,verbose_name='时长')
    is_used=models.BooleanField(default=False,verbose_name='是否已经使用')
    add_time=models.DateTimeField(default=datetime.now,verbose_name='生成时间')
    class Meta:
        verbose_name='卡密'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.kacode
