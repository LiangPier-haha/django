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

#这一行，不能放在上面
from goods.models import GoodsCategory
from db_tools.data.category_data import row_data

for lev1 in row_data:
    cat1 = GoodsCategory()
    cat1.name = lev1['name']
    cat1.code = lev1['code'] if lev1['code'] else ''
    cat1.category_type = 1
    cat1.save()
    for lev2 in lev1['sub_categorys']:
        cat2 = GoodsCategory()
        cat2.name = lev2['name']
        cat2.code = lev2['code'] if lev2['code'] else ''
        cat2.category_type = 2
        cat2.parent_category = cat1
        cat2.save()
        for lev3 in lev2['sub_categorys']:
            cat3 = GoodsCategory()
            cat3.name = lev3['name']
            cat3.code = lev3['code'] if lev3['code'] else ''
            cat3.category_type = 3
            cat3.parent_category = cat2
            cat3.save()

