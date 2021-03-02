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

    id: int
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

    id: int
    time: TimeType
    diff: int
    category_id: int
    description: str
    confirmed: bool


@dataclass
class Date:
    """Unit of time, that is referenced by accounts and events."""

    id: int
    date: DateType
    balance: int
    unconfirmed_balance: int
    events: List[int]


@dataclass
class Account:
    """Users account. One user can have multiple accounts."""

    id: int
    name: str
    dates: List[int]
    templates: List[int]
    categories: List[int]


@dataclass
class User:
    """Well, it's User."""

    id: int
    name: str
    email: str
    accounts: List[int]


UserSchema = class_schema(User)
AccountSchema = class_schema(Account)
DateSchema = class_schema(Date)
CategorySchema = class_schema(Category)
EventSchema = class_schema(Event)
TemplateSchema = class_schema(Template)
