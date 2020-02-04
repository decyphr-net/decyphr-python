from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from accounts.models import UserProfile
from accounts.serializers import UserSerializer, TokenAuthSerializer


class ObtainAuthToken(APIView):

    def post(self, request):
        serializer = TokenAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': token.key,
        }

        return Response(content)


class UserRegistration(APIView):
    """
    The view that handles the registration process for a user.

    This process includes creating a new entry in the database, as
    well as sending an email to the user as confirmation that they've
    registered
    """

    serializer_class = UserSerializer

    def _send_email(self, email_address):
        """
        Send an email to the newly created to user to let them know
        that they've completed the sign up
        """
        subject = "Welcome to langapp"
        message = "Thank you for registering on langapp"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email_address],
            fail_silently=False,
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            self._send_email(serializer.data["email"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
