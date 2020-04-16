from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from dashboard import views

urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
