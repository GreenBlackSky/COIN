"""Temporary data storage."""
# TODO use three separate lists
# TODO setup postgresql db
# TODO use redis

from datetime import date
from uuid import uuid4
from dataclasses import dataclass
from enum import Enum
from calendar import monthrange
from typing import Dict, List


class Category(Enum):
    """Category of events."""

    Initial = 0
    Income = 1
    Expence = 2
    Correction = 3


@dataclass
class Event:
    """Event data."""

    value: int
    event_date: date
    category: Category
    comment: str


class MonthData:
    """Finantial data per one month."""

    def __init__(self, today: date, initial: int):
        """Initialize MonthData with initial value."""
        self.initial = initial
        self.start_date = today.replace(day=1)
        _, self.month_len = monthrange(today.year, today.month)
        self.events: Dict[str, Event] = {
            self.start_date: Event(initial, today, Category.Initial, "")
        }

    def add_event(self, event_date: date, value: int, category: Category, comment: str):
        """Add new event in month."""
        if event_date.replace(day=1) != self.start_date:
            return None
        event_uid = uuid4().hex
        self.events[event_uid] = Event(value, event_date, category, comment)
        return event_uid

    def get_data(self):
        """Get month data."""
        ret = [0] * self.month_len
        for event in self.events.values():
            ret[event.event_date.day - 1] += event.value
        for day in range(1, self.month_len):
            ret[day] += ret[day - 1]
        return ret

    def calculate(self) -> int:
        """Calculate final sum for month."""
        return sum(
            event.value
            for event in self.events.values()
        )


class UserData:
    """User finantial history."""

    def __init__(self, today: date, initial: int):
        """Create new empty history."""
        self.months: Dict[date, MonthData] = {
            today.replace(day=1): MonthData(today, initial)
        }

    def add_event(self, event_date: date, value: int, category: Category, comment: str):
        """Add new event."""
        key = event_date.replace(day=1)
        if key not in self.months:
            last_month = None
            for month in self.months:
                if month < key and (last_month is None or last_month < month):
                    last_month = month
            last_month_data = self.months.get(last_month)
            if last_month_data is None:
                return
            self.months[key] = MonthData(key, last_month_data.calculate())
        return self.months[key].add_event(event_date, value, category, comment)

    def get_balance(self, day: date):
        """Get current balance."""
        key = day.replace(day=1)
        if key not in self.months:
            return None
        month_data = self.months[key]
        return month_data.calculate()

    def get_month_data(self, month: date):
        """Get month data."""
        month_data = self.months.get(month.replace(day=1))
        if month_data is None:
            return None
        return month_data.get_data()


class Storage:
    """Singleton data storage. Don't actualy use."""

    def add_event(self, user_uid: str, event_date: date, value: int, category: Category, comment: str):
        """Add new event."""
        return self.users[user_uid].add_event(event_date, value, category, comment)

    def get_balance(self, user_uid: str, day: date):
        """Get last known balance."""
        return self.users[user_uid].get_balance(day)

    def get_month_data(self, user_id: str, month: date):
        """Get month data for user."""
        return self.users[user_id].get_month_data(month)
