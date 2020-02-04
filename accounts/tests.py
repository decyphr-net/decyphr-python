from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from accounts.models import UserProfile
from languages.models import Language


class AccountsTests(APITestCase):
    """
    The test cases for the accounts API endpoint
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

        # Test user details
        self.email = "aaronsnig@gmail.com"
        self.username = "aaronsnig501"
        self.password = "testpassword"
        self.first_name = "Aaron"
        self.last_name = "Sinnott"

        self.user_details_as_dict = {
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "first_language": 1,
            "language_being_learned": 2,
        }

    def _do_registration(self):
        """
        A convenience function that is used when tests require a new
        user to be created
        """
        url = reverse("register")
        data = self.user_details_as_dict

        response = self.client.post(url, data, format="json")

    def test_registration(self):
        """
        Test that a new user can be registered
        """
        url = reverse("register")
        data = self.user_details_as_dict

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().email, "aaronsnig@gmail.com")

    def test_that_error_is_thrown_if_the_username_is_not_unique(self):
        """
        Ensure that a user cannot register with a username that has
        already been registered on the app
        """
        url = reverse("register")
        data = self.user_details_as_dict

        # Update the email address so we don't run into conflicts with
        # other validators
        data["email"] = "aaron@example.com"

        # Create first user so that we already have a user with this
        # username in the database
        self._do_registration()

        # Create the second user with this username
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["username"][0], "A user with that username already exists."
        )

    def test_that_error_is_thrown_if_email_is_not_unique(self):
        """
        A user should not be able to register with an email address
        that already exists in the database
        """
        url = reverse("register")
        data = self.user_details_as_dict

        # Update the username so we don't run into conflicts with
        # other validators
        data["username"] = "aaron"

        # Create first user so that we already have a user with this
        # email in the database
        self._do_registration()

        # Create the second user with this email
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "This field must be unique.")

    def test_that_error_is_thrown_if_password_is_not_present(self):
        """
        A user should not be able to register if they don't provide a
        password for their account
        """
        url = reverse("register")
        data = self.user_details_as_dict

        data["password"] = ""

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0], "This field may not be blank.")

    def test_that_error_is_thrown_if_first_language_is_not_present(self):
        """
        An error should be thrown if a user doesn't provide their first
        language
        """
        url = reverse("register")
        data = self.user_details_as_dict

        data["first_language"] = ""

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["first_language"][0], "This field may not be null."
        )

    def test_that_error_is_thrown_if_second_language_is_not_present(self):
        """
        An error should be thrown if a user doesn't provide the
        language it is that they're trying to learn
        """
        url = reverse("register")
        data = self.user_details_as_dict

        data["language_being_learned"] = ""

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["language_being_learned"][0], "This field may not be null."
        )

    def test_that_error_is_thrown_if_languages_are_equal(self):
        """
        A user shouldn't be able to choose the same first and second
        language. For example, if a user's native language is English,
        then they shouldn't be able to choose that as the language
        they're learning
        """
        url = reverse("register")
        data = self.user_details_as_dict

        data["language_being_learned"] = 1

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "You cannot learn a language that is the same as your native language.",
        )

    def test_user_can_choose_languages_upon_registration(self):
        """
        Ensure that a user can select their native language, and the
        language that they're trying to learn
        """
        url = reverse("register")
        data = self.user_details_as_dict

        data.update({"first_language": 3, "language_being_learned": 4})

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.get().first_language.name, "Spanish")
        self.assertEqual(
            UserProfile.objects.get().language_being_learned.name, "German"
        )
    
    def test_that_token_is_created_for_user_upon_registration(self):
        """
        Ensure that a new token is generated for a user when they
        register as a new user on the site
        """
        url = reverse("register")
        data = self.user_details_as_dict

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIsNotNone(
            Token.objects.get(
                user__email=self.user_details_as_dict["email"]))

    def test_that_a_registered_user_can_get_a_token(self):
        """
        Ensure that once a user has registered, they can get access to an
        authentication token
        """
        registration_url = reverse("register")
        auth_token_url = reverse("api_token_auth")

        registration_data = self.user_details_as_dict
        login_data = {"username": self.username, "password": self.password}

        registration_response = self.client.post(
            registration_url, registration_data, format="json"
        )

        self.assertEqual(registration_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(auth_token_url, login_data, format="json")

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.data)
    
    def test_that_a_user_can_log_in_with_an_email(self):
        """
        Test that a user can log in and get a token with an email
        """
        url = reverse("api_token_auth")
        data = {"username": self.email, "password": self.password}
        
        self._do_registration()

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
    
    def test_that_correct_error_is_thrown_if_the_username_field_is_empty(self):
        """
        Test that the correct error message is returned if a username
        string is empty
        """
        url = reverse("api_token_auth")
        data = {"username": "", "password": self.password}
        
        self._do_registration()

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["username"][0], "Please enter a username")

    def test_that_correct_error_is_thrown_if_no_username_is_provided(self):
        """
        Test that the correct error message is returned if a username
        property is not provided in the incoming data
        """
        url = reverse("api_token_auth")
        data = {"password": self.password}
        
        self._do_registration()

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["username"][0], "Username is required")
    
    def test_that_correct_error_is_thrown_if_the_password_field_is_empty(self):
        """
        Test that the correct error message is returned if a username
        string is empty
        """
        url = reverse("api_token_auth")
        data = {"username": "aaronsing501", "password": ""}
        
        self._do_registration()

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0], "Please enter a password")

    def test_that_correct_error_is_thrown_if_no_password_is_provided(self):
        """
        Test that the correct error message is returned if a password
        property is not provided in the incoming data
        """
        url = reverse("api_token_auth")
        data = {"username": self.username}
        
        self._do_registration()

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0], "Password is required")

    def test_unregistered_users_cannot_get_tokens(self):
        """
        Ensure that a user that doesn't exist within the 
        cannot be granted access to receive an auth token
        """
        url = reverse("api_token_auth")
        data = {"username": "notindatabaseusername", "password": "noneexistentpassword"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            "This user wasn't found. Please try again"
        )

    def test_that_a_user_can_retrieve_their_profile(self):
        """
        Ensure that a user can retrieve their profile when an
        auth token is provided
        """
        url = reverse("profile")
        self._do_registration()

        user = UserProfile.objects.get(email=self.email)
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_profile_is_retrieved_for_user(self):
        """
        Test to ensure that the correct profile is returned for a user
        when they request the profile URL
        """
        url = reverse("profile")
        self._do_registration()

        user = UserProfile.objects.get(email=self.email)
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.email)
        self.assertEqual(response.data["username"], self.username)
        self.assertEqual(response.data["first_name"], self.first_name)
        self.assertEqual(response.data["last_name"], self.last_name)
        self.assertEqual(response.data["first_language"], 1)
        self.assertEqual(response.data["language_being_learned"], 2)

    def test_that_profile_cannot_be_accessed_by_unauthenicated_user(self):
        """
        Ensure that the user profile cannot be accessed unless the user
        has been authenticated
        """
        url = reverse("profile")

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
