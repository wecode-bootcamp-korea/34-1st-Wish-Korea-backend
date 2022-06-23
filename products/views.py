import json

from django.http  import JsonResponse
from django.views import View

from products.models import Category, SubCategory, Product, Size

class NavigatorView(View):
    def get(self, request):
        categories     = Category.objects.all()
        sub_categories = SubCategory.objects.all()
        result  = []
        result2 = []

        for category in categories:
            result2 = []
            for sub_category in sub_categories.filter(category_id = category.id):
                result2.append({
                    'id'   : sub_category.name,
                    'name' : sub_category.name
                })
            result.append(
                {'category'    : category.id,
                'name'         : category.name,
                'sub_category' : result2
                }
            )

        return JsonResponse({'result' : result}, status = 200)

class ListView(View):
    def get(requst, id):
        sub_category_id = requst.GET['category_id']
        sub_category = SubCategory.objects.get(id = sub_category_id)
        all_category = sub_category.category.subcategory_set.all()
        return {'sub_category_name': sub_category.name,
         'content' : sub_category.content,
         'image_url' : sub_category.image_url,
         'products' : [
            {'name' : lambda x : product.name + Size.objects.get(id = product.item_set.size_id).size_g for i in  products

            }for product in products
         ]
        }
        