from rest_framework import serializers
from .models import UserFav,UserLeavingMessage,UserAddress
from goods.serializers import GoodsSerializer


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = UserFav
        fields = '__all__'


class UserFavListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M:%S")
    #这里的goods是我们userfav表当中的一个外键字段，它对应了一个商品，所以序列化的时候，我们的many=False
    #而之间我们通过related_name的值，获取到的是所有的子表对象，然后去序列化，因此many=True
    goods = GoodsSerializer(many=False)
    class Meta:
        model = UserFav
        fields = '__all__'


class    UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserLeavingMessage
        fields = '__all__'


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserAddress
        fields = '__all__'