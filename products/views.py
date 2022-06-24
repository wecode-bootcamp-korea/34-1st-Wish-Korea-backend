import json

from django.http  import JsonResponse
from django.views import View

from products.models       import Product

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
    def get(self, request, product_id):
        try:
            product    = Product.objects.get(id = product_id)

            result = {
                'product_id' : product_id,
                'name'       : product.name,
                'tag'        : product.tag,
                'image'      : [url for url in product.imgaeurl_set.all()],
                'manual'     : product.manual,
                'content'    : product.content,
                'components' : [
                    {
                        'id'        : component.id,
                        'name'      : component.name,
                        'important' : component.productcomponent_set.get(product_id = product_id).important
                    } for component in product.component.all()
                ],
                'products'             : [
                    {
                        'id'     : item.id,
                        'size_g' : item.size.size_g,
                        'price'  : int(item.price),
                        'stock'  : item.stock,
                        'image'  : item.image_url
                    }for item in product.item_set.all()
                ] 
            }
            
            return JsonResponse({'result' : result}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Product'}, status = 400)