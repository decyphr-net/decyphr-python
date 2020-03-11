from rest_framework import serializers
from reading_sessions.models import ReadingSession
from translator.serializers import TranslationSerializer


class ReadingSessionSerializer(serializers.ModelSerializer):
    translation_set = TranslationSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingSession
        fields = ["user", "book", "duration", "pages", "translation_set"]