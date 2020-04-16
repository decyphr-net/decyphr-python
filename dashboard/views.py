from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import DashboardSerializer
from translator.models import Translation
from practice.models import Session
from reading_sessions.models import ReadingSession
from library.models import LibraryBooks


class Dashboard(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = DashboardSerializer

    def get(self, request):
        user = request.user
        translations = Translation.objects.filter(user=user)
        practice_sessions = Session.objects.filter(user=user)
        reading_sessions = ReadingSession.objects.filter(user=user)
        library_items = LibraryBooks.objects.filter(user=user)

        data = {
            "translations": translations,
            "library_items": library_items,
            "practice_sessions": practice_sessions,
            "reading_sessions": reading_sessions
        }

        serializer = self.serializer_class(data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)