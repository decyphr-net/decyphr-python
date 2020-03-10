from django.db import models
from accounts.models import UserProfile
from books.models import Book


class ReadingSession(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    duration = models.DurationField(null=False, blank=False)
    pages = models.FloatField()