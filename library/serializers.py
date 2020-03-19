from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from library.models import LibraryBooks
from accounts.models import UserProfile
from books.models import Book
from books.serializers import BookSerializer
from reading_sessions.models import ReadingSession
from reading_sessions.serializers import ReadingSessionSerializer


class LibrarySerializer(serializers.ModelSerializer):

    book = BookSerializer()
    readingsession_set = serializers.SerializerMethodField()
    
    def get_readingsession_set(self, obj):
        reading_sessions = ReadingSession.objects.filter(
            user=self.context["request"].user)
        serializer = ReadingSessionSerializer(reading_sessions, many=True)
        return serializer.data

    class Meta:
        model = LibraryBooks
        fields = ["book", "readingsession_set"]


class AddToLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryBooks
        fields = ["user", "book"]
        validators = [
            UniqueTogetherValidator(
                queryset=LibraryBooks.objects.all(),
                fields=("user", "book")
            )
        ]
    
    def create(self, validated_data):
        self.is_valid(raise_exception=True)
        library_book = super(AddToLibrarySerializer, self).create(validated_data)
        library_book.save()
        return library_book
        
