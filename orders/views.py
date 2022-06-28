import json

from django.http     import JsonResponse
from django.views    import View

from orders.models         import Cart
from core.token_decorators import token_decorator

class CartView(View):
    @token_decorator
    def delete(self, requset, cart_id):
        try:
            Cart.objects.get(id = cart_id, user = requset.user).delete()

            return JsonResponse({'message' : 'No Content'}, status = 200)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Cart'}, status = 400)

class CartsView(View):
    @token_decorator
    def get(self, request):
        user   = request.user
        carts  = Cart.objects.filter(user = user)
        result = {
            'carts' : [
                {
                    'cart_id'   : cart.id,
                    'items'     : cart.item_id,
                    'name'      : cart.item.product.name,
                    'price'     : int(cart.item.price),
                    'size'      : cart.item.size.size_g,
                    'stock'     : cart.item.stock,
                    'quantity'  : cart.quantity,
                    'image_url' : [image.url for image in cart.item.product.imageurl_set.all()],
                    'sub_catgory_name' : cart.item.product.sub_category.name
            }for cart in carts]
        }
            
        return JsonResponse({'result' : result}, status = 200)
