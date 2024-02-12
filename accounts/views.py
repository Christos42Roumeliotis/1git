from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import AuthTokenSerializer, UserSerializer
from django.contrib import auth
# Create your views here.
class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer
    renderer_classes = [JSONRenderer, CSVRenderer]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
