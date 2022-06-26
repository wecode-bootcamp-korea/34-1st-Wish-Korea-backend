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
            item_id_list  = [item['item_id'] for item in data['items']]
            quantity_list = [item['quantity'] for item in data['items']]

            cart = [ Cart.objects.get_or_create(
                user_id  = user_id, 
                item_id  = item_id,
                quantity = quantity_list[idx]) for idx, item_id in enumerate(item_id_list)
                ]

            return JsonResponse({'result' : 'aga'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)