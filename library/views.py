from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from library.models import LibraryBook
from library.serializers import (
    LibrarySerializer, AddToLibrarySerializer)
from books.models import Book
from reading_sessions.models import ReadingSession


class LibraryViewSet(viewsets.ModelViewSet):
    """LibraryViewSet

    Handles all of the interactions that users will have with their libraries.
    Users will use this endpoint to monitor and manage their libraries,
    including updating and deleting items
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LibrarySerializer
    write_serializer = AddToLibrarySerializer
    queryset = LibraryBook.objects.all()

    def list(self, request):
        """List the user's library

        Get a full list of all of the items that the user has in their library
        """
        library = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(library, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Add item to library

        Add a new book to a user's library
        """
        serializer = self.write_serializer(
            data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            library_item = self.queryset.get(
                user=request.user, book_id=serializer.data["book"])
            serializer = self.serializer_class(library_item)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors)
