"""
This section of functionality is difficult to test as the information comes
from the Google Books API, however I should still be able to test:

    - A request can be made to the endpoint
    - An appropriate error message will be returned if the API requirements
        aren't met
    - An error is thrown if the request isn't authenticated
    - The Google Books will not be called if the data already exists within
        Decyphr
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book
from accounts.models import UserProfile
from languages.models import Language


class BooksTests(APITestCase):
    """The test cases for the book API
    """
    fixtures = ['fixtures.json']

    def test_a_client_cant_access_the_endpoint_without_a_token(self):
        """Unauthorized usage

        A client that tries to access the books endpoint recieves a 401 if they
        don't provide a token
        """
        url = reverse("books-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_a_client_can_access_the_endpoint_with_a_token(self):
        """Authorized usage

        An authorized client will be able to access the endpoint
        """
        url = reverse("books-list")
        user = UserProfile.objects.first()

        self.client.force_authenticate(user=user)

        response = self.client.get(url, {"name": "harry"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
