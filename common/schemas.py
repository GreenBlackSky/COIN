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
    user_id: int


@dataclass
class Date:
    """Unit of time, that is referenced by accounts and events."""

    id: int
    account_id: int
    date: DateType
    balance: int
    unconfirmed_balance: int


@dataclass
class Category:
    """Category of transaction."""

    id: int
    account_id: int
    name: str
    description: str
    hidden: bool


@dataclass
class Event:
    """Transaction event."""

    date_id: int
    account_id: int
    time: TimeType
    diff: int
    category_id: int
    description: str
    confirmed: bool


@dataclass
class Template:
    """Template for regular transaction."""

    active: bool
    account_id: int
    time: TimeType
    diff: int
    category_id: int
    last_confirmed_date_id: int
    description: str
    template: int
    cycle_length: int


UserSchema = class_schema(User)
AccountSchema = class_schema(Account)
DateSchema = class_schema(Date)
CategorySchema = class_schema(Category)
EventSchema = class_schema(Event)
TemplateSchema = class_schema(Template)
