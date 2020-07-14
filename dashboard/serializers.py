from rest_framework import serializers
from translator.serializers import TranslationSerializer
from library.serializers import LibrarySerializer


class DashboardSerializer(serializers.Serializer):

    translations_count = serializers.IntegerField()
    library_item_count = serializers.IntegerField()
    practice_sessions_count = serializers.IntegerField()
    reading_sessions_count = serializers.IntegerField()                                                                                                                                   