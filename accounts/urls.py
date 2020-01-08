from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts.views import (
    UserRegistration, UserProfileView)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('current-user/', UserProfileView.as_view(), name='profiles'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
