import marshmallow
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    username: str
    language_code: str = "None"
    last_name: str = "None"
    first_name: str = "None"

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Chat:
    id: int
    username: str
    type: str
    last_name: str = "None"
    first_name: str = "None"

@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    date: int
    text: str = "__None__"

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message = field()

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE

