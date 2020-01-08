from django.contrib.auth.models import AbstractUser
from django.db import models
from languages.models import Language


class UserProfile(AbstractUser):

    first_language = models.ForeignKey(
        Language,
        related_name='first_language',
        on_delete=models.CASCADE,
        default=2
    )
    language_being_learned = models.ForeignKey(
        Language,
        related_name='language_being_learned',
        on_delete=models.CASCADE,
        default=1
    )