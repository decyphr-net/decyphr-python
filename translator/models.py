from django.db import models
from translator.aws_utils import delete_from_bucket
from accounts.models import UserProfile
from languages.models import Language


class Translation(models.Model):

    user = models.ForeignKey(UserProfile, related_name="user", on_delete=models.CASCADE)
    source_text = models.TextField()
    translated_text = models.TextField()
    audio_file_path = models.CharField(max_length=200)
    source_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="source_language"
    )
    target_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="target_language"
    )

    def delete(self):
        delete_from_bucket(self.audio_file_path)
        super(Translation, self).delete()

    def __str__(self):
        return "{} - {} -> {}".format(
            self.user, self.source_text, self.translated_text)
