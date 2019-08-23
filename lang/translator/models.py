from django.db import models


class Translation(models.Model):

    source_text = models.TextField()
    translated_text = models.TextField()
    audio_file_path = models.CharField(max_length=200)