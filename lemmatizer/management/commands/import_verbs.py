from verbecc import Conjugator
from django.core.management.base import BaseCommand, CommandError
from lemmatizer.models import Verb
from languages.models import Language


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        portuguese = Language.objects.first()
        cj = Conjugator(lang=portuguese.short_code)
        verb_list = cj.get_verbs_list()
        for verb in verb_list:
            new_verb = Verb(name=verb, language=portuguese)
            new_verb.save()