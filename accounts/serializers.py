from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.validators import UniqueValidator
from accounts.models import UserProfile
from languages.models import Language


class UserSerializer(serializers.ModelSerializer):
    """
    The main serializer object that will be used to retrieve user
    information from the database so that it can be displayed to
    the currently logged in user
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    first_language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())
    language_being_learned = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all()
    )

    class Meta:
        model = UserProfile
        depth = 1
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "date_joined",
            "first_language",
            "language_being_learned",
        ]

    def create(self, validated_data):
        """
        When creating a new user, we need to take the password from
        the incoming data and use Django's built in `set_password` to
        properly encrypt the password
        """
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, data):
        """
        We'll do an extra step of validation to ensure that a user
        hasn't chosen thesame language from both language fields upon
        registration
        """
        if data["first_language"] == data["language_being_learned"]:
            raise serializers.ValidationError(
                "You cannot learn a language that is the same as your native language."
            )
        return data
