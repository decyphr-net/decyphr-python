from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from library.models import LibraryBook
from accounts.models import UserProfile
from books.models import Book
from books.serializers import BookSerializer
from reading_sessions.models import ReadingSession


class LibrarySessionSerializer(serializers.ModelSerializer):

    book = BookSerializer()

    class Meta:
        model = LibraryBook
        fields = ["id", "book"]


class LibrarySerializer(serializers.ModelSerializer):

    book = BookSerializer()
    readingsession_count = serializers.SerializerMethodField()
    
    def get_readingsession_count(self, obj):
        return obj.readingsession_set.all().count()

    class Meta:
        model = LibraryBook
        fields = ["id", "book", "readingsession_count"]


class AddToLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryBook
        fields = ["user", "book"]
        validators = [
            UniqueTogetherValidator(
                queryset=LibraryBook.objects.all(),
                fields=("user", "book")
            )
        ]
    
    def create(self, validated_data):
        self.is_valid(raise_exception=True)
        library_book = super(AddToLibrarySerializer, self).create(validated_data)
        library_book.save()
        return library_book
        
