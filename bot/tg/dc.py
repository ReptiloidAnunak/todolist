import marshmallow
import marshmallow_dataclass
from dataclasses import dataclass
from typing import List, Dict


# @dataclass
# class Chat:
#     id: int
#     is_bot: bool
#     first_name: str
#     last_name: str
#     username: str
#
#     class Meta:
#         unknown = marshmallow.EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: dict

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]  # todo

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Message:
    message_id: int
    # id: int
    # chat: dict
    # date: int
    # text: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message # todo

    class Meta:
        unknown = marshmallow.EXCLUDE

