import requests
import json
from typing import Union, Any

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist.settings import TG_BOT_TOKEN
import marshmallow_dataclass


get_updates_response_schema = marshmallow_dataclass.class_schema(
    GetUpdatesResponse
)()
send_message_response_schema = marshmallow_dataclass.class_schema(
    SendMessageResponse
)()


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
            return get_updates_response_schema.loads(response.text)
        except Exception as e:
            print(f'Failed to parse data: {response} due error: {e}')
            raise NotImplementedError

    def send_message(self, chat_id: int, text: str) -> Union[SendMessageResponse, None]:
        """Отправляет пользователю сообщение"""
        url = self.get_url(BotUrlMethods.SEND_MESSAGE) + '?chat_id=' + str(chat_id) + '&text=' + text
        message_resp = requests.get(url)
        try:
            return send_message_response_schema.loads(message_resp.text)
        except Exception as e:
            print(f'Failed to send data: {message_resp} due error: {e}')
            return None
