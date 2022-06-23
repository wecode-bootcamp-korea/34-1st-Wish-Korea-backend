import json
from unicodedata import category

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
    def get(requst):
        try:
            sub_category_id = requst.GET['category_id']
            sub_categories = SubCategory.objects.all()
            sub_category = sub_categories.get(id = sub_category_id)
            products = Product.objects.filter(sub_category_id = sub_category_id)
            sizes = Size.objects.all()
            result = []
            for product in products:
                {'sub_cateogry_id'   : sub_category.id,
                 'sub_category_name' : sub_category.name,
                 'content'           : sub_category.content,
                 'image_url'         : sub_category.url, 
                 'sub_categories'    : [{'id'    : i.id, 
                                        'name' : i.name} for i in sub_category.all()],
                 'products' : [ for product in products size_names =  if len(product.item_set.all() else)] 
                }           
            for product in products:
                if len(product.item_set.all())==1:
                    {'name' : product.name}
                else:
                    size_names = [i.size.id for i in product.item_set.all()]
                    name = f'{product.name} '
                    for i in size_names[1:]:
                        name =  '/' + name + 'g'
                    {'name' : name}

            
        
        except KeyError:
            return JsonResponse({'message':'Key Error'}, status = 400)

        except SubCategory.DoesNotExist({'message' : 'hey~~~'})