import requests
from django.shortcuts import render
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from languages.models import Language
from books.models import Book
from books.serializers import BookSerializer
from books.google_utils import get_books


class BookAPIView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer
    search_fields = ["title"]
    filter_backends = (filters.SearchFilter,)
    queryset = Book.objects.all()

    def get(self, request):
        lang = request.user.language_being_learned.short_code
        book_name = request.query_params["name"]

        book_list = get_books(book_name, lang)

        if book_list:
            for book in book_list:
                try:
                    book_dict = {
                        "title": book["volumeInfo"]["title"],
                        "author": [author for author in book["volumeInfo"]["authors"]],
                        "language": Language.objects.get(short_code=lang),
                    }
                except KeyError:
                    pass

                try:
                    new_book, created = Book.objects.get_or_create(
                        title__icontains=book["volumeInfo"]["title"], defaults=book_dict)
                except Book.MultipleObjectsReturned:
                    pass
        books = self.serializer_class(
            Book.objects.filter(title__icontains=book_name), many=True)
        return Response(books.data)
