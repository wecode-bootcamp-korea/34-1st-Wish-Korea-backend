from django.urls import path

from users.views import SignUpView

urlpatterns = [
    path('/sign',SignUpView.as_veiw())
]
