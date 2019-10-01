from rest_framework import serializers 
from accounts.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    The main serializer object that will be used to retrieve user
    information from the database so that it can be displayed to
    the currently looged in user
    """

    class Meta:
        model = UserProfile
        depth = 1
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'date_joined', 'first_language', 'language_being_learned']