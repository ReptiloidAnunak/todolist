import requests
import json
from typing import Union, Dict, List, Any

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist.settings import TG_BOT_TOKEN
import marshmallow_dataclass


GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(
    GetUpdatesResponse
)
SendMessageResponseSchema = marshmallow_dataclass.class_schema(
    SendMessageResponse
)


class BotUrlMethods:
    GET_UPDATES = "getUpdates"
    SEND_MESSAGE = "sendMessage"


class TgClient:
    def __init__(self, token=TG_BOT_TOKEN):
        self.token = token

    def get_url(self, method: str) -> str:
        """Формирует ссылку запроса на сервер телеграм-бота из токена и метода"""
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> Union[GetUpdatesResponse, Any]:
        """Возвращает обновленные данные из чата, включая сообщение пользователя"""
        url = self.get_url(BotUrlMethods.GET_UPDATES)
        response = requests.get(url)
        try:
            return GetUpdatesResponseSchema().loads(response.text)
        except Exception:
            print(f'Failed to parse data: {response}')
            raise NotImplementedError

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Отправляет пользователю сообщение"""
        url = self.get_url(BotUrlMethods.SEND_MESSAGE) + '?chat_id=' + str(chat_id) + '&text=' + text
        message_resp = requests.get(url)
        try:
            return SendMessageResponseSchema().loads(message_resp.text)
        except Exception:
            print(f'Failed to send data: {message_resp}')
            raise NotImplementedError
