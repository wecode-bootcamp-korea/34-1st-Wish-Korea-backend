import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Sum

from orders.models         import Cart
from core.token_decorators import token_decorator

class CartsView(View):
    @token_decorator
    def patch(self, requset):
        try:
            data                = json.loads(requset.body)
            cart                = Cart.objects.get(id = data['cart_id'])
            total_cart_quantity = Cart.objects.filter(item_id=6).aggregate(total_quantity=Sum('quantity'))["total_quantity"]
            if cart.item.stock - total_cart_quantity < data["quantity"]:
                    return JsonResponse({'message' : 'Out of stock'}, status = 400)
            
            cart.quantity += quantity
            cart.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Cart'}, status = 400)

class CartsView(View):
    @token_decorator
    def post(self, requset):
        try:
            items = json.loads(requset.body)['items']

            for item in items:
                cart, created       = Cart.objects.get_or_create(user_id  = request.user.id, item_id  = item["id"])
                total_cart_quantity = Cart.objects.filter(item_id=6).aggregate(total_quantity=Sum('quantity'))["total_quantity"]

                if cart.item.stock - total_cart_quantity < item["quantity"]:
                    return JsonResponse({'message' : 'Out of stock'}, status = 400)

                cart.quantity += item["quantity"]

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
           
        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)