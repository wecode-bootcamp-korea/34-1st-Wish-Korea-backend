import json

import jwt

from django.http     import JsonResponse
from django.views    import View
from django.db.utils import IntegrityError

from orders.models         import Cart
from core.token_decorators import token_decorator

class CartView(View):
    @token_decorator
    def delete(self, requset):
        try:
            cart_id = requset.GET('cart_id')
            print(cart_id)
            Cart.objects.get(id = cart_id)

            return JsonResponse({'message' : 'No Content'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)
        
        except IntegrityError:
            return JsonResponse({'message' : 'Invalid Item'}, status = 400)