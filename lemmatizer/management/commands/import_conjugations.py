from verbecc import Conjugator
from django.core.management.base import BaseCommand, CommandError
from lemmatizer.models import Verb, Form, Tense
from languages.models import Language


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def get_verb_conjugations(self, cg, verb):
        return cg.conjugate(verb)

    def get_verb_moods(self, verb):
        return verb["moods"].items()
    
    def get_table(self, mood):
        return mood.items()

    def handle(self, *args, **kwargs):
        verbs = Verb.objects.all()[:5000]
        cg = Conjugator(lang="pt")
        for verb in verbs:
            verb_name = self.get_verb_conjugations(cg, verb.name)
            for mood_name, mood in self.get_verb_moods(verb_name):
                for tense_name, tense in self.get_table(mood):
                    tense_name = Tense.objects.get(name=tense_name, mood__name=mood_name)
                    for item in tense:
                        if item == "-":
                            continue
                        new_form = Form(form=item, verb=verb, tense=tense_name)
                        new_form.save()