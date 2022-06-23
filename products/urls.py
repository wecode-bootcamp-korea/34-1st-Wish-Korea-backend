from django.urls import path

from products.views import NavigatorView, ListView

urlpatterns = [
    path('/navigator', NavigatorView.as_view()),
    path('/list', ListView.as_view(),)
]