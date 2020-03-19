from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    readingsession_set = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "publisher",
                  "publish_date", "description", "category",
                  "language", "small_thumbnail", "thumbnail",
                  "readingsession_set"]