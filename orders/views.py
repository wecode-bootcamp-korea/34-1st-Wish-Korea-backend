import json

import jwt

from django.http     import JsonResponse
from django.views    import View

from orders.models         import Cart
from core.token_decorators import token_decorator

class CartsView(View):
    @token_decorator
    def patch(self, requset):
        try:
            quantity = int(requset.GET.get('quantity'))
            cart     = Cart.objects.get(id = cart_id)
            
            if quantity > cart.item.stock:
                return JsonResponse({'message' : 'Out of stock'}, status = 400)
            
            cart.quantity += quantity
            cart.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Cart'}, status = 400)