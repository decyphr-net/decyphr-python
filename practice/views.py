import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Question, Session
from .serializers import QuestionSerializer, SessionSerializer
from translator.models import Translation
from translator.serializers import TranslationSerializer


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
    
    def post(self, request):
        session = Session(user=request.user)
        session.save()
        translations = Translation.objects.filter(user=request.user)
        random_translations = random.sample(list(translations), 5)
        for translation in random_translations:
            question = Question(translation=translation, session=session)
            question.save()
        
        serializer = SessionSerializer(session)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
