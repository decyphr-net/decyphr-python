from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from languages import views

urlpatterns = [
    path('', views.LanguageView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)