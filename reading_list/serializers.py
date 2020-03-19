from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
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
        validators = [
            UniqueTogetherValidator(
                queryset=ReadingList.objects.all(),
                fields=("user", "book")
            )
        ]
    
    def create(self, validated_data):
        self.is_valid(raise_exception=True)
        reading_list = super(AddToReadingListSerializer, self).create(validated_data)
        reading_list.save()
        return reading_list
        
