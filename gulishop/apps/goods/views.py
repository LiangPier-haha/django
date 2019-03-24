from .models import Goods,GoodsCategory
from .serializers import GoodsSerializer,CategorySerializer
from rest_framework import generics,mixins,pagination,filters,viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter


class GoodsPagination(pagination.PageNumberPagination):
    page_size = 12
    # max_page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'page_size'


class GoodsViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # 配置过滤器
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    # filter_fields = ('name',)
    filter_class = GoodsFilter
    search_fields = ('name','desc','goods_brief')
    ordering_fields = ('shop_price','sold_num')

    #此时，我们可以不需要写get方法，因为我们把get方法放在路由当中去做绑定


class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

    # def get_queryset(self):
    #     return GoodsCategory.objects.filter(category_type=1)