import requests
from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from languages.models import Language
from books.models import Book
from books.serializers import BookSerializer
from books.google_utils import get_books, parse_book_data


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
                book_dict = parse_book_data(book, lang)

                try:
                    new_book, created = Book.objects.get_or_create(
                        title__icontains=book_dict["title"], defaults=book_dict)
                except Book.MultipleObjectsReturned:
                    continue
                except TypeError:
                    continue
                except ValidationError:
                    continue
        books = self.serializer_class(
            Book.objects.filter(title__icontains=book_name), many=True)
        return Response(books.data)
