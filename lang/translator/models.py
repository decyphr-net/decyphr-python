from django.db import models
from accounts.models import UserProfile
from languages.models import Language


class Translation(models.Model):

    user = models.ForeignKey(UserProfile,
        related_name='user', on_delete=models.CASCADE)
    source_text = models.TextField()
    translated_text = models.TextField()
    audio_file_path = models.CharField(max_length=200)
    source_language = models.ForeignKey(
        Language, on_delete=models.CASCADE,
        related_name='source_language')
    target_language = models.ForeignKey(
        Language, on_delete=models.CASCADE,
        related_name='target_language')