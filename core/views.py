from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from core.models import User
from core.serializers import UserCreateSerializer


class UserRegView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
