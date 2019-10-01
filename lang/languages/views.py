from rest_framework.views import APIView
from rest_framework.response import Response
from languages.models import Language
from languages.serializers import LanguageSerializer


class LanguageView(APIView):

    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)
