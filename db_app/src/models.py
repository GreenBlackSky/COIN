"""Data base models."""

import datetime

from sqlalchemy import Column, ForeignKey, Date, Time, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


DeclarativeBase = declarative_base()


class TestData(DeclarativeBase):
    """Test data model."""

    __tablename__ = "test_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)


class User(DeclarativeBase):
    """User model."""

    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False, unique=False)

    accounts = relationship(
        'Account',
        back_populates='user',
        cascade="all, delete",
        passive_deletes=True
    )


class Account(DeclarativeBase):
    """Account model. Each user can have multyple accounts."""

    __tablename__ = 'accounts'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    actual_date = Column(Date())

    user = relationship('User', back_populates='accounts')
    dates = relationship(
        'Date',
        back_populates='account',
        cascade="all, delete",
        passive_deletes=True
    )
    categories = relationship(
        'Category',
        back_populates='account',
        cascade="all, delete",
        passive_deletes=True
    )
    events = relationship('Event', back_populates='account')
    templates = relationship(
        'Template',
        back_populates='account',
        cascade="all, delete",
        passive_deletes=True
    )


class Date(DeclarativeBase):
    """Dates of transactions."""

    __tablename__ = 'dates'

    id = Column(Integer(), primary_key=True)
    account_id = Column(Integer(), ForeignKey('accounts.id'))
    date = Column(Date())
    balance = Column(Integer())
    unconfirmed_balance = Column(Integer())

    account = relationship('Account', back_populates='dates')
    events = relationship(
        'Event',
        back_populates='date',
        cascade="all, delete",
        passive_deletes=True
    )


class Category(DeclarativeBase):
    """Categories of transactions."""

    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True)
    account_id = Column(Integer(), ForeignKey('accounts.id'))
    name = Column(String(100))
    description = Column(String(200))
    hidden = Column(Boolean())

    account = relationship('Account', back_populates='categories')
    events = relationship('Event', back_populates='category')
    templates = relationship(
        'Template',
        back_populates='category',
        cascade="all, delete",
        passive_deletes=True
    )


class Event(DeclarativeBase):
    """Transactions events."""

    __tablename__ = 'events'

    date_id = Column(Date(), ForeignKey('dates.id'))
    account_id = Column(Integer(), ForeignKey('accounts.id'))
    time = Column(Time())
    diff = Column(Integer())
    category_id = Column(Integer(), ForeignKey('categories.id'))
    description = Column(String(200))
    confirmed = Column(Boolean())

    date = relationship('Date', back_populates='events')
    account = relationship('Account', back_populates='events')
    category = relationship('Category', back_populates='events')


class Template(DeclarativeBase):
    """Events templates."""

    __tablename__ = 'templates'

    active = Column(Boolean())
    account_id = Column(Integer(), ForeignKey('accounts.id'))
    time = Column(Time())
    diff = Column(Integer())
    category_id = Column(Integer(), ForeignKey('category.id'))
    last_confirmed_date = Column(Date())
    description = Column(String(200))
    template = Column(Integer())
    cycle_length = Column(Integer())

    account = relationship('Account', back_populates='events')
    category = relationship('Category', back_populates='events')
