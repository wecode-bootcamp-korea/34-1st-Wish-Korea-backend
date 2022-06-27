import json

import jwt

from django.http  import JsonResponse
from django.views import View

from orders.models   import Cart
from products.models import Item

class CartView(View):
    def post(self, requset):
        try:
            data    = json.loads(requset.body)['items']
            #user_id = requset.user
            print(data)
            user_id = 1
            carts = [ Cart.objects.get_or_create(
                user_id  = user_id, 
                item_id  = i.get('item_id'),
                ) for i in data]
            
            for idx,obj in enumerate(carts):
                print(idx,obj)
                if obj[1]:
                    obj[0].quantity = data[idx].get('quantity')
                    obj[0].save()
                else:
                    obj[0].quantity += data[idx].get('quantity')
                    obj[0].save()

            return JsonResponse({'result' : str(carts)}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)