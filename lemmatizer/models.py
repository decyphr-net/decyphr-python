from django.db import models
from languages.models import Language


class Verb(models.Model):

    name = models.CharField(max_length=50)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mood(models.Model):
    
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tense(models.Model):

    name = models.CharField(max_length=50)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Form(models.Model):

    form = models.CharField(max_length=50)
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE)
    tense = models.ForeignKey(Tense, on_delete=models.CASCADE)

    def __str__(self):
        return self.form