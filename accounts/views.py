from django.conf import settings
from django.contrib.auth import logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import UserProfile
from . import serializers
from .utils import get_and_authenticate_user, create_user_account


class AuthViewSet(viewsets.GenericViewSet):
    """Authentication Viewset

    The viewset that will be responsible for handle the user's authentication
    and authorization
    """
    permission_classes = [AllowAny,]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.RegisterUserSerializer
    }
    queryset = UserProfile.objects.all()

    @action(methods=['POST'], detail=False)
    def login(self, request):
        """Login
        
        Authenticate the user and log them in, and return the user and the
        user's token to the client. The request data will be serialized as per
        the requirements of the `UserLoginSerializer`.

        Returns:
            AuthorizedUserSerializer: A JSON-ified UserProfile object which
            also includes the token for that user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthorisedUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.AuthorisedUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)
    

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
    
    def get_serializer_class(self):
        """Get Serializer Class

        This viewset has multiple actions and has potentially different 
        serializers per action. This will handle the switching out of each
        of the serializer classes
        """
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
