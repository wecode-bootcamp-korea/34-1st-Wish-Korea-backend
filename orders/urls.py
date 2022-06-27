from django.urls import path

from orders.views import CartView

urlpatterns = [
    path('/', CartView.as_view())
]