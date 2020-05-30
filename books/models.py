"""
The Book Model

This model will store all necessary information pertaining to each individual
book.
"""
from datetime import datetime
from django.db import models
from languages.models import Language


class Book(models.Model):

    title = models.CharField(max_length=150, null=False, blank=False)
    author = models.CharField(max_length=150, null=False, blank=False)
    publisher = models.CharField(max_length=150, null=True, blank=True)
    publish_date = models.DateField(
        blank=True, null=True, default=datetime.now().today)
    description = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    small_thumbnail = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title