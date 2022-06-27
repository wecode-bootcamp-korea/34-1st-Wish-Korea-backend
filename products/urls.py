from django.urls import path

<<<<<<< HEAD
from products.views import CategoryView, ListView

urlpatterns = [
    path('/categories', CategoryView.as_view()),
    path('/', ProductListView.as_view(),)
=======
from products.views import CategoryView, ProductView

urlpatterns = [
    path('/categories', CategoryView.as_view()),
    path('/<int:product_id>', ProductView.as_view())
>>>>>>> main
]