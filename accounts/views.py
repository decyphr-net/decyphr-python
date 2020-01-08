from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserProfile
from accounts.serializers import UserSerializer


class UserRegistration(APIView):

    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)


class UserPofileView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        user = UserProfile.objects.get(id=request.user.id)
        serializer = self.serializer_class(data=user)
        return Response(serializer.data)
