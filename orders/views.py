import json

from django.http     import JsonResponse
from django.views    import View

from orders.models         import Cart
from core.token_decorators import token_decorator

class CartsView(View):
    @token_decorator
    def delete(self, requset, cart_id):
        try:
            Cart.objects.get(id = cart_id).delete()

            return JsonResponse({'message' : 'No Content'}, status = 201)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Cart'}, status = 400)