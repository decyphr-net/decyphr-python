"""
The utilities used to help with the integration with Google Books

This module contains a number of functions that will be used to handle the
communication between the BookViewset and the Google Books API.

Google Books allows us to search for books with a number of parameters. The
main parameters that we'll use will be:

    - **name**: the name of the book (this does not need to the full name of
      the book as the API will return partial matches)
    - **projection**: we use `lite` to lower the footprint that we're using
    - **langRestrict**: restrict results to be a specific language. We will use
      the language that the user is learning
    - **orderBy**: we can order by `newest` or `relevance`. Right now we're
      ordering by relevance in order to ensure that users will still be able to
      search for books that are both new and old
    - **limit_param**: we are currently limiting the results to 10
    - **key_param**: the Google Books API key which is defined in the `settings`

The data that comes back from the API is not structured very well. Not all
books contain the information that we're looking for and dates have no set
format. Some dates only contain years, some years and months while others have
the year, month and date.

In addition to this, Google doesn't even provide keys in the instances where
they don't have information, meaning that the `KeyError` is thrown 
often here.

Because the information is not always consistent, we'll store the information
that we can for now. Most of the database will allow for empty fields to
accomodate these issues here.

For now, we'll stick with the Google Books API as it seems to be the most
complete API to date. If a more consistent solution is found can consider
changing, but it's better to stick with Google for now.
"""
from datetime import datetime
import requests
from django.conf import settings
from languages.models import Language


def _construct_url(name, lang):
    """Construct the Google Books URL
    
    The URL for Google Books is a simple URL with query parameters. These are
    all combined together to form the full string and this function constructs
    that string.

    Args:
        name (str): the name of the book to be searched for
        lang (str): the short language code to determine the langauge that the
        book should be. NOTE: This *must* be the short code, for example `pt`
        or `en`
    
    Returns:
        str: The URL that will be used to call the Google Books API, containing
        the name of the book, the language, order, limit and the Google Books
        API key
    
    Example:
        This must called with the name of the of the book that the user is
        searching for, and the language code must be a `short_code`::

            url = _construct_url("harry", "en")
        
        The API will perform partial title searches so the full book name not
        required::

            url = _construct_url("ha", "en")
    """
    endpoint = settings.GOOGLE_BOOKS_ENDPOINT
    name_param = f"q={name}"
    projection_param = f"projection=full"
    lang_param = f"langRestrict={lang}"
    order_param = f"orderBy=relevance"
    limit_param = f"limit=10"
    key_param = f"key={settings.GOOGLE_BOOKS_API}"
    return f"{endpoint}{name_param}&{projection_param}&{lang_param}&{order_param}&{key_param}"


def _parse_book_fields(field_name, dataset):
    """Parse the data from the book object

    The `KeyError` pops up very regularly when it comes to reading in the data
    from the Google Books API. If they don't have a specific piece of
    information they don't even provide the key so this needs to be handled in
    a lot of different places. Wrapping this *pickling* in this function
    seemed to be the tidiest way to deal with this.

    This function will check for the existance of a key and return the value
    associated with the key, or return `None` for that field if the key doesn't
    exist.

    Args:
        field_name (str): The name of the field that we want to retrieve
        data (dict): The book information that came back from the Google Books
        API
    
    Returns:
        str: The value for the given field, or,
        None: If the field is not found
    
    Example:
        This is a private function that should only be used within this
        module::

            book = book["volumeInfo"]
            book_title = _parse_book_fields("title", book)
    """
    try:
        return dataset.get(field_name)
    except KeyError:
        return None


def _parse_book_image_urls(field_name, dataset):
    """Parse the image data from the book object

    This function will check for the existance of a key and return the value
    associated with the key, or return `None` for that field if the key doesn't
    exist.

    This function is mostly the same as `_parse_book_fields` with the only
    difference being that the image information is nested.

    Args:
        field_name (str): The name of the field that we want to retrieve
        data (dict): The book image information that came back from the Google
        Books API
    
    Returns:
        str: The value for the given field, or,
        None: If the field is not found
    
    Example:
        This is a private function that should only be used within this
        module::

            book = book["volumeInfo"]
            book_thumbnail = _parse_book_image_urls("thumbnail", book)
            book_small_thumbnail =  _parse_book_image_urls("smallThumbnail", book)
    """
    try:
        return "" if dataset.get(
            "imageLinks") is None else dataset.get("imageLinks").get(field_name)
    except KeyError:
        return None


def _populate_book_data(volume_info, lang):
    """Generate the book dict

    This will generate a dict version of the book that we'll be able to
    serialize and store in our own database as the Google Books API does not
    give us the information in a format that's useable for use.

    Args:
        volume_info (dict): The book information that was provided by Google
        lang (int): The ID of the language that the user is learning
    
    Returns:
        dict: Returns a dict containing the `title`, `author`, `publisher`,
        `publish_date`, description`, `language`, `category`, `small_thumbnail`,
        `thumbnail`
    
    Example:
        This is most likely going to be used in a list comprehension as we want
        to get the information for multiple books rather than one::
        
            books = [_populate_book_data(book["volumeInfo"], lang) for book in data]
    
    TODO:
        The date needs to be address. For now, all dates are defaulting to the
        date that the search was performed because of the inconsistancies with
        the data. This needs to be resolved
    """
    return {
        "title": _parse_book_fields("title", volume_info),
        "author": str(_parse_book_fields("authors", volume_info)),
        "publisher": _parse_book_fields("publisher", volume_info),
        "publish_date": datetime.today().strftime('%Y-%m-%d'),
        "description": _parse_book_fields("description", volume_info),
        "language": lang,
        "category": _parse_book_fields("mainCategory", volume_info),
        "small_thumbnail": _parse_book_image_urls("smallThumbnail", volume_info),
        "thumbnail": _parse_book_image_urls("thumbnail", volume_info)
    }


def parse_book_data(data, lang):
    """Parse the book information

    This function will take all of the information that was recieved from the
    API and format it in a way that we can store it in our database.

    Args:
        data (list): The list of books that came back from the API. This list
        must be comprised of dicts that contain a `volumeInfo` key
        lang (id): The ID of the language that the user is learning
    
    Returns:
        list: A list of the parsed and formatted book information for us to
        write to the database
    
    Example:
        This function can be used once the data has been retruned from the API::

            api_data = get_books(search_parameters, user_language.short_code)
            books = parse_book_data(api_data, user_language.id)
    """
    books = [_populate_book_data(book["volumeInfo"], lang) for book in data]
    return books


def get_books(name, language_code):
    """Get books from Google Books API

    Retrieve the set of books from the Google API.

    Args:
        name (str): The name of the book being searched for
        language_code (str): The short code of the language that the student
        is learning
    
    Returns:
        list: The list of books returned from the API
        None: If there was an issue retrieving the data from the API
    
    Example:
        This function must be called with the language short code::
        
            api_data = get_books(search_parameters, user_language.short_code)
    """
    url = _construct_url(name, language_code)
    response = requests.get(url)
    if "items" in response.json():
        return response.json()["items"]
    else:
        return None