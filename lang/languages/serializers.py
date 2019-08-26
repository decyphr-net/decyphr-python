from rest_framework import serializers
from languages.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    """
    The main serializer object that will be used to render a list of
    languages to a user, and also provide details on the language for
    a user to learn more about the language
    """

    class Meta:
        model = Language
        fields = ['name', 'code', 'short_code', 'description']