from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reading_sessions.models import ReadingSession
from reading_sessions.serializers import (
    CreateReadingSessionSerializer, ReadingSessionSerializer)


class ReadingSessionView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ReadingSessionSerializer

    def get(self, request, pk=None):
        if pk:
            session = ReadingSession.objects.get(id=pk)
            serializer = self.serializer_class(session)
        else:
            sessions = ReadingSession.objects.filter(user=request.user)
            serializer = self.serializer_class(sessions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        incoming_data = request.data
        incoming_data["user"] = request.user.id
        create_serializer = CreateReadingSessionSerializer(data=incoming_data)

        if create_serializer.is_valid():
            
            model = create_serializer.save()
            data = {
                "user": model.user.id,
                "library_item": model.library_item,
                "duration": model.duration,
                "pages": model.pages,
                "translation_set": model.translation_set.all(),
                "id": model.id
            }
            return_serializer = self.serializer_class(data=data)
            return_serializer.is_valid()

            return Response(return_serializer.data)
        else:
            return Response(create_serializer.errors)
    
    def put(self, request, pk):
        session = ReadingSession.objects.get(id=pk)
        session.pages = request.data["number_of_pages"]
        session.save()
        return Response({"message": "Successfully updated"}, status=status.HTTP_200_OK)