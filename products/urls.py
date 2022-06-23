from django.urls import path

from products.views import NavigatorView

urlpatterns = [
    path('/categories', NavigatorView.as_view())
]