from rest_framework import serializers
from reading_sessions.models import ReadingSession
from translator.serializers import TranslationSerializer
from library.serializers import LibrarySessionSerializer


class CreateReadingSessionSerializer(serializers.ModelSerializer):
    session_id = serializers.ReadOnlyField()
    translations = TranslationSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingSession
        fields = ["session_id", "user", "library_item", "duration", "pages", "translations"]


class ReadingSessionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    library_item = LibrarySessionSerializer(read_only=True)

    class Meta:
        model = ReadingSession
        fields = ["id", "user", "library_item", "duration", "pages", "status", "translation_set"]
        extra_kwargs = {
            'user': {
                'required': False
            },
            'duration': {
                'required': False
            },
            'pages': {
                'required': False
            },
            'status': {
                'required': False
            },
            'translation_set': {
                'required': False
            },
        }
