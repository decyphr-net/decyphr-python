from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import UserProfile
from languages.models import Language


class AccountsTests(APITestCase):

    def setUp(self):
        """
        In order to create new user accounts, we need to create
        language defaults to associate with the user objects
        """
        # Test languages
        pt = Language(
            name='Brazilian Portuguese',
            code='pt-BR', short_code='pt',
            description='The language spoken in Brazil')
        en = Language(
            name='English', code='en-GB', short_code='en',
            description='The language spoken in Ireland')
        es = Language(
            name='Spanish', code='es', short_code='ens',
            description='The language spoken in Spain')
        de = Language(
            name='German', code='de', short_code='de',
            description='The language spoken in Germany'
        )
        pt.save()
        en.save()
        es.save()
        de.save()

        # Test user details
        self.email = 'aaronsnig@gmail.com'
        self.username = 'aaronsnig501'
        self.password = 'testpassword'
        self.first_name = 'Aaron'
        self.last_name = 'Sinnott'

        self.user_details_as_dict = {
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'first_language': 1,
            'language_being_learned': 2
        }

    def test_registration(self):
        """
        Test that a new user can be registered
        """
        url = reverse('register')
        data = self.user_details_as_dict

        data.update({})

        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(
            UserProfile.objects.get().email, 'aaronsnig@gmail.com')
    
    def test_user_can_choose_languages_upon_registration(self):
        """
        Ensure that a user can select their native language, and the
        language that they're trying to learn
        """
        url = reverse('register')
        data = self.user_details_as_dict

        data.update({'first_language': 3, 'language_being_learned': 4})

        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            UserProfile.objects.get().first_language.name, 'Spanish')
        self.assertEqual(
            UserProfile.objects.get().language_being_learned.name, 'German')