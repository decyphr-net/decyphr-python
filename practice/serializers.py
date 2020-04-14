from rest_framework import serializers
from .models import Question, Session
from translator.serializers import TranslationSerializer


class QuestionSerializer(serializers.ModelSerializer):

    translation = TranslationSerializer(read_only=True)
    correct = serializers.BooleanField(read_only=True)
    correct_answer = serializers.SerializerMethodField(read_only=True)

    def get_correct_answer(self, obj):
       return obj.translation.translated_text

    class Meta:
        model = Question
        fields = ["id", "answer_provided", "correct", "translation", "correct_answer"]


class SessionSerializer(serializers.ModelSerializer):

    question_set = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Session
        fields = ["id", "user", "duration", "score", "question_set"]