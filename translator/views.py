from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from translator.aws_utils import bundle_aws_data
from translator.models import Translation
from translator.serializers import IncomingSerializer
from translator.serializers import TranslationSerializer


class TranslationViewSet(viewsets.ModelViewSet):

    queryset = Translation.objects.all()
    permission_classes = (IsAuthenticated,)
    write_serializer = IncomingSerializer
    serializer_class = TranslationSerializer

    def get_object(self, pk):
        """
        A simple helper method to retrieve an individual item from
        the database based on the ID, or raise a 404 error
        """
        try:
            return Translation.objects.get(pk=pk)
        except Translation.DoesNotExist:
            raise Http404
    
    def bundle_new_data(self, data, user):
        """
        Bundle up the calls to AWS and the population of the new new serializer
        """
        new_data = bundle_aws_data(data["text_to_be_translated"], user)
        new_data["session"] = data["session"]
        return self.serializer_class(data=new_data)
    
    def create(self, request):
        """
        Create a new translation based on the incoming text. The incoming
        serializer will provide the text to be translated and the ID of the
        session that the text belongs to.

        This will then be translated and analysed by AWS, with a audio clip
        which will be contained in the outgoing serializer.
        """
        serializer = self.write_serializer(data=request.data)

        if serializer.is_valid():
            translation = self.bundle_new_data(serializer.data, request.user)
            translation.is_valid()
            translation.save()
            return Response(translation.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """
        Retrieve the list of translations specific to that user's current
        reading session and paginate the results
        """
        user = request.user
        session_id = request.GET.get("sessionId")
        session_translations = self.queryset.filter(
            user=user, session__id=session_id).order_by('-created_on')
        
        page = self.paginate_queryset(session_translations)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(session_translations, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        """
        Delete a translation from the database
        """
        translation = self.get_object(pk)
        translation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
