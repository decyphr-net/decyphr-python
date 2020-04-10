from rest_framework import serializers
from .models import Question, Session
from translator.serializers import TranslationSerializer


class QuestionSerializer(serializers.ModelSerializer):

    translation = TranslationSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "answer_provided", "correct", "translation"]


class SessionSerializer(serializers.ModelSerializer):

    question_set = QuestionSerializer(read_only=True, many=True)


    class Meta:
        model = Session
        fields = ["id", "user", "duration", "question_set"]