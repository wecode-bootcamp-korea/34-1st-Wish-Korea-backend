import json

from django.http  import JsonResponse
from django.views import View

from products.models import Category, SubCategory

class CategoryView(View):
    def get(self, request):
        categories     = Category.objects.all()
        result = [
            {
                'category_id'    : category.id, 
                'name'           : category.name,
                'products_count' : category.prefetch_related('product'),
                'sub_cateogry'   : [
                    {
                        'id'             : sub_category.id,
                        'name'           : sub_category.name,
                        'products_count' : sub_category.product_set.all().count() 
                    } for sub_category in category.subcategory_set.all()
                ] 
            } for category in categories
        ]

        return JsonResponse({'result' : result}, status = 200)

class ListView(View):
    def get(self, requst):
        try:
            sub_category_id = requst.GET['category_id']
            sub_categories  = SubCategory.objects.all()
            sub_category    = sub_categories.get(id = sub_category_id)
            products        = sub_category.product_set.all()
            
            result = {
                'sub_cateogry_id' : sub_category.id,
                'content'         : sub_category.content,
                'image_url'       : sub_category.image_url, 
                'products' : [
                    {
                        'id'               : product.id,
                        'name'             : product.name,
                        'tag'              : product.tag,
                        'is_new'           : product.is_new,
                        'is_vegan'         : product.is_vegan,
                        'is_only_online'   : product.is_only_online,
                        'is_made_in_korea' : product.is_made_in_korea,
                        'is_sold_out'      : bool(not sum([item.stock for item in product.item_set.all()])),
                        'price'            : int(product.item_set.order_by('price')[0].price), 
                        'image_url'        : [image.url for image in product.imgaeurl_set.all()]
                    } for product in products],
                }    

            return JsonResponse({'result' : result}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)

        except SubCategory.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Category'}, status = 400)
    