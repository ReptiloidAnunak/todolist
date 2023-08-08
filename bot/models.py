from django.db import models
from core.models import User


class TgUser(models.Model):
    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    tg_chat_id = models.IntegerField()
    tg_user_id = models.IntegerField(unique=True)
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    username = models.CharField(max_length=150, null=True)
    verification_code = models.CharField(max_length=20, null=True)

