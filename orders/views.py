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
        try:
            user   = request.user
            carts  = Cart.objects.filter(user = user)

            result = {
                'carts' : [
                    {
                        'cart_id'   : cart.id,
                        'items'     : cart.item_id,
                        'name'      : cart.item.product.name,
                        'price'     : cart.item.price,
                        'size'      : cart.item.size.size_g,
                        'stock'     : cart.item.stock,
                        'image_url' : [image.url for image in cart.item.product.imageurl_set.all()],
                        'sub_catgory_name' : cart.item.product.sub_category.name}
                ]for cart in carts
                }

            return JsonResponse({'result' : result}, status = 200)

        except IndexError:
            result['cart']['image_url'] = ''
            return JsonResponse({'result' : result}, status = 400)