import json
from unittest import result

from django.http  import JsonResponse
from django.views import View

from products.models       import Product
from core.token_validators import token_validator

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

class ProductView(View):
    @token_validator
    def get(self, request):
        try:
            product_id = request.GET['product_id']
            product    = Product.objects.get(id = product_id)

            result = {
                'is_user'    : bool(request.user),
                'product_id' : product_id,
                'name'       : None,
                'tag'        : product.tag,
                'image'      : [url for url in product.imgaeurl_set.all()],
                'menual'     : product.manual,
                'content'    : product.content,
                'products'   : [
                    {
                        'size_g' : item.size.size_g,
                        'price'  : item.price,
                        'stock'  : item.stock,
                        'image'  : item.image_url
                    }for item in product.item_set.all()
                ] 
            }

            if len(product.item_set.all()) == 1:
                result['products'][idx].setdefault('name', name)
            else:
                size_values = [size_value.size.size_g for size_value in product.item_set.all()]
                name       = product.name
                size_values.sort()
                for i in size_values:
                    name += '/' + str(i) + 'g'
                name = name.replace(f'{product.name}/', f'{product.name} ')
                result['products'][idx].setdefault('name', name)
        
            
            
            return JsonResponse({'result' : result}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'Invalid Product'}, status = 400)