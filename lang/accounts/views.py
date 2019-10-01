from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import UserProfile
from accounts.serializers import UserSerializer


class UserPofileView(APIView):

    def get(self, request, pk):
        user = UserProfile.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
