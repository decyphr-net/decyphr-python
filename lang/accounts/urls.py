from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views

urlpatterns = [
    path('current-user/', views.current_user),
    path('users/', views.UserAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
