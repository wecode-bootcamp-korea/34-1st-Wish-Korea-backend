from django.urls import path

from orders.views import CartView, CartsView

urlpatterns = [
    path('/cart/<int:cart_id>', CartView.as_view()),
    path('/carts', CartsView.as_view())
]