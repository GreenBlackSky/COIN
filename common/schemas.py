"""Module contains marshmallow schemas for objects, services exchange with."""

from datetime import date as DateType, time as TimeType
from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import class_schema


@dataclass
class Category:
    """Category of transaction."""

    id: int
    name: str
    description: str
    color: str
    hidden: bool


@dataclass
class Template:
    """Template for regular transaction."""

    active: bool
    time: TimeType
    diff: int
    category_id: int
    last_confirmed_date_id: int
    description: str
    template: int
    cycle_length: int


@dataclass
class Event:
    """Transaction event."""

    time: TimeType
    diff: int
    category_id: int
    description: str
    confirmed: bool


@dataclass
class Date:
    """Unit of time, that is referenced by accounts and events."""

    date: DateType
    balance: int
    unconfirmed_balance: int
    events: List[Event]


@dataclass
class Account:
    """Users account. One user can have multiple accounts."""

    id: int
    name: str
    dates: List[Date]
    templates: List[Template]
    categories: List[Category]


@dataclass
class User:
    """Well, it's User."""

    id: int
    name: str
    accounts: List[Account]


UserSchema = class_schema(User)
AccountSchema = class_schema(Account)
DateSchema = class_schema(Date)
CategorySchema = class_schema(Category)
EventSchema = class_schema(Event)
TemplateSchema = class_schema(Template)
