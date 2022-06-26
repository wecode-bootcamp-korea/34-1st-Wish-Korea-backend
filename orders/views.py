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
            item_id_list  = [i['item_id'] for i in data['items']]
            quantity_list = [i['quantity'] for i in data['items']]

            cart = Cart.objects.get_or_create(user_id = user_id, item_id = user_id)

            return JsonResponse({'message' : 'Create'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)