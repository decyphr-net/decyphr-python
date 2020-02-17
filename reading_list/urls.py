from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from reading_list import views

urlpatterns = [
    path("", views.ReadingListView.as_view(), name="reading_list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
