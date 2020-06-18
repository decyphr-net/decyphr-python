from rest_framework import serializers
from reading_sessions.models import ReadingSession
from translator.serializers import TranslationSerializer
from library.models import LibraryBook


class ReadingSessionSerializer(serializers.ModelSerializer):
    """The Reading Session Serializer

    This serializer will handle the serialization of the data for the
    `ReadingSession` model.

    Args:
        library_item (int): The ID of the library item that this reading
        session will map too
        duration (str): A string representation of the value that will be
        stored as the duration of the session
        pages (float): The number of pages that the user read during the
        session
        status (string): A one letter status indicator to inform what part of
        the process the reading session
    """

    id = serializers.IntegerField(read_only=True)
    library_item = serializers.PrimaryKeyRelatedField(
        queryset=LibraryBook.objects.all())
    translations = TranslationSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingSession
        depth = 1
        fields = [
            "id", "library_item", "duration",
            "pages", "status", "translations"
        ]
        extra_kwargs = {
            'duration': {
                'required': False
            },
            'pages': {
                'required': False
            },
            'status': {
                'required': False
            },
            'translations': {
                'required': False
            },
        }
        