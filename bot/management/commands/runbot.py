from typing import Any

from django.core.management.base import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.functions import generate_verification_code
from core.models import User
from goals.models import Goal

# python3 manage.py runbot


class Command(BaseCommand):
    help = "Run telegram-bot"
    tg_client = TgClient()

    def handle(self, *args, **options: Any) -> None:
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.tg_user_auth(item)
                self.get_goals(item)

    def tg_user_auth(self, item):
        tg_user_id = item.message.from_.id
        chat_id = item.message.chat.id
        tg_user, _ = TgUser.objects.get_or_create(tg_chat_id=chat_id,
                                              tg_user_id=tg_user_id)
        if tg_user.verification_code == "":
            code = generate_verification_code()
            print(code)
            tg_user.verification_code = code
            tg_user.save()
            print("tg_code: ", tg_user.verification_code)

            answer = ("Подтвердите, пожалуйста, свой аккаунт. "
                   f"Для подтверждения необходимо ввести код:\n{code}")
            print(answer)
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=answer)

        else:
            answer = ("Подтвердите, пожалуйста, свой аккаунт. "
                      f"Для подтверждения необходимо ввести код:\n{tg_user.verification_code}")
            print("tg_code: ", tg_user.verification_code)
            print(answer)
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=answer)

            user = User.objects.get(verification_code=tg_user.verification_code)
            if user.verification_code != "":
                self.get_goals(item=item)

    def get_goals(self, item):
        tg_user_id = item.message.from_.id
        chat_id = item.message.chat.id
        tg_user = TgUser.objects.get(tg_chat_id=chat_id,
                                        tg_user_id=tg_user_id)

        user = User.objects.get(verification_code=tg_user.verification_code)
        if item.message.text == "/goals":
            print("GOALS!")
            goals = Goal.objects.filter(user=user, is_deleted=False)
            goals_list = [goal.title for goal in goals]
            text = "\n*".join(goals_list)
            print(text)
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id,
                                        text=text)
        else:
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id,
                                        text="Неизвестная команда")

