from django.urls import path
from accounts.views import (
    RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView)

urlpatterns = [
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
]