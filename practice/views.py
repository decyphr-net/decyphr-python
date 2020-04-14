import random
from datetime import datetime
from datetime import timedelta
from fuzzywuzzy import fuzz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Question, Session
from .serializers import QuestionSerializer, SessionSerializer
from translator.models import Translation
from translator.serializers import TranslationSerializer


class PracticeQuestionView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    def get(self, request, pk=None):
        if pk:
            question = Question.objects.get(id=pk)
            serializer = self.serializer_class(question)
        else:
            questions = Question.objects.all()
            serializer = self.serializer_class(questions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        question = Question.objects.get(id=pk)
        
        users_guess = request.data["guess"]
        correct_answer = question.translation.translated_text

        ratio = fuzz.ratio(users_guess, correct_answer)
        
        question.answer_provided
        
        if ratio >= 85:
            question.correct = True
        
        question.save()
        serializer = self.serializer_class(question)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PracticeSessionView(APIView):

    permission_classes = (IsAuthenticated,)
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
    
    def put(self, request, pk):
        session = Session.objects.get(id=pk)
        duration_items = [int(date_item) for date_item in request.data["duration"].split(':')]
        session.duration = timedelta(
            hours=duration_items[0],
            minutes=duration_items[1],
            seconds=duration_items[2]
        )

        total_number_of_questions = session.question_set.all().count()
        correct_questions = session.question_set.filter(correct=True).count()

        percentage = 100 * correct_questions / total_number_of_questions

        session.score = percentage
        session.save()
        serializer = SessionSerializer(session)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
