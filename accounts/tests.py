"""
The tests module for the accounts app.

This should test for all of the functionality across the accounts app. Any and
all initial data required to be in place for these tests should be loaded from
the `fixtures`
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from accounts.models import UserProfile
from languages.models import Language


class AccountsViewTests(APITestCase):
    """
    The test cases for the accounts viewset
    """
    fixtures = ['fixtures.json']

    def setUp(self):
        """
        A set of basic data to be reused across all of the accounts tests
        """
        self.email = "aaronsnig@example.com"
        self.username = "aaronsnig"
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
            "language_preference": 1
        }
    
    def test_registration(self):
        """Registration test

        A user can register when all of the requirements are successfully met
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(
            UserProfile.objects.last().email, "aaronsnig@example.com")
        
    def test_that_error_is_thrown_if_the_username_is_not_unique(self):
        """Throw an error when the username is not unique

        When a user tries to register with a username that is already taken
        they will receive an error informing them that the username has been
        taken
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        data["username"] = "aaron"

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["username"][0],
            "A user with that username already exists."
        )
    
    def test_that_error_is_thrown_if_email_is_not_unique(self):
        """Throw an error when the email is not unique

        When a user tries to register with a email that is already taken
        they will receive an error informing them that the email has been
        taken
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        data["email"] = "aaronsnig@gmail.com"

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["email"][0], "This field must be unique.")
    
    def test_that_error_is_thrown_if_password_is_not_present(self):
        """Throw an error when the password is not present

        When a user tries to register without providing a password they
        receive an error informing them that they must provide a password
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        data["password"] = ""

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"][0], "This field may not be blank.")
    
    def test_that_error_is_thrown_if_first_language_is_not_present(self):
        """Throw an error when the first language is not present
        
        When a user tries to register without providing a first language they
        receive an error informing them that they must provide a first language
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        data["first_language"] = ""

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["first_language"][0], "This field may not be null."
        )
    
    def test_that_error_is_thrown_if_second_language_is_not_present(self):
        """Throw an error when the second language is not present

        When a user tries to register without providing a second language they
        receive an error informing them that they must provide a second language
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        data["language_being_learned"] = ""

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["language_being_learned"][0], "This field may not be null."
        )
    
    def test_that_error_is_thrown_if_language_preference_is_not_present(self):
        """Throw an error when the language preference is not present

        When a user tries to register without providing a language preference
        they receive an error informing them that they must provide a language
        preference
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        data["language_preference"] = ""

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["language_preference"][0], "This field may not be null."
        )
    
    def test_that_error_is_thrown_if_languages_are_equal(self):
        """Throw an error when the first and second languages are equal

        When a user tries to register with matching first and second languages
        they receive an error informing them that they cannot learn the same
        language as their first language
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        data["language_being_learned"] = 1

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "You cannot learn a language that is the same as your native language.",
        )
    
    def test_user_can_choose_languages_upon_registration(self):
        """A user can choose their languages

        A user can choose any languages as their native language, or the
        language to learn. They are not limited to the languages used elsewhere
        in these tests
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        data.update({"first_language": 4, "language_being_learned": 3})

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            UserProfile.objects.last().first_language.name, "Spanish")
        self.assertEqual(
            UserProfile.objects.last().language_being_learned.name, "German"
        )
    
    def test_that_token_is_created_for_user_upon_registration(self):
        """A token is created upon registration

        When a user registers to the site, they are assigned an auth token
        that the client will use to authenticate the user against the API
        """
        url = reverse("user-register")
        data = self.user_details_as_dict

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIsNotNone(
            Token.objects.get(user__email=self.user_details_as_dict["email"]))
    
    def test_that_a_registered_user_can_get_a_token(self):
        """A registered user can get their token

        Once a user has registered, they can get access to their auth token
        """
        registration_url = reverse("user-register")
        auth_token_url = reverse("api_token_auth")

        registration_data = self.user_details_as_dict
        login_data = {"username": self.username, "password": self.password}

        registration_response = self.client.post(
            registration_url, registration_data, format="json"
        )

        self.assertEqual(
            registration_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(
            auth_token_url, login_data, format="json")

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.data)
    
    def test_that_a_user_can_log_in_with_an_email(self):
        """Logins can be performed with an email address

        When a user is logging in, they can use their email address as an
        identifier
        """
        registration_url = reverse("user-register")
        auth_token_url = reverse("api_token_auth")

        registration_data = self.user_details_as_dict
        login_data = {"username": self.email, "password": self.password}

        registration_response = self.client.post(
            registration_url, registration_data, format="json"
        )

        login_response = self.client.post(
            auth_token_url, login_data, format="json")

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.data)
    
    def test_that_correct_error_is_thrown_if_the_username_field_is_empty(self):
        """Login cannot be performed with an empty username

        When a user attempts to login with an empty username field in the post
        data, they will receive an error telling them that they need to enter a
        username
        """
        registration_url = reverse("user-register")
        auth_token_url = reverse("api_token_auth")

        registration_data = self.user_details_as_dict
        login_data = {"username": "", "password": self.password}

        registration_response = self.client.post(
            registration_url, registration_data, format="json"
        )

        login_response = self.client.post(
            auth_token_url, login_data, format="json")

        self.assertEqual(
            login_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            login_response.data["username"][0], "Please enter a username")

    def test_that_correct_error_is_thrown_if_no_username_is_provided(self):
        """Login cannot be performed without a username

        When a client attempts to perform a login without providing a
        `username` in the post data, an error will be return to inform that a
        username field is required
        """
        registration_url = reverse("user-register")
        auth_token_url = reverse("api_token_auth")

        registration_data = self.user_details_as_dict
        login_data = {"password": self.password}

        registration_response = self.client.post(
            registration_url, registration_data, format="json"
        )

        login_response = self.client.post(
            auth_token_url, login_data, format="json")

        self.assertEqual(
            login_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            login_response.data["username"][0], "Username is required")
    
    def test_that_correct_error_is_thrown_if_the_password_field_is_empty(self):
        """Login cannot be performed with an empty password

        When a client attempts to login with an empty password field in the post
        data, they will receive an error telling them that they need to enter a
        password
        """
        registration_url = reverse("user-register")
        auth_token_url = reverse("api_token_auth")

        registration_data = self.user_details_as_dict
        login_data = {"username": self.username, "password": ""}

        registration_response = self.client.post(
            registration_url, registration_data, format="json"
        )

        login_response = self.client.post(
            auth_token_url, login_data, format="json")

        self.assertEqual(
            login_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            login_response.data["password"][0], "Please enter a password")

    def test_that_correct_error_is_thrown_if_no_password_is_provided(self):
        """Login cannot be performed without a password

        When a client attempts to perform a login without providing a
        `password` in the post data, an error will be return to inform that a
        password field is required
        """
        registration_url = reverse("user-register")
        auth_token_url = reverse("api_token_auth")

        registration_data = self.user_details_as_dict
        login_data = {"username": self.username}

        registration_response = self.client.post(
            registration_url, registration_data, format="json"
        )

        login_response = self.client.post(
            auth_token_url, login_data, format="json")

        self.assertEqual(
            login_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            login_response.data["password"][0], "Password is required")

    def test_unregistered_users_cannot_get_tokens(self):
        """Unregistered users can get tokens
        
        Clients that have not registered to the site cannot retrieve access
        tokens
        """
        url = reverse("api_token_auth")
        data = {
            "username": "notindatabaseusername",
            "password": "noneexistentpassword"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            "This user wasn't found. Please try again"
        )