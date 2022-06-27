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
                    'cart_id'   : cart.id,
                    'item_id'   : cart.item_id,
                    'name'      : cart.item.product.name,
                    'price'     : cart.item.price,
                    'stock'     : cart.item.stock,
                    'image_url' : cart.item.product.image_url,
                    'size'      : [size.size_g for size in cart.item.size_set],
                    'sub_catgory_name' : cart.item.product.sub_category.name}
            ]for cart in carts
            }
        
        return JsonResponse({'result' : result}, status = 200)