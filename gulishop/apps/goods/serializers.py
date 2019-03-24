from rest_framework import serializers
from .models import Goods,GoodsCategory,GoodsImage


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=30,min_length=3)
#     goods_front_image = serializers.ImageField(required=True)
#     shop_price = serializers.FloatField(required=True)
#     add_time = serializers.DateTimeField(required=True)

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        #可以部分序列化
        # fields = ['name','add_time']
        #可以全部序列化
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        #可以部分序列化
        # fields = ['name','add_time']
        #可以全部序列化
        fields = '__all__'




class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    #嵌套的序列化，这里必须是related_name的值，才能拿到子表对象进行序列化，否则行不通
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'