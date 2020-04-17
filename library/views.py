from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from library.models import LibraryBooks
from library.serializers import (
    LibrarySerializer, AddToLibrarySerializer)
from books.models import Book
from reading_sessions.models import ReadingSession


class LibraryBooksView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        book_list = LibraryBooks.objects.filter(user=request.user)
        serializer = LibrarySerializer(book_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        book = Book.objects.get(id=request.data["book"])
        data = {
            "user": request.user.id,
            "book": book.id
        }
        serializer = AddToLibrarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            library_item = LibraryBooks.objects.get(user=request.user, book=book)
            serialized_item = LibrarySerializer(library_item)
            return Response(data=serialized_item.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors)
