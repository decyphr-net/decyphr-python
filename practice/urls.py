from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from practice import views

urlpatterns = [
    path("questions/", views.PracticeQuestionView.as_view(), name="question"),
    path("questions/<int:pk>/", views.PracticeQuestionView.as_view(), name="answer-question"),
    path("sessions/", views.PracticeSessionView.as_view(), name="session"),
    path("sessions/<int:pk>/", views.PracticeSessionView.as_view(), name="session-update"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
