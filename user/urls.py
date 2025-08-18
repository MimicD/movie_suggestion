from django.urls import path
from .views import UserCreateView, UserLoginView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name = "user-create"),
    path('login/', UserLoginView.as_view(), name = "user-login")
]
