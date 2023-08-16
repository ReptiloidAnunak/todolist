
from rest_framework import response, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from bot.management.commands.runbot import Command
from bot.models import TgUser
from bot.setializers import TgUserVerificationSerializer
from core.models import User


class TgUserVerification(UpdateAPIView):
    serializer_class = TgUserVerificationSerializer
    permission_classes = [IsAuthenticated]
    success_ver_answ = "Верификация прошла успешно"

    def get_object(self) -> User:
        return self.request.user

    def perform_update(self, serializer: serializers.ModelSerializer) -> response.Response:
        """Получает верификационный код, проверяет его на соответствие с кодом
         в таблице телеграм-пользователей, связывает тг-аккаунт пользователя
         с его аккаунтом в приложении."""
        ver_code = self.request.data["verification_code"]
        tg_user = TgUser.objects.get(verification_code=ver_code)
        tg_user.user_id = self.get_object()
        tg_user.save()

        self._send_tg_confirmation(tg_user.tg_chat_id)
        return response.Response(self.success_ver_answ,
                                 status=status.HTTP_200_OK)

    def _send_tg_confirmation(self, tg_chat_id):
        """ Отправляет сообщение в тг об успешной верификации"""
        tg_client = Command.tg_client
        tg_client.send_message(chat_id=tg_chat_id,
                               text=self.success_ver_answ)






