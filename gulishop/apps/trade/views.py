from django.shortcuts import render
from rest_framework import mixins,viewsets
from .models import ShopCart,OrderInfo,OrderGoods
from .serializers import ShoppingCartSerializer,ShoppingCartListSerializer,OrderInfoSerializer,OrderInfoDetailSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
import time,random
from utils.alipay import AliPay
from gulishop.settings import ali_key,private_key,app_id
from rest_framework.views import APIView
from datetime import datetime

# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    # serializer_class = ShoppingCartSerializer
    authentication_classes = (SessionAuthentication,JSONWebTokenAuthentication)
    permission_classes = (IsOwnerOrReadOnly,IsAuthenticated)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShopCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartListSerializer
        else:
            return ShoppingCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        goods = serializer.validated_data['goods']
        nums = serializer.validated_data['nums']

        cart_list = ShopCart.objects.filter(user=self.request.user,goods=goods)
        if cart_list:
            cart = cart_list[0]
            cart.nums += nums
            cart.save()
        else:
            cart = ShopCart()
            cart.user = self.request.user
            cart.goods = goods
            cart.nums = nums
            cart.save()
        # serializer = self.get_serializer_class()(cart)
        serializer = self.get_serializer(cart)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderInfoViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    # serializer_class = OrderInfoSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoDetailSerializer
        else:
            return OrderInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://47.104.111.107:8000/alipay_return/",
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.104.111.107:8000/alipay_return/"
        )
        url = alipay.direct_pay(
            subject=instance.order_sn,
            out_trade_no=instance.order_sn,
            total_amount=instance.order_mount
        )
        # 沙箱环境
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        serializer = self.get_serializer(instance)
        ret = serializer.data
        ret['alipay_url'] = re_url
        return Response(ret)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #第一步：创建好订单
        order_sn = self.get_order_sn()
        order = OrderInfo.objects.create(**serializer.validated_data)
        order.order_sn = order_sn
        order.save()

        #第二步：创建好订单的订单商品并且与订单进行关联
        cart_list = ShopCart.objects.filter(user=self.request.user)
        for cart in cart_list:
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = cart.goods
            order_goods.goods_num = cart.nums
            order_goods.save()

        #第三步：清空购物车
        cart_list.delete()

        #第四步：生成订单支付链接，加入我们的返回数据当中，为了让前端可以去请求这个支付页面
        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://47.104.111.107:8000/alipay_return/",
            app_private_key_path = private_key,
            alipay_public_key_path= ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.104.111.107:8000/alipay_return/"
        )
        url = alipay.direct_pay(
            subject=order.order_sn,
            out_trade_no=order.order_sn,
            total_amount=order.order_mount
        )
        # 沙箱环境
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)


        headers = self.get_success_headers(serializer.data)
        # serializer = self.get_serializer_class()(order)
        serializer = self.get_serializer(order)
        ret = serializer.data
        ret['alipay_url'] = re_url
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)


    def get_order_sn(self):
        order_sn = '{strtime}{userid}{randomnum}'.format(strtime=time.strftime('%Y%m%d%H%M%S'),userid=str(self.request.user.id),randomnum=str(random.randint(10,99)))
        return order_sn


class AliPayView(APIView):
    def get(self,request):
        data_dict = {}
        for k, v in request.GET.items():
            data_dict[k] = v
        print(data_dict)
        sign = data_dict.pop('sign')
        print(sign)

        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://47.104.111.107:8000/alipay_return/",
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.104.111.107:8000/alipay_return/"
        )
        result = alipay.verify(data_dict, sign)
        if result:
            order_sn = data_dict.get('out_trade_no', '')
            trade_no = data_dict.get('trade_no', '')
            pay_time = datetime.now()
            pay_status = data_dict.get('trade_status', 'TRADE_SUCCESS')

            order_list = OrderInfo.objects.filter(order_sn=order_sn)
            if order_list:
                order = order_list[0]
                order.pay_status = pay_status
                order.pay_time = pay_time
                order.trade_no = trade_no
                order.save()
                from django.shortcuts import redirect,reverse
                ret = redirect(reverse('index'))
                ret.set_cookie('nextPath','pay',2)
                return ret

    def post(self,request):
        data_dict = {}
        for k,v in request.POST.items():
            data_dict[k] = v
        sign = data_dict.pop('sign',None)

        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://47.104.111.107:8000/alipay_return/",
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.104.111.107:8000/alipay_return/"
        )
        result = alipay.verify(data_dict,sign)
        if result:
            order_sn = data_dict.get('out_trade_no','')
            trade_no = data_dict.get('trade_no','')
            pay_time = datetime.now()
            pay_status = data_dict.get('trade_status','TRADE_SUCCESS')

            order_list = OrderInfo.objects.filter(order_sn = order_sn)
            if order_list:
                order = order_list[0]
                order.pay_status = pay_status
                order.pay_time = pay_time
                order.trade_no = trade_no
                order.save()
                return Response('success')



