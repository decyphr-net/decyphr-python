from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Question
from .serializers import QuestionSerializer


class PracticeQuestionView(APIView):

    serializer_class = QuestionSerializer

    def get(self, request, pk=None):
        questions = Question.objects.all
        serializer = QuestionSerializer(questions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
