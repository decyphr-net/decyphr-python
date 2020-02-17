import requests
from django.conf import settings
from languages.models import Language


def _construct_url(name, lang):
    endpoint = settings.GOOGLE_BOOKS_ENDPOINT
    key = settings.GOOGLE_BOOKS_API
    return f"{endpoint}q={name}&projection=lite&langRestrict={lang}&orderBy=relevance&limit=10&key={key}"


def parse_book_data(data, lang):
    book = data["volumeInfo"]
    try:
        title = "" if book.get("title") is None else book.get("title")
        authors = "" if book.get("authors") is None else book.get("authors")
        publisher = "" if book.get("publisher") is None else book.get("publisher")
        publish_date = "" if book.get("publishedDate") is None else book.get("publishedDate")
        description = "" if book.get("description") is None else book.get("description")
        language = Language.objects.get(short_code=lang)
        category = "" if book.get("mainCategory") is None else book.get("mainCategory")
        small_thumbnail = "" if book.get("imageLinks") is None else book.get("imageLinks").get("smallThumbnail")
        thumbnail = "" if book.get("imageLinks") is None else book.get("imageLinks").get("thumbnail")
    except KeyError:
        return None

    book_dict = {
        "title": title,
        "author": authors,
        "publisher": publisher,
        "publish_date": publish_date,
        "description": description,
        "language": language,
        "category": category,
        "small_thumbnail": small_thumbnail,
        "thumbnail": thumbnail
    }
    return book_dict

def get_books(name, language_code):
    url = _construct_url(name, language_code)
    response = requests.get(url)
    if "items" in response.json():
        return response.json()["items"]
    else:
        return None