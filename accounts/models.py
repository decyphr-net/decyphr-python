"""
The accounts models.

This is where we'll store the information relevant to the users' accounts.

We want to able to store the user's information, such as their usual profile
information, their preferences for the site, and also a login history to give
users points for logging into the app everyday.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from languages.models import Language


class UserProfile(AbstractUser):
    """
    The user model that stores the user's overall profile.

    This model extends Django's `AbstractUser` and inherits the
    majority of the necessary fields like `username`, `email` and
    `password`. As such, not all validation is done at the model 
    level. Unique emails are enforced within the `serializers`.

    `first_language` and `language_being_learned` are also required
    fields, but only enforced by the `serializer`. Users created by
    other means, like superusers, will be given a default value upon
    the creation of the account.

    The `language_preference` field will allow users to choose what lanugage
    they would like to view the site in.
    """

    first_language = models.ForeignKey(
        Language, related_name="first_language", on_delete=models.CASCADE, default=1
    )
    language_being_learned = models.ForeignKey(
        Language,
        related_name="language_being_learned",
        on_delete=models.CASCADE,
        default=2,
    )
    language_preference = models.ForeignKey(
        Language,
        related_name="site_language_preference",
        on_delete=models.CASCADE,
        default=2
    )
