from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts.views import (
    UserRegistration, UserPofileView)

urlpatterns = [
    path('register/', UserRegistration.as_view()),
    path('current-user/', UserPofileView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
