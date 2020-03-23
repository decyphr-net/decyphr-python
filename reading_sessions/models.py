from django.db import models
from accounts.models import UserProfile
from library.models import LibraryBooks


class ReadingSession(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    library_item = models.ForeignKey(LibraryBooks, on_delete=models.CASCADE)
    duration = models.DurationField(null=False, blank=False)
    pages = models.FloatField()