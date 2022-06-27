import json

import jwt

from django.http     import JsonResponse
from django.views    import View
from django.db.utils import IntegrityError

from orders.models         import Cart
from core.token_decorators import token_decorator

class CartView(View):
    @token_decorator
    def post(self, requset):
        try:
            data  = json.loads(requset.body)['items']
            user  = requset.user
            carts = (Cart.objects.get_or_create(
                user    = user, 
                item_id = item.get('item_id'),
                ) for item in data)
            
            for idx,obj in enumerate(carts):
                if data[idx].get('quantity') > obj[0].quantity:
                    return JsonResponse({'message' : 'Out of stock'}, status = 400)

                if obj[1]:
                    obj[0].quantity = data[idx].get('quantity')
                    obj[0].save()
                else:
                    obj[0].quantity += data[idx].get('quantity')
                    obj[0].save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)
        
        except IntegrityError:
            return JsonResponse({'message' : 'Invalid Item'}, status = 401)