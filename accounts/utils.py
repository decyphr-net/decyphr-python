"""Accounts Utilities

The module contains a set of helper methods that will be used to create and
authenticate users within the application. These functions will mostly exist
for the purpose of wrapping existing functionality within Django
"""
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import UserProfile


def get_and_authenticate_user(username, password):
    """Authenticate the user

    Authenticate the user that's attempting to log in using their username and
    password.

    Args:
        username (str): The username that the user provided
        password (str): The password that the user provided
    
    Returns:
        UserProfile: An authenticated user instance is returned if the
        authentication process is successful
    
    Raises:
        ValidationError: If the username and password cannot be matched
    
    Examples:
        This function can be called by explicitly passing the username and
        password::

            user = get_and_authenticate_user(username, password)
        
        Or, by unpacking the `UserLoginSerializer`::
        
            user = get_and_authenticate_user(**serializer.validated_data)
    """
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError(
            "Invalid email/password. Please try again!")
    return user


def create_user_account(
    email,
    password,
    username='',
    first_language=0,
    language_being_learned=0,
    language_preference=0
):
    """Create User Account

    Create a new user account using the information provided. This function
    will just wrap Django's `.create_user` method in order to create a new
    user instance with the protected password.

    Args:
        email (str): The email provided by the user
        password (str): The password provided by the user
        username (str): The username provided by the user
        first_language (int): The ID of the language that the user chose as
        their first language
        language_being_learned (int): The ID of the language that the user
        chose as the language that they wish to learn
        language_preference (int): The ID of the language that the user
        chose as the language that they wish to view the site in
    
    Returns:
        UserProfile: The newly created user instance
    
    Example:
        This function can be called by explicitly passing in the arguments::

            user = create_user_account(email, password, username,
                first_language, language_being_learned, language_preference)
        
        Or, by unpacking the `RegisterUserSerializer`::
        
            user = create_user_account(**serializer.validated_data)
    """
    user = UserProfile.objects.create_user(
        email=email, password=password, username=username,
        first_language=first_language,
        language_being_learned=language_being_learned,
        language_preference=language_preference)
    token = Token.objects.create(user=user)
    return user