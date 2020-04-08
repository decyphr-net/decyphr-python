from rest_framework import serializers
from .models import Question, Session


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = "__all__"