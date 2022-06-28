from django.urls import path

from orders.views import CartsView, CartView

urlpatterns = [
    path('/carts', CartsView.as_view()),
    path('/cart', CartView.as_view())
]