from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts.views import (
    UserRegistration, UserProfileView)

urlpatterns = [
    path('register/', UserRegistration.as_view()),
    path('current-user/', UserProfileView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
