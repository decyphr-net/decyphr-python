from rest_framework import serializers
from translator.serializers import TranslationSerializer
from practice.serializers import SessionSerializer
from reading_sessions.serializers import ReadingSessionSerializer
from library.serializers import LibrarySerializer


class DashboardSerializer(serializers.Serializer):

    translations = TranslationSerializer(many=True)
    library_items = LibrarySerializer(many=True)
    practice_sessions = SessionSerializer(many=True)
    reading_sessions = ReadingSessionSerializer(many=True)