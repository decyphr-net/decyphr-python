import requests
from django.conf import settings


def translate_text(text, source_lang, target_lang):
    data = {
        "initial_language_code": target_lang,
        "target_language_code": source_lang,
        "text": text,
    }

    response = requests.post(settings.FULL_TRANSLATION, data)
    return response.json()
