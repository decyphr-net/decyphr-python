from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Question, Session
from .serializers import QuestionSerializer, SessionSerializer


class PracticeQuestionView(APIView):

    serializer_class = QuestionSerializer

    def get(self, request, pk=None):
        questions = Question.objects.all()
        serializer = self.serializer_class(questions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PracticeSessionView(APIView):

    serializer_class = SessionSerializer

    def get(self, request, pk=None):
        sessions = Session.objects.all()
        serializer = self.serializer_class(sessions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
