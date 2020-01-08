from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from accounts.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    The main serializer object that will be used to retrieve user
    information from the database so that it can be displayed to
    the currently logged in user
    """

    class Meta:
        model = UserProfile
        depth = 1
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'date_joined', 'first_language', 'language_being_learned']


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance