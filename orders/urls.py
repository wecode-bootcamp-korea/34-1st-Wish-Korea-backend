from django.urls import path

from orders.views import CartView, CartsView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/carts', CartsView.as_view())
]