from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts.views import UserRegistration, UserProfileView, ObtainAuthToken

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path("current-user/", UserProfileView.as_view(), name="profile"),
    path("auth/", ObtainAuthToken.as_view(), name="api_token_auth")
]

urlpatterns = format_suffix_patterns(urlpatterns)
