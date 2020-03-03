from rest_framework import serializers
from reading_list.models import ReadingList
from accounts.models import UserProfile
from books.models import Book
from books.serializers import BookSerializer


class ReadingListSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = ReadingList
        fields = ["book"]


class AddToReadingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadingList
        fields = ["user", "book"]