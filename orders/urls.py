from django.urls import path

from orders.views import CartsView

urlpatterns = [
    path('/carts', CartsView.as_view())
]