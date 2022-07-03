from django.urls import path

from orders.views import CartView, CartsView

urlpatterns = [
    path('/carts', CartsView.as_view()),
    path('/cart', CartView.as_view())
]