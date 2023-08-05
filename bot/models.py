from django.db import models
from core.models import User


class TgUser(models.Model):
    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    tg_chat_id = models.IntegerField()
    tg_user_id = models.IntegerField()
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

