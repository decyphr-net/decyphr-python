from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translator.aws_utils import bundle_aws_data
from translator.models import Translation
from translator.serializers import IncomingSerializer
from translator.serializers import TranslationSerializer
from accounts.models import UserProfile


class TranslatorView(APIView):
    """
    The main view surround the translation API
    """
    def get(self, request):
        translations = Translation.objects.all()
        serializer = TranslationSerializer(translations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        This post method will perform a couple of tasks.

        1. It will retrieve and de-serialize the incoming JSON data
        2. It will use this data to retrieve the translation and the
           location to the audio from AWS
        3. It will take the information from the API and use it to
           create a new record in the `Translation` table so that
           a user can retrieve the translation again at a later time
        """
        # Grab the incoming data and use it to instansiate the
        # serializer
        serializer = IncomingSerializer(data=request.data)

        # If the data coming in from the request is valid
        if serializer.is_valid():
            # Generate the data from AWS
            user = UserProfile.objects.get(
                pk=serializer.data["user_id"])
            new_data = bundle_aws_data(
                serializer.data["text_to_be_translated"], user)

            # Create a new `TranslationSerializer` from this new data
            translation = TranslationSerializer(data=new_data)

            # If it's valid, save it to the database and return with a
            # successful status
            if translation.is_valid():
                translation.save()
                return Response(
                    translation.data, status=status.HTTP_201_CREATED)

            # If there was an issue validating the `translation` then
            # return a bad request and a status of 400
            return Response(
                translation.errors, status=status.HTTP_400_BAD_REQUEST)

        # If there was an issue validating the `serializer` then
        # return a bad request and a status of 400
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
