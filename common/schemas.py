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
    last_confirmed_date: DateType
    description: str
    template: int
    cycle_length: int


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
class Account:
    """Users account. One user can have multiple accounts."""

    id: int
    name: str
    actual_date: DateType
    balance: float
    unconfirmed_balance: float
    templates: List[int]
    categories: List[int]


@dataclass
class User:
    """Well, it's User."""

    id: int
    email: str
    accounts: List[int]


UserSchema = class_schema(User)
AccountSchema = class_schema(Account)
CategorySchema = class_schema(Category)
EventSchema = class_schema(Event)
TemplateSchema = class_schema(Template)
