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
from django.utils import timezone
import pytz
from rest_framework import status
from rest_framework.test import APITestCase
from translator.models import Translation
from translator.aws_utils import (
    bundle_aws_data, _generate_audio_file, _translate_text)
from translator.serializers import TranslationSerializer
from accounts.models import UserProfile
from languages.models import Language
from books.models import Book
from library.models import LibraryBook
from reading_sessions.models import ReadingSession


class TranslatorTests(APITestCase):
    """
    The test cases for the translator API endpoint
    """
    fixtures = ['fixtures.json']
    
    def _create_reading_session(self):
        """
        A helper method that will create a new `readingsession` so that
        a translation can be tied to a session object. It begins by creating
        a new book object that is required for the reading session
        """
        date = datetime(2013, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)
        book = Book(
            title="Harry Potter", author="JK Rowling", publisher="hello",
            publish_date=date,
            language=Language.objects.get(name="Brazilian Portuguese"))
        book.save()

        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        library_item = LibraryBook(user=user, book=book)
        library_item.save()

        reading_session = ReadingSession(
            user=user,
            library_item=library_item, duration=timedelta(microseconds=-1), pages=2.5)
        reading_session.save()
        return reading_session

    def _create_translation(self, text, user):
        """
        A helper method used to create translations for the tests
        """
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

    def test_that_a_non_logged_in_user_cant_get_translations(self):
        """
        Ensure that unauthenticated users cannot retireve translations from
        the API
        """
        url = reverse("translate-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_that_a_non_logged_in_user_cant_create_translations(self):
        """
        Ensure that unauthenticated users cannot add translations via the
        translations API
        """
        url = reverse("translate-list")

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
        url = reverse("translate-list")
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")

        self._create_translation(
            "Esta é uma frase em português.", user)

        self.client.force_authenticate(user=user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_a_logged_in_user_can_create_translations(self):
        """
        Test to ensure that a user that is logged in can post to the
        translations endpoint
        """
        url = reverse("translate-list")
        

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        self.client.force_authenticate(user=user)
        self._create_reading_session()

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_that_the_translation_contains_an_id(self):
        """
        Ensure that the translation contains an ID property
        """
        url = reverse("translate-list")
        

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        self.client.force_authenticate(user=user)
        self._create_reading_session()

        response = self.client.post(url, data)
        self.assertIn("id", response.data)

    def test_that_the_source_text_is_correct(self):
        """
        Test that the API returns the correct source language for
        the logged in user
        """
        url = reverse("translate-list")
        self._create_reading_session()

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
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
        url = reverse("translate-list")

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        self.client.force_authenticate(user=user)
        self._create_reading_session()

        response = self.client.post(url, data)

        self.assertEqual(
            response.data["translated_text"],
            "This is a phrase in Portuguese.")

    def test_that_the_source_language_is_correct(self):
        """
        Ensure that the source language ID in the response is correct.
        This should match the ID of the language that the user is learning
        """
        url = reverse("translate-list")
        

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        self.client.force_authenticate(user=user)
        self._create_reading_session()

        response = self.client.post(url, data)
        self.assertEqual(
            response.data["source_language"],
            user.language_being_learned.id)

    def test_that_the_target_language_is_correct(self):
        """
        Ensure that the target language ID in the response is correct.
        This should match the ID of the user's native language
        """
        url = reverse("translate-list")

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        self.client.force_authenticate(user=user)
        self._create_reading_session()

        response = self.client.post(url, data)
        self.assertEqual(
            response.data["target_language"],
            user.first_language.id)

    def test_that_audio_clip_is_received(self):
        """
        Test to ensure that the audio clip of the text snippet is
        received
        """
        url = reverse("translate-list")

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        self.client.force_authenticate(user=user)
        self._create_reading_session()

        response = self.client.post(url, data)

        self.assertIn("audio_file_path", response.data)

    def test_that_the_analysis_is_received(self):
        """
        Test to ensure that the text anaylsis of the text snippet is
        received
        """
        url = reverse("translate-list")

        data = {
            "text_to_be_translated": "Esta é uma frase em português.",
            "session": 1
        }
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        self.client.force_authenticate(user=user)
        self._create_reading_session()

        response = self.client.post(url, data)
        self.assertIn("analysis", response.data)

    def test_to_ensure_that_an_item_can_be_deleted(self):
        """
        Test to ensure that the a translation can be deleted
        """
        url = reverse("translate-detail", args=(1,))
        
        user = UserProfile.objects.get(email="aaronsnig@gmail.com")
        self.client.force_authenticate(user=user)
        self._create_reading_session()

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
        self.assertEqual(translation, "I'm hungry")

    # TODO: Create a test to ensure the correct ordering
    # TODO: Create tests for the `pagination` functionality
    # TODO: Create tests for the `analysis` functionality
    # TODO: Finish tests for the `aws_utils` functions
