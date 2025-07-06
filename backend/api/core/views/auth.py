from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from api.core.serializers import auth as auth_serializers
from django.conf import settings
from rest_framework import viewsets, status

User = get_user_model()

class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser] if not settings.DEBUG else [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = auth_serializers.UserSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:            
            username = request.data.get('username')
            password = request.data.get('password')

            if not username or not password:
                return Response({"message": "Credenciais incompletas"}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(username=username, password=password)
            if user is None:
                return Response({"message": "Usuário ou senha inválidos"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            data = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": auth_serializers.UserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"Erro ao fazer login: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"message": "Refresh token não informado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
            user = User.objects.get(id=refresh["user_id"])
            data = {
                "access": str(access),
                "refresh": str(refresh),
                "user": auth_serializers.UserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"message": f"Token inválido ou expirado: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)

class UserMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user:
            return Response({"message": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(auth_serializers.UserSerializer(user).data)
