from rest_framework import serializers
from reading_list.models import ReadingList


class ReadingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadingList
        fields = ["user", "book"]