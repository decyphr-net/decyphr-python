from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reading_sessions.models import ReadingSession
from reading_sessions.serializers import ReadingSessionSerializer


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
        serializer = self.serializer_class(data=incoming_data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)