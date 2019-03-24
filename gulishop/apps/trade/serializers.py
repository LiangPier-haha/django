from rest_framework import serializers
from .models import ShopCart,OrderInfo,OrderGoods
from goods.serializers import GoodsSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ShopCart
        fields = '__all__'


class ShoppingCartListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShopCart
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)


    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")


    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'