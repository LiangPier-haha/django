import xadmin
from .models import *
from xadmin import views


class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True

class CommXadminSetting(object):
    site_title = '谷粒商城后台管理系统'
    site_footer = '尚硅谷教育出品'
    menu_style = 'accordion'


class GoodsCategoryAdmin(object):
    list_display = ['name','category_type','code','parent_category','is_tab','add_time']



class GoodsAdmin(object):
    list_display = ['category', 'name', 'goods_sn', 'goods_front_image', 'click_num', 'add_time']
    style_fields = {'desc':'ueditor'}



class CategoryBrandAdmin(object):
    list_display = ['category', 'image', 'name', 'add_time']




class GoodsImageAdmin(object):
    list_display = ['goods', 'image','add_time']



class BannerAdmin(object):
    list_display = ['goods', 'image','index', 'add_time']


class StudentInfoAdmin(object):
    list_display = ['name', 'age', 'add_time']



xadmin.site.register(GoodsCategory,GoodsCategoryAdmin)
xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(CategoryBrand,CategoryBrandAdmin)
xadmin.site.register(GoodsImage,GoodsImageAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(StudentInfo,StudentInfoAdmin)
xadmin.site.register(views.BaseAdminView,BaseXadminSetting)
xadmin.site.register(views.CommAdminView,CommXadminSetting)


