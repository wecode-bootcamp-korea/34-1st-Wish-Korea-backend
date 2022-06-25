import json

import jwt

from django.http  import JsonResponse
from django.views import View

from orders.models import Cart

class CartView(View):
    def post(self, requset):
        try:
            data     = json.loads(requset.body)
            user_id  = requset.user
            item_id  = data['item_id']
            quantity = data['quantity']

            Cart.objects.create(
                user_id  = user_id,
                item_id  = item_id,
                quantity = quantity
            )

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)