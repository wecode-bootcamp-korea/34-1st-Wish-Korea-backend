from django.urls import path

from products.views import NavigatorView

urlpatterns = [
    path('/navigator', NavigatorView.as_view())
]