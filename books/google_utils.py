import requests
from django.conf import settings


def _construct_url(name, lang):
    endpoint = settings.GOOGLE_BOOKS_ENDPOINT
    key = settings.GOOGLE_BOOKS_API
    return f"{endpoint}q={name}&projection=lite&langRestrict={lang}&orderBy=relevance&limit=10&key={key}"


def get_books(name, language_code):
    url = _construct_url(name, language_code)
    response = requests.get(url)
    if "items" in response.json():
        return response.json()["items"]
    else:
        return None