import json
from unicodedata import name

import jwt

from django.http  import JsonResponse
from django.views import View

from orders.models         import Cart
from core.token_dacorators import token_decorator

class CartView(View):
    @token_decorator
    def get(self, request):
        user   = request.user
        carts  = Cart.objects.filter(user = user)

        result = {
            'cart' : [
                {
                    'cart_id'    : cart.id,
                    'item_id'    : cart.item_id,
                    'product_size' : 
                    'name'       : cart.item.product.name,
                    'price'      : cart.item.price,
                    'stock'      : cart.item.stock,
                    'image_url'  : '', #cart.item.product.imageurl_set.get(),
                    'item_sizes' : [123,515,1000],
                    #'size'      : [size.size_g for size in cart.item.;size.order_by('size_g')],
                    'sub_catgory_name' : cart.item.product.sub_category.name}
            ]for cart in carts
            }
        
        return JsonResponse({'result' : result}, status = 200)