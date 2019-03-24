
from django_filters import rest_framework as filters
from .models import Goods
from django.db.models import Q

class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name='shop_price',lookup_expr='gte',label='最低价格')
    pricemax = filters.NumberFilter(field_name='shop_price',lookup_expr='lte',label='最高价格')
    # name = filters.CharFilter(field_name='name',lookup_expr='contains')
    top_category = filters.NumberFilter(method='get_top_category')

    def get_top_category(self,queryset,name,value):
        #因为我们的商品的类别存储的最低类别
        #而用户点击的时候，可以点击任意类别，我们要根据任意类别去过滤出这个类别的商品
        return queryset.filter(Q(category_id = value)|Q(category__parent_category_id = value)|Q(category__parent_category__parent_category_id = value))


    class Meta:
        model = Goods
        fields = ['pricemin','pricemax','is_hot']
