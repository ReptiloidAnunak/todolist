from typing import Any

from django.core.management.base import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.functions import generate_verification_code, create_goal_list_message
from core.models import User
from goals.models import Goal

# python3 manage.py runbot


class Command(BaseCommand):
    help = "Run telegram-bot"
    tg_client = TgClient()
    user_authenticated = False

    def handle(self, *args, **options: Any) -> None:
        offset = 0
        old_messages = self.tg_client.get_updates(offset=offset).result
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                if item not in old_messages:
                    old_messages.append(item)
                    if self.user_authenticated is True:
                        self.get_goals(item)
                    else:
                        self.tg_user_auth(item)

    def tg_user_auth(self, item) -> None:
        tg_user_id = item.message.from_.id
        chat_id = item.message.chat.id
        tg_user, _ = TgUser.objects.get_or_create(tg_chat_id=chat_id,
                                                  tg_user_id=tg_user_id)
        if tg_user.verification_code is None:
            code = generate_verification_code()
            tg_user.verification_code = code
            tg_user.save()

            answer = ("Подтвердите, пожалуйста, свой аккаунт. "
                   f"Для подтверждения необходимо ввести код:\n{code}")
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=answer)

        elif not User.objects.filter(verification_code=tg_user.verification_code).exists():
            answer = ("Подтвердите, пожалуйста, свой аккаунт. "
                      f"Для подтверждения необходимо ввести код:\n{tg_user.verification_code}")
            print("tg_code: ", tg_user.verification_code)
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id, text=answer)

        else:
            self.get_goals(item=item)

    def get_goals(self, item) -> None:
        tg_user_id = item.message.from_.id
        chat_id = item.message.chat.id
        tg_user = TgUser.objects.get(tg_chat_id=chat_id,
                                     tg_user_id=tg_user_id)

        if item.message.text != "/goals":
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id,
                                        text="Неизвестная команда")
        else:
            user = User.objects.get(verification_code=tg_user.verification_code)
            goals = Goal.objects.filter(user=user, is_deleted=False)
            goals_list = [goal.title for goal in goals]
            text = create_goal_list_message(goals_list)
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id,
                                        text=text)

