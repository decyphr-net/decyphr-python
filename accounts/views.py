from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from accounts.permissions import IsCreationOrIsAuthenticated
from accounts.models import UserProfile
from accounts.serializers import UserSerializer, TokenAuthSerializer


class ObtainAuthToken(APIView):

    def post(self, request):
        try:
            serializer = TokenAuthSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            content = {
              "token": token.key
            }

            return Response(content, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            message = "This user wasn't found. Please try again"
            return Response(message, status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    """
    Handle user interactions with their profile
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCreationOrIsAuthenticated, )

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
    
    def _create_token(self, user):
        Token.objects.create(user=user)
        return user

    def create(self, request):
        """
        Register the new user
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = UserProfile.objects.create_user(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve the profile for the currently logged in user
        """
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
