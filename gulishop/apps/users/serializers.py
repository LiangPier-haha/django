from rest_framework import serializers
from .models import VerifyCode,UserProfile
from gulishop.settings import MOBILE_RE
from datetime import datetime
import re
from rest_framework.validators import UniqueValidator

class VerifyCodeSerializer(serializers.ModelSerializer):

    def validate_mobile(self, mobile):
        #第一步：判断手机是不是合法
        com = re.compile(MOBILE_RE)
        if not com.match(mobile):
            raise serializers.ValidationError('手机号码不合法')
        #第二步：判断手机是不是注册过
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError('手机号码已经被注册')
        #第三步：判断手机是不是已经在规定时间内发送过短信
        ver_list = VerifyCode.objects.filter(mobile=mobile).order_by('-add_time')
        if ver_list:
            ver = ver_list[0]
            if (datetime.now() - ver.add_time).seconds <= 60:
                raise serializers.ValidationError('验证码已经发送，请1分钟后再次发送')
            else:
                ver.delete()
        return mobile


    class Meta:
        model = VerifyCode
        fields = ['mobile']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,max_length=30,min_length=11,validators=[UniqueValidator(queryset=UserProfile.objects.all())])
    password = serializers.CharField(required=True,max_length=20,min_length=6,write_only=True,style={'input_type': 'password'})
    code = serializers.CharField(required=True,max_length=6,min_length=6,write_only=True)

    def validate_code(self, code):
        #它是我们输入的用户名进来验证之前的数据存在 initial_data当中
        mobile = self.initial_data['username']
        ver_list = VerifyCode.objects.filter(mobile=mobile,code=code).order_by('-add_time')
        if ver_list:
            last_ver = ver_list[0]
            if(datetime.now() - last_ver.add_time).seconds > 1800:
                raise serializers.ValidationError('验证码已经够过期，重新发送')
        else:
            raise serializers.ValidationError('手机或者验证码出错')

    class Meta:
        model = UserProfile
        fields = ['username','password','code']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name','birthday','gender','email','mobile']