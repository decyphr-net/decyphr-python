from django.contrib import admin
from lemmatizer.models import Verb, Tense, Mood, Form

admin.site.register(Verb)
admin.site.register(Tense)
admin.site.register(Mood)
admin.site.register(Form)