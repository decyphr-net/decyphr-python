from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from accounts.models import UserProfile
from languages.models import Language


class AccountTests(APITestCase):
    """
    Test cases for the `accounts` app.

    This app should cover the following cases:
        - Creating a new user account
        - Getting an access token after creating a new account
        - Getting a user's details
        - Log in
        - Retrieving users profiles
        - Updating a user's profile
        - Deleting a user
    """

    def setUp(self):
        """
        In order to create new user accounts, we need to create
        language defaults to associate with the user objects
        """
        # Test languages
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
        pt.save()
        en.save()

        # Test user details
        self.email = "aaronsnig@gmail.com"
        self.username = "aaronsnig501"
        self.password = "testpassword"

        self.user_details_as_dict = {
            "email": self.email,
            "username": self.username,
            "password": self.password,
        }

        # Test URL endpoints
        self.create_account = reverse("create-account")
        self.get_account = reverse("get-account")

    def test_create_account(self):
        """
        Calling the `create-account` URL will create a new user in
        the database
        """
        response = self.client.post(
            self.create_account, self.user_details_as_dict, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().username, "aaronsnig501")

    def test_token_retrival_for_new_account(self):
        """
        Calling the `create-account` URL will create a new user in
        the database and return a token to the new user
        """
        response = self.client.post(
            self.create_account, self.user_details_as_dict, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_get_account(self):
        """
        Calling the `get-account` URL will return the details of the
        currently logged in user
        """
        user = UserProfile(
            email=self.email, username=self.username, password=self.password
        )
        user.save()
        self.client.force_authenticate(user)

        response = self.client.get(self.get_account, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.email)
        self.assertEqual(response.data["username"], self.username)
