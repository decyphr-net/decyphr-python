from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import DashboardSerializer
from translator.models import Translation
from practice.models import Session
from reading_sessions.models import ReadingSession
from library.models import LibraryBook


class Dashboard(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = DashboardSerializer

    def get(self, request):
        user = request.user
        translations = Translation.objects.filter(user=user)
        library_items = LibraryBook.objects.filter(user=user)
        practice_sessions_count = Session.objects.filter(
            user=user).count()
        reading_session_count = ReadingSession.objects.filter(
            library_item__user=user).count()

        data = {
            "library_item_count": library_items.count(),
            "translations_count": translations.count(),
            "practice_sessions_count": practice_sessions_count,
            "reading_sessions_count": reading_session_count
        }

        serializer = self.serializer_class(data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)