import requests
import json

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist.settings import TG_BOT_TOKEN
import marshmallow_dataclass


class BotUrlMethods:
    GET_UPDATES = "getUpdates"
    SEND_MESSAGE = "sendMessage"


class TgClient:
    def __init__(self, token=TG_BOT_TOKEN):
        self.token = token

    def get_url(self, method: str) -> str:
        """Формирует ссылку запроса на сервер телеграм-бота из токена и метода"""
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """Возвращает обновленные данные из чата, включая сообщение пользователя"""
        url = self.get_url(BotUrlMethods.GET_UPDATES)
        updates_resp = requests.get(url)
        GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
        result = GetUpdatesResponseSchema().loads(updates_resp.text)

        if not result:
            raise NotImplementedError
        return result

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Отправляет пользователю сообщение"""
        url = self.get_url(BotUrlMethods.SEND_MESSAGE) + '?chat_id=' + str(chat_id) + '&text=' + text
        message_resp = requests.get(url)
        SendMessageResponseSchema = marshmallow_dataclass.class_schema(SendMessageResponse)

        result = SendMessageResponseSchema().loads(message_resp.text)

        if not result:
            raise NotImplementedError
        return result
