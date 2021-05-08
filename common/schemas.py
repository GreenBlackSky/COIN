"""Module contains marshmallow schemas for objects, services exchange with."""

from datetime import date as DateType, time as TimeType
from dataclasses import dataclass

from marshmallow_dataclass import class_schema


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
    actual_date: DateType
    balance: float


@dataclass
class Event:
    """Transaction event."""

    id: int
    date: DateType
    time: TimeType
    diff: int
    category_id: int
    description: str
    confirmed: bool


@dataclass
class Category:
    """Category of transaction."""

    id: int
    name: str
    description: str
    color: str


@dataclass
class Template:
    """Template for regular transaction."""

    id: int
    active: bool
    time: TimeType
    diff: int
    category_id: int
    last_confirmed_date: DateType
    description: str
    template: int
    cycle_length: int


UserSchema = class_schema(User)
AccountSchema = class_schema(Account)
CategorySchema = class_schema(Category)
EventSchema = class_schema(Event)
TemplateSchema = class_schema(Template)
