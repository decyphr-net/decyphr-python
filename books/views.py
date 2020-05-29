"""
The Book Views.

This module will handle the interaction between the client and the Book model.

Clients can retrieve single book instances, or lists of books. When a client
searches for a book, we check to see if the book is present in the database
and if it's not, the book will be searched for in Google Books and if found
there, they will be added to the database and for easier access when a client
tries to access this data at a later point
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
    the application.

    Only users that have been authenticated will be able to access the books.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def retrieve(self, request, pk):
        """Get by ID

        Retrieve a single book instance based on it's ID.

        Args:
            self (BookViewSet): The current BookViewSet instance
            request (Request): The current request being handled
            pk (int): The ID of the book that is being requested by the client
        
        Returns:
            Reponse: The serialized book and the status
        """
        book = Book.objects.get(id=pk)
        serializer = self.serializer_class(book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Get a list of books

        Retrieves a list of books from the database, but will retrieve a list
        from Google Books if no results are found in the database

        Args:
            self (BookViewSet): The current BookViewSet instance
            request (Request): The current request being handled
        
        Returns:
            Reponse: The serialized list of books and the status
        """
        search_parameters = request.query_params["name"]
        user_language = request.user.language_being_learned
        books = Book.objects.filter(title__icontains=search_parameters)

        # If the set of books returned from the database is 0, get the books
        # from the Google Books API
        if books.count() == 0:
            api_data = get_books(search_parameters, user_language.short_code)
            books = parse_book_data(api_data, user_language.id)
 
        serializer = self.serializer_class(data=books, many=True)
        serializer.is_valid()
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
