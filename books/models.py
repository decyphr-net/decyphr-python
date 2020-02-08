from django.db import models
from languages.models import Language


class Book(models.Model):

    title = models.CharField(max_length=150, null=False, blank=False)
    author = models.CharField(max_length=150, null=False, blank=False)
    publisher = models.CharField(max_length=150, null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    category = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    small_thumbnail = models.URLField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.title