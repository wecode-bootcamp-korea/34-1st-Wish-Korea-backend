import json
from unicodedata import category

from django.http  import JsonResponse
from django.views import View

from products.models import Category, SubCategory, Product

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        result = [
            {
                'category_id'    : category.id, 
                'name'           : category.name,
                'products_count' : category.subcategory_set.filter(
                    product__sub_category__in = category.subcategory_set.all()).count(),
                'sub_categories' : [
                    {
                        'id'             : sub_category.id,
                        'name'           : sub_category.name,
                        'products_count' : sub_category.product_set.all().count() 
                    } for sub_category in category.subcategory_set.all()
                ] 
            } for category in categories
        ]

        return JsonResponse({'result' : result}, status = 200)

class ProductListView(View):
    def get(self, request):
        try:
            if request.GET.get('category_id'):
                category_id = request.GET['category_id']
                category    = Category.objects.get(id = category_id)
                products    = Product.objects.filter(sub_category__category_id = category_id)
                
                if category_id:
                    q =
                    category = Category.objects.get(id=category_id)

                if sub_category:
                    q = 
                    category = SubCategory.objects.get(id=sub_category_id) 
                
                category_information = {
                    'id'        : category.id,
                    'content'   : category.content,
                    'image_url' : category.image_url,
                }
                
                result      = { 
                    'products'    : [
                        {
                            'id'               : product.id,
                            'name'             : product.name,
                            'tag'              : product.tag,
                            'is_new'           : product.is_new,
                            'is_vegan'         : product.is_vegan,
                            'is_only_online'   : product.is_only_online,
                            'is_made_in_korea' : product.is_made_in_korea,
                            'is_sold_out'      : not product.item_set.exclude(stock__exact = 0).exists(),
                            'price'            : int(product.item_set.order_by('price')[0].price), 
                            'image_url'        : [image.url for image in product.imgaeurl_set.all()]
                        } for product in products],
                    }
                result['category'] = category_information
                
                return JsonResponse({'result' : result}, status = 200) 
            
            sub_category_id = request.GET['sub_category_id']
            sub_category    = SubCategory.objects.get(id = sub_category_id)
            products        = sub_category.product_set.all()
            
            result = {
                'sub_cateogry_id' : sub_category.id,
                'content'         : sub_category.content,
                'image_url'       : sub_category.image_url, 
                'products'        : [
                    {
                        'id'               : product.id,
                        'name'             : product.name,
                        'tag'              : product.tag,
                        'is_new'           : product.is_new,
                        'is_vegan'         : product.is_vegan,
                        'is_only_online'   : product.is_only_online,
                        'is_made_in_korea' : product.is_made_in_korea,
                        'is_sold_out'      : not product.item_set.exclude(stock__exact = 0).exists(),
                        'price'            : int(product.item_set.order_by('price')[0].price), 
                        'image_url'        : [image.url for image in product.imgaeurl_set.all()]
                    } for product in products],
                }    

            return JsonResponse({'result' : result}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)

        except SubCategory.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Category'}, status = 400)