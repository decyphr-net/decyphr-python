from rest_framework import serializers
from reading_list.models import ReadingList


class ReadingListSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = ReadingList
        depth = 1
        fields = ["user", "book"]