"""
The Book Views.

This module will handle the interaction between the client and the Book model.

Clients can retrieve single book instances, or lists of books. When a client
searches for a book, we check to see if the book is present in the database
and if it's not, the book will be searched for in Google Books and if found
there, they will be added to the database and for easier access when a client
tries to access this data at a later point.
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from languages.models import Language
from books.models import Book
from books.serializers import BookSerializer
from books.google_utils import get_books, parse_book_data


class BookViewSet(viewsets.ModelViewSet):
    """BookViewSet

    Handles the interactions that the user will have with the the books within
    the application. Only users that have been authenticated will be able to
    access the books.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def retrieve(self, request, pk):
        """Get by ID.
        
        Retrieve a single book instance based on it's ID.

        Args:
            self (BookViewSet): The current BookViewSet instance
            request (Request): The current request being handled
            pk (int): The ID of the book that is being requested by the client

        Returns:
            Reponse: The serialized book and the status

        Example:
            This endpoint will be available at::

                /books/<pk>

            In order to call this from cURL, use the following::

                curl -H 'Content-type: application/json' \\
                     -H 'Authorization: Token <your_token>' \\
                    http://127.0.0.1:8000/books/2/

        Example Response:
            The response data should look like::

                {
                    "id": 2,
                    "title": "Reading Harry Potter",
                    "author": "['Giselle Liza Anatol']",
                    "publisher": "Greenwood Publishing Group",
                    "publish_date": "2020-05-14",
                    "description": "The tropes and themes of J. K. Rowling's ...",
                    "category": "",
                    "small_thumbnail": "http://books.google.com/books/...",
                    "thumbnail": "http://books.google.com/books/...",
                    "language": 2
                }
        
        Raises:
            HTTP 401 Unauthorized status if the user is not authorized
        """
        book = Book.objects.get(id=pk)
        serializer = self.serializer_class(book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Get a list of books

        Retrieves a list of books from the database, but will retrieve a list
        from Google Books if no results are found in the database.

        This endpoint must be called with a query paramater of `name`

        Args:
            self (BookViewSet): The current BookViewSet instance
            request (Request): The current request being handled
        
        Returns:
            Reponse: The serialized list of books and the status
        
        Example:
            This endpoint will be available at::

                /books/?name=<book_name>

            In order to call this from cURL, use the following::

                curl -X POST -H 'Content-type: application/json' \\
                     -H 'Authorization: Token <your_token>' \\
                    http://127.0.0.1:8000/books/?name=harry
        
        Example output:
            The response data should look like::
            
                [
                    {
                        "id": 1,
                        "title": "The Ivory Tower and Harry Potter",
                        "author": "['Lana A. Whited']",
                        "publisher": "University of Missouri Press",
                        "publish_date": "2020-05-14",
                        "description": "Now available in paper, The Ivory...",
                        "category": "",
                        "small_thumbnail": "http://books.google.com/books/...",
                        "thumbnail": "http://books.google.com/books/...",
                        "language": 2
                    },
                    {
                        "id": 2,
                        "title": "Reading Harry Potter",
                        "author": "['Giselle Liza Anatol']",
                        "publisher": "Greenwood Publishing Group",
                        "publish_date": "2020-05-14",
                        "description": "The tropes and themes of J. K. ...",
                        "category": "",
                        "small_thumbnail": "http://books.google.com/books/...",
                        "thumbnail": "http://books.google.com/books/...",
                        "language": 2
                    }
                ]
        
        Raises:
            HTTP 401 Unauthorized status if the user is not authorized
        """
        search_parameters = request.query_params["name"]
        user_language = request.user.language_being_learned

        # If the set of books returned from the database is 0, get the books
        # from the Google Books API
        if Book.objects.filter(title__icontains=search_parameters).count() == 0:
            api_data = get_books(search_parameters, user_language.short_code)
            books = parse_book_data(api_data, user_language.id)

            # DRF was returning odd errors when trying to save this data with
            # `many=True` so for now each book that comes from the API will
            # created until another bulk operation can be found
            for book in books:
                serializer = self.serializer_class(data=book)
                if serializer.is_valid():
                    serializer.save()
        
        books = Book.objects.filter(title__icontains=search_parameters)
        serializer = self.serializer_class(books, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
