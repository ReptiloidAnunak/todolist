import marshmallow
from dataclasses import dataclass
from typing import List


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    last_name: str #нет в ответе отправленного сообщения
    username: str
    language_code: str #нет в ответе отправленного сообщения

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Chat:
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


@dataclass
class Message:
    message_id: int
    from_: MessageFrom
    chat: Chat
    date: int
    text: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]  # todo

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE

