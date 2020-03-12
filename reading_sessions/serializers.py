from rest_framework import serializers
from reading_sessions.models import ReadingSession
from translator.serializers import TranslationSerializer
from books.serializers import BookSerializer


class ReadingSessionSerializer(serializers.ModelSerializer):
    translation_set = TranslationSerializer(many=True, read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = ReadingSession
        fields = ["id", "user", "book", "duration", "pages", "translation_set"]
