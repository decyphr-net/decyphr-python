from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from books.views import BookAPIView

urlpatterns = [
    path("", BookAPIView.as_view(), name="books"),
    path("<int:pk>/", BookAPIView.as_view(), name="book-id"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
