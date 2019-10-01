from django.db import models


class Language(models.Model):

    name = models.CharField(max_length=50, blank=False, null=False)
    code = models.CharField(max_length=8, blank=False, null=False)
    short_code = models.CharField(max_length=2, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return "{} - {}".format(self.name, self.code)
