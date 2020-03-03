from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reading_list.models import ReadingList
from reading_list.serializers import (
    ReadingListSerializer, AddToReadingListSerializer)
from books.models import Book


class ReadingListView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        book_list = ReadingList.objects.filter(user=request.user)
        serializer = ReadingListSerializer(book_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {
            "user": request.user.id,
            "book": int(request.data["book"])
        }
        serializer = AddToReadingListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors)
