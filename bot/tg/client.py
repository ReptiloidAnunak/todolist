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

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url(BotUrlMethods.GET_UPDATES)
        updates_resp = requests.get(url)
        updates_raw = json.loads(updates_resp.text)
        GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
        result = GetUpdatesResponseSchema().loads(updates_resp.text)

        if not updates_raw:
            raise NotImplementedError
        return result

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        raise NotImplementedError
