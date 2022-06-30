import json

from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Sum, F
from django.db.models.functions import Coalesce

from orders.models         import Cart
from core.token_decorators import token_decorator

class CartView(View):
    @token_decorator
    def delete(self, request, cart_id):
        try:
            Cart.objects.get(id = cart_id, user = request.user).delete()

            return JsonResponse({'message' : 'No Content'}, status = 204)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Cart'}, status = 404)

class CartsView(View):
    @token_decorator
    def get(self, request):
        user   = request.user
        carts  = Cart.objects.filter(user = user).annotate(qauntity_sum = Sum('item__cart__quantity'))
        result = {
            'carts' : [
                {
                    'cart_id'   : cart.id,
                    'items'     : cart.item_id,
                    'name'      : cart.item.product.name,
                    'price'     : int(cart.item.price),
                    'size'      : cart.item.size.size_g,
                    'stock'     : cart.item.stock - cart.qauntity_sum,
                    'quantity'  : cart.quantity,
                    'image_url' : [image.url for image in cart.item.product.imageurl_set.all()],
                    'sub_catgory_name' : cart.item.product.sub_category.name
            }for cart in carts]
        }
            
        return JsonResponse({'result' : result}, status = 200)

    @token_decorator
    def post(self, request):
        try:
            items = json.loads(request.body)['items']
            for item in items:
                cart, created       = Cart.objects.get_or_create(user_id  = request.user.id, item_id  = item["id"])
                total_cart_quantity = Cart.objects.filter(item_id=item['id']).aggregate(total_quantity=Sum('quantity'))["total_quantity"]

                if cart.item.stock - total_cart_quantity < item["quantity"]:
                    return JsonResponse({'message' : 'Out of stock'}, status = 400)

                cart.quantity += item["quantity"]
                cart.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
           
        except KeyError:
            return JsonResponse({'message' : 'Key Error'}, status = 400)
