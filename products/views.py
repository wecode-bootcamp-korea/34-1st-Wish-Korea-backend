import json

from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Count, Q, Sum, Case, When, F
from django.db.models.functions import Coalesce

from products.models import Category, SubCategory, Product
from orders.models   import Cart

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all().annotate(product_counts=Count("subcategory__product__id")).prefetch_related('subcategory_set')
        result = [
            {
                'category_id'    : category.id, 
                'name'           : category.name,
                'products_count' : category.product_counts,
                'content'        : category.content,
                'image_url'      : category.image_url,
                'sub_categories' : [
                    {
                        'id'             : sub_category.id,
                        'name'           : sub_category.name,
                        'content'        : sub_category.content,
                        'image_url'      : sub_category.image_url,
                        'products_count' : sub_category.product_set.all().count() 
                    } for sub_category in category.subcategory_set.all()
                ] 
            } for category in categories
        ]

        return JsonResponse({'result' : result}, status = 200)

class ProductListView(View):
    def get(self, request):
        try:
            category_id     = request.GET.get('category_id')
            sub_category_id = request.GET.get('sub_category_id')
            sort_key        = request.GET.get('sort_key')
            offset          = int(request.GET.get('offset', 0))
            limit           = int(request.GET.get('limite', 30))
            
            q = Q()

            if category_id:
                q &= Q(sub_category__category_id = category_id)
            
            if sub_category_id:
                q &= Q(sub_category_id = sub_category_id)

            sort_set = {
                'random' : '?',
                'hot'    : 'total'
            }
            
            products = Product.objects.filter(q).annotate(
                quantity_sum = Coalesce(Sum('item__cart__quantity'),0), 
                stock_sum    = Coalesce(Sum('item__stock'),0),
                total        = F('stock_sum') - F('quantity_sum'),
                is_sold_out  = Case(When(total__exact=0, then = True), default = False)
                ).order_by(sort_set.get(sort_key, 'hot'))[offset:offset + limit]
                
            result = {
                'products' : [
                    {   
                        'id'               : product.id,
                        'name'             : product.name,
                        'tag'              : product.tag,
                        'is_new'           : product.is_new,
                        'is_vegan'         : product.is_vegan,
                        'is_only_online'   : product.is_only_online,
                        'is_made_in_korea' : product.is_made_in_korea,
                        'is_sold_out'      : product.is_sold_out,
                        'price'            : [int(item.price) for item in product.item_set.order_by('price')],
                        'image_url'        : [image.url for image in product.imageurl_set.all()]
                } for product in products],
            }
                
            return JsonResponse({'result' : result}, status = 200) 

        except SubCategory.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Category'}, status = 400)
        
        except Category.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Category'}, status = 400)

class ProductView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)
            result = {
                'product_id' : product_id,
                'name'       : product.name,
                'tag'        : product.tag,
                'image'      : [image.url for image in product.imageurl_set.all()],
                'components' : [
                    {
                        'id'        : component.id,
                        'name'      : component.name,
                        'important' : component.productcomponent_set.get(product_id = product_id).important
                    } for component in product.component.all()
                ],
                'items' : [
                    {   
                        'id'     : item.id,
                        'size_g' : item.size.size_g,
                        'price'  : int(item.price),
                        'stock'  : item.stock - Cart.objects.filter(item_id = item.id).aggregate(stock = Coalesce(Sum('quantity'), 0))['stock'],
                        'image'  : item.image_url
                    }for item in product.item_set.order_by('size__size_g')
                ] 
            }
            
            return JsonResponse({'result' : result}, status = 200)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Product'}, status = 400)