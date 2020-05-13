"""
A utility module that used to retrieve information from the Google
Books API.
"""
from datetime import datetime
import requests
from django.conf import settings
from languages.models import Language


def _construct_url(name, lang):
    """
    The URL for Google Books is a simple URL with query parameters.

    These are all combined together to form the full string and this
    function constructs that string
    """
    endpoint = settings.GOOGLE_BOOKS_ENDPOINT

    name_param = f"q={name}"
    projection_param = f"projection=lite"
    lang_param = f"langRestrict={lang}"
    order_param = f"orderBy=relevance"
    limit_param = f"limit=10"
    key_param = f"key={settings.GOOGLE_BOOKS_API}"

    return f"{endpoint}{name_param}&{projection_param}&{lang_param}&{order_param}&{key_param}"


def parse_book_data(data, lang):
    books = []
    for book in books:
        book = book["volumeInfo"]
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
        
        books.append({
            "title": title,
            "author": str(authors),
            "publisher": publisher,
            "publish_date": datetime.today().strftime('%Y-%m-%d'),
            "description": description,
            "language": language.id,
            "category": category,
            "small_thumbnail": small_thumbnail,
            "thumbnail": thumbnail
        })
    return books


def get_books(name, language_code):
    url = _construct_url(name, language_code)
    response = requests.get(url)
    if "items" in response.json():
        return response.json()["items"]
    else:
        return None