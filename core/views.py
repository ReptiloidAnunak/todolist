from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.models import User
from core.serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer


class UserRegView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class AuthUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(UserDetailSerializer(user).data)

        else:
            return Response("Логин или пароль неверный", 403)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User: #Добавить сообщение о необходимой аутентификации
        self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response('Вы вышли из аккаунта', 200)

