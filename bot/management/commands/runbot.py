from typing import Any
from django.utils import timezone
from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.functions import (generate_verification_code, create_goal_list_message,
                           create_categories_list, confirm_goal_creation)
from core.models import User
from goals.models import Goal, GoalCategory

# python3 manage.py runbot


class Command(BaseCommand):
    help = "Run telegram-bot"
    tg_client = TgClient()
    user_authenticated = False

    bot_commands = ["/goals", "/create"]
    categories_numbers = []
    categories_dict = {}
    category_title = ""

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
            self.route_process(item, tg_user)

    def route_process(self, item, tg_user):
        user_message = item.message.text
        user = User.objects.get(verification_code=tg_user.verification_code)
        chat_id = item.message.chat.id

        if user_message == "/goals":
            self.get_goals(item)
        elif user_message == "/create":
            self.get_cat_choice(user, chat_id)
        elif "cat-" in user_message:
            raw_cat = user_message
            self.get_category(chat_id, raw_cat)
        elif "goal-" in user_message:
            raw_goal = user_message
            self.crate_goal(user, chat_id, raw_goal)
        else:
            self.tg_client.send_message(chat_id=tg_user.tg_chat_id,
                                        text="Неизвестная команда")

    def get_goals(self, item) -> None:
        tg_user_id = item.message.from_.id
        chat_id = item.message.chat.id
        tg_user = TgUser.objects.get(tg_chat_id=chat_id,
                                     tg_user_id=tg_user_id)

        user = User.objects.get(verification_code=tg_user.verification_code)
        goals = Goal.objects.filter(user=user, is_deleted=False)
        goals_list = [goal.title for goal in goals]
        text = create_goal_list_message(goals_list)
        self.tg_client.send_message(chat_id=tg_user.tg_chat_id,
                                    text=text)

    def get_cat_choice(self, user, chat_id):

        categories = list(GoalCategory.objects.filter(user=user, is_deleted=False))

        for cat in categories:
            number = categories.index(cat) + 1
            self.categories_numbers.append(number)
            self.categories_dict[number] = cat.title

        cat_choice = create_categories_list(self.categories_dict)

        self.tg_client.send_message(chat_id=chat_id,
                                    text=f"{cat_choice}"
                                    "\n\nНажмите на номер нужной категории или пришлите его номер в формате: cat-1")

    def get_category(self, chat_id, raw_cat):
        cat_number = int(raw_cat.split("-")[1])
        if cat_number not in self.categories_dict.keys():
            self.tg_client.send_message(chat_id=chat_id,
                                        text=f"Номера категории в списке нет"
                                             "\nПришлите номер нужной категории в формате: cat-1")
        else:
            self.category_title = self.categories_dict[cat_number]
            self.tg_client.send_message(chat_id=chat_id,
                                        text="\nПришлите название цели в формате: goal-Ваша цель")

    def crate_goal(self, user, chat_id, raw_goal):
        goal_title = raw_goal.split("-")[1]
        category = GoalCategory.objects.filter(is_deleted=False,
                                               user=user,
                                               title=self.category_title).first()
        new_goal = Goal.objects.create(
            title=goal_title,
            user=user,
            category=category,
        )

        new_goal.save()
        response = confirm_goal_creation(new_goal)
        self.tg_client.send_message(chat_id=chat_id,
                                    text=response)






