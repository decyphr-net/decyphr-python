from rest_framework import serializers
from translator.models import Translation
from translator.analyzer import analyse


class IncomingSerializer(serializers.Serializer):
    """
    A very simple Serializer that exists for the sole purpose of
    deserialising the JSON that contains the text that the user
    wants to have translated
    """

    text_to_be_translated = serializers.CharField(required=True)


class TranslationSerializer(serializers.ModelSerializer):
    """
    The main serializer object that will be used to create
    translations and store them in the database, as well as
    render translations to a user
    """

    analysis = serializers.SerializerMethodField()

    class Meta:
        model = Translation
        fields = [
            "id",
            "source_text",
            "translated_text",
            "audio_file_path",
            "source_language",
            "target_language",
            "user",
            "analysis"
        ]
    
    def get_analysis(self, obj):
        return analyse(obj.source_text)
