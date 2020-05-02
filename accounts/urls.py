from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts.views import ObtainAuthToken

urlpatterns = [
    path("", ObtainAuthToken.as_view(), name="api_token_auth")
]

urlpatterns = format_suffix_patterns(urlpatterns)
