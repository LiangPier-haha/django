from django.shortcuts import render
from rest_framework import mixins,viewsets
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from .models import VerifyCode,UserProfile
from .serializers import VerifyCodeSerializer,UserSerializer,UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from random import choice
from utils.yunpian import YunPian
from gulishop.settings import YUNPIAN_KEY
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.


class VerifyCodeViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = VerifyCode.objects.all()
    serializer_class = VerifyCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        code = self.get_random_code()

        yunpian = YunPian(YUNPIAN_KEY)
        result = yunpian.send_msg(mobile,code)

        if result['code'] == 0:
            ver = VerifyCode()
            ver.mobile = mobile
            ver.code = code
            ver.save()
            return Response(data={'mobile':mobile,'msg':result['msg']},status=status.HTTP_201_CREATED)
        else:
            return Response(data={'mobile': mobile, 'msg': result['msg']}, status=status.HTTP_400_BAD_REQUEST)

    def get_random_code(self):
        str = '1234567890'
        code = ''
        for i in range(6):
            code += choice(str)
        return code


class UserViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    #我们的认证一般都不会配置在settings当中 进行全局配置，因为当用户token过期不过期我们都是允许用户查看某些资源的，所以
    #我们要在必须认证的资源上局部添加认证信息
    authentication_classes = (SessionAuthentication,JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            return []
        else:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        '''
        这个方法，可以让我们动态的配置序列化，只有用户在创建的时候，我们用创建的序列化UserSerializer，其余的操作全部使用UserDetailSerializer
        :return:
        '''
        if self.action == 'create':
            return UserSerializer
        else:
            return UserDetailSerializer

    def get_object(self):
        '''
        这个方法，是让我们在获取某个用户的时候，无论填什么样的id，拿到的永远是当前登陆的用户
        :return:
        '''
        return self.request.user


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = UserProfile()
        user.username = username
        user.mobile = username
        user.set_password(password)
        user.save()
        #如果你需要注册后直接就是登陆状态，那么你需要把token手动生成 返回给前端进行设置
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        ret = serializer.data
        ret['name'] = user.name if user.name else user.username
        ret['token'] = token

        headers = self.get_success_headers(serializer.data)
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)