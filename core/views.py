from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from core.models import User
from core.serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer, \
    UserUpdatePwdSerializer


class UserRegView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class AuthUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request) -> Response:
        """Функция аутентификации пользователя
        с использованием соответствующих встроенных методов Django"""
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(UserDetailSerializer(user).data,
                            status=status.HTTP_200_OK)

        else:
            return Response("Неправильный логин или пароль",
                            status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        """Получает из запроса данные пользователя
        для дальнейшего отображения его профиля,
        заменяет отбор данных по pk"""
        return self.request.user

    def delete(self, request, *args, **kwargs) -> Response:
        logout(request)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserPwdUpdate(UpdateAPIView):
    model = User
    serializer_class = UserUpdatePwdSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        """Получает из запроса данные пользователя
        для дальнейшего отображения его профиля,
        заменяет отбор данных по pk"""
        return self.request.user

    def put(self, request, *args, **kwargs) -> Response:
        """Сравнивает два результата ввода пароля при его смене
        для подтверждения пользователем данного действия"""
        user = request.user
        if user.check_password(request.data["old_password"]):
            user.set_password(request.data["new_password"])
            user.save()
            return Response("Пароль успешно обновлен", 200)
        else:
            return Response("Старый пароль введен неправильно", 403)

    def patch(self, request, *args, **kwargs) -> Response:
        """Сравнивает два результата ввода пароля при его смене
        для подтверждения пользователем данного действия"""
        user = request.user
        if user.check_password(request.data["old_password"]):
            user.set_password(request.data["new_password"])
            user.save()
            return Response("Пароль успешно обновлен", 200)
        else:
            return Response("Старый пароль введен неправильно", 403)

