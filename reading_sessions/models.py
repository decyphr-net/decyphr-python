from django.db import models
from library.models import LibraryBook


class ReadingSession(models.Model):

    STATUS_TYPES = (
        ('N', 'Not Started'),
        ('I', 'In Progress'),
        ('E', 'Ended By User'),
        ('F', 'Finished'),
    )

    library_item = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    duration = models.DurationField(null=False, blank=False)
    pages = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_TYPES, default=STATUS_TYPES[0][0])