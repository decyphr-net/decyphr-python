from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from translator import views

urlpatterns = [
    path("", views.TranslatorView.as_view(), name="translate"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
