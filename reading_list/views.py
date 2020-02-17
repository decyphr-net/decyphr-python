from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reading_list.models import ReadingList
from reading_list.serializers import ReadingListSerializer
from books.models import Book


class ReadingListView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ReadingListSerializer

    def get(self, request):
        book_list = ReadingList.objects.filter(user=request.user)
        serializer = self.serializer_class(book_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {
            "user": request.user.id,
            "book": Book.objects.get(id=int(request.data["book"])).id
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
