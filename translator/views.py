from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from translator.models import Translation
from translator.serializers import IncomingSerializer
from translator.serializers import TranslationSerializer
from .utils import translate_text


class TranslationViewSet(viewsets.ModelViewSet):

    queryset = Translation.objects.all()
    permission_classes = (IsAuthenticated,)
    write_serializer = IncomingSerializer
    serializer_class = TranslationSerializer

    def get_object(self, pk):
        """Get object

        A simple helper method to retrieve an individual item from the database
        based on the ID, or raise a 404 error.

        Args:
            pk (int): The primary key of the object being looked up
        
        Returns:
            Translation: The translation object that matches the primary key
        
        Raises:
            Http404 is the object doesn't exist in the database
        
        Examples:
            Can be called with the following::

                def destroy(self, request, pk):
                    translation = self.get_object(pk)
        """
        try:
            return Translation.objects.get(pk=pk)
        except Translation.DoesNotExist:
            raise Http404

    def bundle_new_data(self, data, user):
        """Bundle Data
        
        A helper method to bundle up the call to the Translation service and
        generate a new serializer instance based on the information from the
        API.

        Args:
            data (IncomingSerializer): A validated instance of IncomingSerializer
            user (UserProfile): The user that the information will relate to
        
        Returns:
            TranslationSerializer: The TranslationSerializer generated from the API data
        
        Examples:
            Can be called with the following::
            
                serializer = self.write_serializer(data=request.data)

                if serializer.is_valid():
                    translation = self.bundle_new_data(serializer.data, request.user)
        """
        translation = translate_text(
            data["text_to_be_translated"],
            user.language_being_learned.short_code,
            user.first_language.code,
        )

        translation_data = {
            "source_text": data["text_to_be_translated"],
            "translated_text": translation["translated_text"],
            "audio_file_path": translation["audio_location"],
            "source_language": user.language_being_learned.id,
            "target_language": user.first_language.id,
            "user": user.id,
            "session": data["session"],
        }
        return self.serializer_class(data=translation_data)

    def create(self, request):
        """
        Create a new translation based on the incoming text. The incoming
        serializer will provide the text to be translated and the ID of the
        session that the text belongs to.

        This will then be translated and analysed by Google, with a audio clip
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
            user=user, session__id=session_id
        ).order_by("-created_on")

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
