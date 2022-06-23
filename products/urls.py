from django.urls import path

from products.views import CategoryView, ListView

urlpatterns = [
    path('/categories', CategoryView.as_view()),
    path('/list', ListView.as_view(),)
]