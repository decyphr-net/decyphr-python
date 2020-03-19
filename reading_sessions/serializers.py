from rest_framework import serializers
from reading_sessions.models import ReadingSession
from translator.serializers import TranslationSerializer
from books.serializers import BookSerializer


class CreateReadingSessionSerializer(serializers.ModelSerializer):
    session_id = serializers.ReadOnlyField()
    translations = TranslationSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingSession
        fields = ["session_id", "user", "book", "duration", "pages", "translations"]


class ReadingSessionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    book = BookSerializer(read_only=True)

    class Meta:
        model = ReadingSession
        fields = ["id", "user", "book", "duration", "pages", "translation_set"]
