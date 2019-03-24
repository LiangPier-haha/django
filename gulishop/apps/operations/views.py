from django.shortcuts import render
from rest_framework import mixins,viewsets
from .models import UserFav,UserLeavingMessage,UserAddress
from .serializers import UserFavSerializer,UserFavListSerializer,UserLeavingMessageSerializer,UserAddressSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.

class UserFavViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    lookup_field = 'goods_id'
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        '''
        这个方法，可以让我们动态的配置序列化，只有用户在创建的时候，我们用创建的序列化UserSerializer，其余的操作全部使用UserDetailSerializer
        :return:
        '''
        if self.action == 'list':
            return UserFavListSerializer
        else:
            return UserFavSerializer


class UserLeavingMessageViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserLeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
