from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from practice import views

urlpatterns = [
    path("questions/", views.PracticeQuestionView.as_view(), name="question"),
    path("sessions/", views.PracticeSessionView.as_view(), name="session"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
