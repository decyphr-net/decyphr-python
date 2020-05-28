"""Accounts Serializers

The Accounts app contains a number of different serializers that will all be
used for various instances.

The `EmptySerializer` is provided as a dummy serializer required by Django Rest
Framework's viewset classes.

Upon login, a user's incoming data will deserialized by the `UserLoginSerializer`.
This will simply just contain the login credentials provided by the user. Once
the user has successfully logged in and authenticated, the view will return
the `AuthorisedUserSerializer`.

Upon registration, a users's incoming data will be deserialized by the
`RegisterUserSerializer`. This will contain the information that the user
provided when filling out the registration form. Once the user has successfully
been created, the view will return the `AuthorisedUserSerializer`.
"""
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from accounts.models import UserProfile
from languages.models import Language


class UserLoginSerializer(serializers.Serializer):
    """Login Serializer

    The serializer that will be used for the user's incoming login credentials.

    Args:
        username (str): The username provided by the user
        password (str): The password provided by the user
    """
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthorisedUserSerializer(serializers.ModelSerializer):
    """Authorised User Serializer

    The serializer that will contain the general information about the user,
    after they have logged in
    """
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff',
            'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff', 'auth_token')
    
    def get_auth_token(self, obj):
        """Get auth token

        Get the user's authentication token.
        """
        token = Token.objects.get(user=obj)
        return token.key


class RegisterUserSerializer(serializers.ModelSerializer):
    """Register New User

    The serializer that will be used to regsiter a new user
    """

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'password', 'username', 'first_language',
            'language_being_learned', 'language_preference')
    
    def validate_email(self, value):
        """Validate email

        Validate the user's email address to ensure that the email address
        doesn't already exist in the database. An error will be raise if the
        email exists within the database
        """
        user = UserProfile.objects.filter(email=value)
        if user:
            raise serializers.ValidationError('Email is already taken')
        return BaseUserManager.normalize_email(value)
    
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class EmptySerializer(serializers.Serializer):
    pass
