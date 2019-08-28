from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views

urlpatterns = [
    path('<int:pk>/', views.UserPofileView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)