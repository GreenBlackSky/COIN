"""Temporary data storage."""
# TODO setup postgresql db
# TODO use three separate lists


from datetime import date
from uuid import uuid4
from dataclasses import dataclass
from enum import Enum


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
    category: Category
    comment: str


class MonthData:
    """Finantial data per one month."""

    def __init__(self, today: date, initial: int):
        """Initialize MonthData with initial value."""
        self.initial = initial
        self.events = {today.replace(day=0): Event(initial, Category.Initial, "")}

    def calculate(self):
        """Calculate final sum for month."""
        return sum((event.value for event in self.events), self.initial)


class UserData:
    """User finantial history."""

    def __init__(self, today: date, initial: int):
        """Create new empty history."""
        self.months = {today.replace(day=0): MonthData(today, initial)}

    def add_event(self, event_date: date, value: int, category: Category, comment: str):
        """Add new event."""
        key = event_date.replace(day=0)
        if key not in self.months:
            last_month = None
            for month in self.months:
                if month < key and (last_month is None or last_month < month):
                    last_month = month
            last_month_data = self.months[last_month]
            self.months[key] = MonthData(key, last_month_data.calculate())

    def get_balance(self):
        """Get current balance."""
        last_month = max(self.months)
        return self.months[last_month].calculate()


class Storage:
    """Singleton data storage. Don't actualy use."""

    instance = None

    @staticmethod
    def get_instance() -> Storage:
        """Access method."""
        if Storage.instance is None:
            Storage.instance = Storage()
        return Storage.instance

    def __init__(self):
        """Initialize storage."""
        self.users = {}

    def add_user(self, today, initial):
        """Add new user and get their uid."""
        user_id = uuid4().hex
        self.users[user_id] = UserData(today, initial)
        return user_id

    def add_event(self, user_uid: int, event_date: date, value: int, category: Category, comment: str):
        """Add new event."""
        self.users[user_uid].add_event(event_date, value, category, comment)

    def get_balance(self, user_uid):
        """Get last known balance."""
        return self.users[user_uid].get_balance()
