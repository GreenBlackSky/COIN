"""Module contains marshmallow schemas for objects, services exchange with."""

from dataclasses import dataclass
from datetime import datetime

from marshmallow import fields
from marshmallow_dataclass import class_schema


fields.DateTime.SERIALIZATION_FUNCS['iso'] = lambda arg: arg.timestamp()
fields.DateTime.DESERIALIZATION_FUNCS['iso'] = datetime.fromtimestamp


@dataclass
class User:
    """Well, it's User."""

    id: int
    name: str
    password_hash: str


@dataclass
class Account:
    """Users account. One user can have multiple accounts."""

    id: int
    name: str


@dataclass
class Event:
    """Transaction event."""

    user_id: int
    account_id: int
    id: int
    event_time: datetime
    diff: int
    description: str


@dataclass
class Category:
    """Category of transaction."""

    user_id: int
    account_id: int
    id: int
    name: str
    color: int


# @dataclass
# class Template:
#     """Template for regular transaction."""

#     id: int
#     active: bool
#     time: TimeType
#     diff: int
#     category_id: int
#     last_confirmed_date: DateType
#     description: str
#     template: int
#     cycle_length: int


UserSchema = class_schema(User)
AccountSchema = class_schema(Account)
CategorySchema = class_schema(Category)
EventSchema = class_schema(Event)
# TemplateSchema = class_schema(Template)
