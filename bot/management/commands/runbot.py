from django.core.management.base import BaseCommand, CommandError

from bot.tg.client import TgClient

# python3 manage.py runbot


class Command(BaseCommand):
    help = "Run telegram-bot"

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient()
        messages_id = []

        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1

            if item.message.message_id not in messages_id:
                tg_client.send_message(chat_id=item.message.chat.id,
                                       text=item.message.text)
                messages_id.append(item.message.message_id)

