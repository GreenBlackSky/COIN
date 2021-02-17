"""Data base models."""

import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
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
    name = Column(String(100), nullable=False, unique=False)
    password_hash = Column(String(200), nullable=False, unique=False)
    # created_on = db.Column(db.DateTime())
    # last_login = db.Column(db.DateTime())
    # accepted_balance = db.Column(db.Integer())
    # balance_accepted_on = db.Column(db.DateTime())

    # def serialize(self):
    #     """Serialize user into dict."""
    #     return {
    #         'created_on': self.created_on,
    #         'last_login': self.last_login,
    #         'accepted_balance': self.accepted_balance,
    #         'balance_accepted_on': self.balance_accepted_on,
    #     }


# class Month(db.Model):
#     """Month data."""

#     __tablename__ = 'months'

#     id = db.Column(db.Integer(), primary_key=True)
#     date = db.Column(db.DateTime())
#     initial_value = db.Column(db.Integer())

#     user_id = db.relationship("User", backref="id")


# class Category(db.Model):
#     """Events category table."""

#     __tablename__ = 'operation_category'

#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(100), primary_key=True)

#     user_id = db.relationship("User", backref="id")


# class Event(db.Model):
#     """Events table."""

#     __tablename__ = 'events'

#     id = db.Column(db.Integer(), primary_key=True)
#     date = db.Column(db.DateTime())
#     value = db.Column(db.Integer())
#     comment = db.Column(db.String(200))
#     accepted = db.Column(db.Boolean())

#     category = db.relationship("Category", backref="id")
#     user_id = db.relationship("User", backref="id")

#     def serialize(self):
#         """Serialize event into dict."""
#         return {
#             "id": self.id,
#             'date': self.date,
#             'value': self.value,
#             'comment': self.comment,
#             'accepted': self.accepted,
#             'category': self.category
#         }


# class Template(db.Model):
#     """Events templates table."""

#     __tablename__ = "templates"

#     id = db.Column(db.Integer(), primary_key=True)
#     start_date = db.Column(db.DateTime())
#     end_date = db.Column(db.DateTime())
#     cycle = db.Column(db.PickleType())
#     value = db.Column(db.Integer())
#     comment = db.Column(db.String(200))

#     category = db.relationship("Category", backref="id")
#     user_id = db.relationship("User", backref="id")
