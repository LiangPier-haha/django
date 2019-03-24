#配置我们文件所在目录的搜寻环境
import os,sys
#第一步先拿到当前文件的路径
file_path = os.path.abspath(__file__)
#第二步 根据这个路径去拿到这个文件所在目录的路径
dir_path = os.path.dirname(file_path)
#第三步：讲这个目录的路径添加到我们的搜寻环境当中
sys.path.append(dir_path)
#第四步，动态设置我们的setting文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gulishop.settings")
#第五步，让设置好的环境初始化生效
import django
django.setup()


from goods.models import Goods,GoodsCategory,GoodsImage
from db_tools.data.product_data import row_data

for item in row_data:
    goods = Goods()
    goods.name = item['name']
    goods.goods_brief = item['desc'] if item['desc'] else ''
    goods.desc = item['goods_desc'] if item['goods_desc'] else ''
    goods.market_price = float(item['market_price'].replace('￥','').replace('元',''))
    goods.shop_price = float(item['sale_price'].replace('￥','').replace('元',''))
    goods.goods_front_image = item['images'][0] if item['images'] else ''

    #我们数据当中存储的是类别的名字。而不是类别的对象，如果我们要去给外键赋值，得找到这个类别的对象
    category_name = item['categorys'][-1]
    category_list = GoodsCategory.objects.filter(name=category_name)
    if category_list:
        goods.category = category_list[0]
    goods.save()

    for image in item['images']:
        goods_image = GoodsImage()
        goods_image.goods = goods
        goods_image.image = image
        goods_image.save()




