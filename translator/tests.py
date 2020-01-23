"""
The test cases for the translator API. This test test suite should test
for the following test cases:

    - A user cannot retrieve translations if they are not logged in
    - A user cannot translate text if they are not logged in
    - A user can retrieve a list of the translations that they've
        created previously
    - A user can translate translate text from the language that they
        have chosen to learn, to their native language
    - A user will recieve an audio clip so they can hear how the original
        text is supposed to be pronounced
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from translator.models import Translation
from translator.aws_utils import bundle_aws_data
from translator.serializers import TranslationSerializer
from accounts.models import UserProfile
from languages.models import Language


class TranslatorTests(APITestCase):
    """
    The test cases for the translator API endpoint
    """

    def _create_user(self):
        url = reverse("register")
        data = {
            "username": "aaronsnig501",
            "email": "aaronsnig@gmail.com",
            "password": "testpassword",
            "first_language": 2,
            "language_being_learned": 1
        }
        self.client.post(url, data)
        
        return data["email"]
    
    def _create_translation(self, text, user):
        data = bundle_aws_data(text, user)
        translation = TranslationSerializer(data=data)
        if translation.is_valid():
            translation.save()

    def setUp(self):
        """
        The test cases for this endpoint will require some extra items.

        There will need to be languages present in the database, as well
        as some users so that we can test to ensure that users can only
        access these enpoints when their logged in, and we also need to
        test to ensure that the translations are associated with the correct
        user, etc
        """
        pt = Language(
            name="Brazilian Portuguese",
            code="pt-BR",
            short_code="pt",
            description="The language spoken in Brazil",
        )
        en = Language(
            name="English",
            code="en-GB",
            short_code="en",
            description="The language spoken in Ireland",
        )
        es = Language(
            name="Spanish",
            code="es",
            short_code="ens",
            description="The language spoken in Spain",
        )
        de = Language(
            name="German",
            code="de",
            short_code="de",
            description="The language spoken in Germany",
        )
        pt.save()
        en.save()
        es.save()
        de.save()

    def test_that_a_non_logged_in_user_cant_get_translations(self):
        """
        Ensure that unauthenticated users cannot retireve translations from
        the API
        """
        url = reverse("translate")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_that_a_non_logged_in_user_cant_create_translations(self):
        """
        Ensure that unauthenticated users cannot add translations via the
        translations API
        """
        url = reverse("translate")
        data = {
            "text_to_be_translated": "hello"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_can_retrieve_their_translations(self):
        """
        Test to ensure that a logged in user can retrieve a list of their
        translations
        """
        url = reverse("translate")
        user = UserProfile.objects.get(email=self._create_user())

        self._create_translation(
            "Esta é uma frase em português.", user)

        self.client.force_authenticate(user=user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_that_a_logged_in_user_can_create_translations(self):
        """
        Test to ensure that a user that is logged in can post to the
        translations endpoint
        """
        url = reverse("translate")
        data = {
            "text_to_be_translated": "Esta é uma frase em português."
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_that_the_source_text_is_correct(self):
        """
        Test that the API returns the correct source language for
        the logged in user
        """
        url = reverse("translate")
        data = {
            "text_to_be_translated": "Esta é uma frase em português."
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)

        self.assertEqual(
            response.data["source_text"],
            "Esta é uma frase em português.")

    def test_that_the_translated_text_is_correct(self):
        """
        Test that the correct response is given from the API after the
        text has been translated
        """
        url = reverse("translate")
        data = {
            "text_to_be_translated": "Esta é uma frase em português."
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)

        self.assertEqual(
            response.data["translated_text"],
            "This is a phrase in Portuguese.")
    
    def test_that_the_source_language_is_correct(self):
        """
        Ensure that the source language ID in the response is correct.
        This should match the ID of the language that the user is learning
        """
        url = reverse("translate")
        data = {
            "text_to_be_translated": "Esta é uma frase em português."
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)
        self.assertEqual(
            response.data["source_language"],
            user.language_being_learned.id)

    def test_that_the_target_language_is_correct(self):
        """
        Ensure that the target language ID in the response is correct.
        This should match the ID of the user's native language
        """
        url = reverse("translate")
        data = {
            "text_to_be_translated": "Esta é uma frase em português."
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)
        self.assertEqual(
            response.data["target_language"],
            user.first_language.id)

    def test_that_audio_clip_is_received(self):
        """
        Test to ensure that the audio clip of the text snippet is
        received
        """
        url = reverse("translate")
        data = {
            "text_to_be_translated": "Esta é uma frase em português."
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)

        self.assertIn("audio_file_path", response.data)
    
    def test_that_the_analysis_is_received(self):
        """
        Test to ensure that the text anaylses of the text snippet is
        received
        """
        url = reverse("translate")
        data = {
            "text_to_be_translated": "Esta é uma frase em português."
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)
        self.assertIn("analysis", response.data)
