from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from library import views

urlpatterns = [
    path("", views.LibraryBooksView.as_view(), name="library"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
