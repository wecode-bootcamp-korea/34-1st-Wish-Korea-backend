from django.urls import path

from orders.views import CartsView

urlpatterns = [
    path('/cart/<int:cart_id>', CartsView.as_view())
]