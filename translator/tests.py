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
from datetime import datetime
from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from translator.models import Translation
from translator.aws_utils import (
    bundle_aws_data, _generate_audio_file, _translate_text)
from translator.serializers import TranslationSerializer
from accounts.models import UserProfile
from languages.models import Language
from books.models import Book
from reading_sessions.models import ReadingSession


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
    
    def _create_reading_session(self):
        book = Book(
            title="Harry Potter", author="JK Rowling", publisher="hello",
            language=Language.objects.get(name="Brazilian Portuguese"))
        book.save()

        reading_session = ReadingSession(
            user=UserProfile.objects.get(email=self._create_user()),
            book=book, duration=timedelta(microseconds=-1), pages=2.5)
        reading_session.save()
        return reading_session

    def _create_translation(self, text, user):
        data = bundle_aws_data(text, user)

        source_language = user.language_being_learned
        target_language = user.first_language
        session = self._create_reading_session()

        translation = Translation(
            user=user, source_text=data["source_text"],
            translated_text=data["translated_text"],
            audio_file_path=data["audio_file_path"],
            source_language=source_language,
            target_language=target_language,
            session=session)
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
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
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
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_that_the_translation_contains_an_id(self):
        """
        Ensure that the translation contains an ID property
        """
        url = reverse("translate")
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)
        self.assertIn("id", response.data)

    def test_that_the_source_text_is_correct(self):
        """
        Test that the API returns the correct source language for
        the logged in user
        """
        url = reverse("translate")
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
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
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
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
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
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
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
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
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)

        self.assertIn("audio_file_path", response.data)

    def test_that_the_analysis_is_received(self):
        """
        Test to ensure that the text anaylsis of the text snippet is
        received
        """
        url = reverse("translate")
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data)
        self.assertIn("analysis", response.data)

    def test_to_ensure_that_an_item_can_be_deleted(self):
        """
        Test to ensure that the a translation can be deleted
        """
        url = reverse("translate-id", args=(1,))
        self._create_reading_session()
        
        user = UserProfile.objects.get(email=self._create_user())
        self.client.force_authenticate(user=user)

        self._create_translation("Esta é uma frase em português.", user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_that_the_audio_file_is_generated_correctly(self):
        """
        Test to ensure that the audio file is generated and that the URL
        provided contains the bucket name and the correct `.mp3` extension
        """
        language = Language.objects.get(name="Brazilian Portuguese")
        file_path = _generate_audio_file("Eu estou com fome", language)
        self.assertIn("https://s3.eu-west-1.amazonaws.com/langappaaron/", file_path)
        self.assertIn(".mp3", file_path)
    
    def test_that_the_text_is_contains_the_correct_translation(self):
        """
        Test that the correct translation comes back from AWS Translate
        """
        text = "Eu estou com fome"
        first_language = Language.objects.get(name="English")
        new_language = Language.objects.get(name="Brazilian Portuguese")
        translation = _translate_text(
            text, first_language, new_language)
        self.assertEqual(translation, "I am hungry.")

    # TODO: Create a test to ensure the correct ordering
    # TODO: Create tests for the `pagination` functionality
    # TODO: Create tests for the `analysis` functionality
    # TODO: Finish tests for the `aws_utils` functions
