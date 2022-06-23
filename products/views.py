import json
from unicodedata import category

from django.http  import JsonResponse
from django.views import View

from products.models import Category, SubCategory, Product, Size

class CategoryView(View):
    def get(self, request):
        categories     = Category.objects.all()
        result = [
            {
                'category_id'  : category.id, 
                'name'         : category.name,
                'sub_cateogry' : [
                    {
                        'id'   : sub_category.id,
                        'name' : sub_category.name
                    } for sub_category in category.subcategory_set.all()
                ] 
            } for category in categories
        ]

        return JsonResponse({'result' : result}, status = 200)

class ListView(View):
    def get(self, requst):
        try:
            sub_category_id = requst.GET['category_id']
            sub_categories = SubCategory.objects.all()
            sub_category = sub_categories.get(id = sub_category_id)
            products = Product.objects.filter(sub_category_id = sub_category_id)
            result = {
                'sub_cateogry_id' : sub_category.id,
                'sub_category_name'    : sub_category.name,
                'content'              : sub_category.content,
                'image_url'            : sub_category.image_url, 
                'sub_categories'       : [{
                    'id'    : i.id, 
                    'name' : i.name,
                    'product_count': i.product_set.all().count()} for i in Category.objects.get(id = sub_category.category_id).subcategory_set.all()],
                 'products' : [{'id' : product.id,
                                'tag' : product.tag,
                                'is_new' : product.is_new,
                                'is_vegan' : product.is_vegan,
                                'is_only_online' : product.is_only_online,
                                'is_made_in_korea' : product.is_made_in_korea,
                                'is_sold_out' : bool(not product.item_set.all()[0].stock),
                                'prince' : int(product.item_set.filter(product_id = product.id)[0].price), 
                                'image_url' : [i.url for i in product.imgaeurl_set.all()]
                                    } for product in products],
                }           
            for idx, product in enumerate(products):
                if len(product.item_set.all())==1:
                    result['products'][idx].setdefault('name',name)
                else:
                    size_names = [i.size.size_g for i in product.item_set.all()]
                    size_names.sort()
                    name = product.name
                    for i in size_names[:]:
                        name =  name + '/' + str(i) + 'g'
                    name = name.replace(f'{product.name}/', f'{product.name} ')
                    result['products'][idx].setdefault('name',name)

            return JsonResponse({'result' : result}, status = 200)
        
        except KeyError:
            return JsonResponse({'message':'Key Error'}, status = 400)

        except SubCategory.DoesNotExist:
            return JsonResponse({'message' : 'hey~~~'}, status = 400)
    