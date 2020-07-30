from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from library.models import LibraryBook
from library.serializers import LibrarySerializer, AddToLibrarySerializer
from books.models import Book
from reading_sessions.models import ReadingSession


class LibraryViewSet(viewsets.ModelViewSet):
    """LibraryViewSet

    Handles all of the interactions that users will have with their libraries and the
    individual library items. Users will use this endpoint to monitor and manage their
    libraries, including updating and deleting items.

    A user can get a list of library items, add books to their library, and update the
    finished date.

    This Viewset provides handlers for the following actions:
    - List all library items - GET
    - Create a library item - POST
    - Mark a an item as finished - PATCH
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LibrarySerializer
    write_serializer = AddToLibrarySerializer
    queryset = LibraryBook.objects.all()

    def list(self, request):
        """List the user's library

        Get a full list of the items that the user has in their library.

        Returns:
            LibrarySerializer (list): A list of library items
        
        Examples:
            This endpoint will be available at::

                /reading-list/

            In order to call this from cURL, use the following::

                curl -X POST -H 'Content-type: application/json' \\
                    -H 'Authorization: Token <your_token>' \\
                    http://127.0.0.1:8000/reading-list/
        
        Example response:
            The response data should look like (longer strings have been truncated for brevity)::

                [
                    {
                        "id": 1,
                        "book": {
                            "id": 7,
                            "title": "Harry Potter and International Relations",
                            "author": "['Daniel H. Nexon', 'Iver B. Neumann']",
                            "publisher": "Rowman & Littlefield",
                            "publish_date": "2020-07-30",
                            "description": "Drawing on a range of historical...",
                            "category": null,
                            "small_thumbnail": "http://books.google.com/books/content...",
                            "thumbnail": "http://books.google.com/books/content?...",
                            "language": 2
                        },
                        "readingsession_count": 1,
                        "finished_on": "2020-07-20T16:24:00Z",
                        "is_finished": false
                    }
                ]
        """
        library = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(library, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Add item to library

        Add a new book to a user's library
        """
        serializer = self.write_serializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            library_item = self.queryset.get(
                user=request.user, book_id=serializer.data["book"]
            )
            serializer = self.serializer_class(library_item)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors)

    def partial_update(self, request, pk):
        item = LibraryBook.objects.get(id=pk)
        serializer = self.serializer_class(item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors)
