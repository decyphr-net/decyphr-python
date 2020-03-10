from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from translator.aws_utils import bundle_aws_data
from translator.models import Translation
from translator.serializers import IncomingSerializer
from translator.serializers import TranslationSerializer
from translator.pagination import BasicPagination
from translator.pagination import PaginationHandlerMixin
from accounts.models import UserProfile


class TranslatorView(APIView, PaginationHandlerMixin):
    """
    The main view surround the translation API
    """

    permission_classes = (IsAuthenticated,)
    pagination_class = BasicPagination

    def get_object(self, pk):
        """
        A simple helper method to retrieve an individual item from
        the database based on the ID, or raise a 404 error
        """
        try:
            return Translation.objects.get(pk=pk)
        except Translation.DoesNotExist:
            raise Http404

    def get(self, request):
        """
        Get the entire list of the current user's translations
        """
        translations = Translation.objects.filter(
            user=request.user).order_by('created_on')

        page = self.paginate_queryset(translations)
        if page is not None:
            serializer = self.get_paginated_response(
                TranslationSerializer(page, many=True).data)
        else:
            serializer = TranslationSerializer(translations, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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
            new_data = bundle_aws_data(
                serializer.data["text_to_be_translated"], request.user
            )

            # Create a new `TranslationSerializer` from this new data
            translation = TranslationSerializer(data=new_data)

            # If it's valid, save it to the database and return with a
            # successful status
            if translation.is_valid():
                translation.save()
                return Response(translation.data, status=status.HTTP_201_CREATED)

            # If there was an issue validating the `translation` then
            # return a bad request and a status of 400
            return Response(translation.errors, status=status.HTTP_400_BAD_REQUEST)

        # If there was an issue validating the `serializer` then
        # return a bad request and a status of 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Delete a translation from the database
        """
        translation = self.get_object(pk)
        translation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)