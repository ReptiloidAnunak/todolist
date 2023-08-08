
from rest_framework import response, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from bot.management.commands.runbot import Command
from bot.models import TgUser
from bot.setializers import TgUserVerificationSerializer
from core.models import User


class TgUserVerification(UpdateAPIView):
    queryset = User
    serializer_class = TgUserVerificationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def perform_update(self, serializer):
        tg_client = Command.tg_client
        ver_code = self.request.data["verification_code"]
        tg_user = TgUser.objects.get(verification_code=ver_code)
        user = self.get_object()
        answer = "Верификация прошла успешно"
        tg_user.user_id = user
        tg_user.save()
        user.verification_code = tg_user.verification_code
        user.save()
        tg_client.send_message(chat_id=tg_user.tg_chat_id, text=answer)
        return response.Response(answer, status=status.HTTP_200_OK)




