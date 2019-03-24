"""gulishop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from rest_framework.authtoken import views
import xadmin
from django.views.static import serve
from gulishop.settings import MEDIA_ROOT
from goods.views import GoodsViewSet,CategoryViewSet
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from users.views import VerifyCodeViewSet,UserViewSet
from operations.views import UserFavViewSet,UserLeavingMessageViewSet,UserAddressViewSet
from trade.views import ShoppingCartViewSet,OrderInfoViewSet
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r'goods',GoodsViewSet,base_name='goods')
router.register(r'categorys',CategoryViewSet,base_name='categorys')
router.register(r'code',VerifyCodeViewSet,base_name='code')
router.register(r'users',UserViewSet,base_name='users')
router.register(r'userfavs',UserFavViewSet,base_name='userfavs')
router.register(r'messages',UserLeavingMessageViewSet,base_name='messages')
router.register(r'address',UserAddressViewSet,base_name='address')
router.register(r'shopcarts',ShoppingCartViewSet,base_name='shopcarts')
router.register(r'orders',OrderInfoViewSet,base_name='orders')

from trade.views import AliPayView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)',serve,{'document_root':MEDIA_ROOT}),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'',include(router.urls)),
    #是token认证的登陆方式
    # url(r'^login/', views.obtain_auth_token),
    #JWTtoken认证的登陆方式
    url(r'^login/', obtain_jwt_token),
    url(r'^alipay_return/$',AliPayView.as_view(),name='alipay'),
    url(r'^index/',TemplateView.as_view(template_name='index.html'),name='index')

]
