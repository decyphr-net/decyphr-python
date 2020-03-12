from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from reading_sessions import views

urlpatterns = [
    path("", views.ReadingSessionView.as_view(), name="reading_sessions"),
    path("<int:pk>/", views.ReadingSessionView.as_view(), name="reading-session-by-id"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
