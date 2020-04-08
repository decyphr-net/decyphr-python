from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from practice import views

urlpatterns = [
    path("", views.PracticeQuestionView.as_view(), name="question"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
