from django.db import models
from accounts.models import UserProfile
from translator.models import Translation


class Session(models.Model): 

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)


class Question(models.Model):

    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    answer_provided = models.CharField(max_length=100, null=True, blank=True)
    correct = models.BooleanField(null=True, blank=True)
    
    