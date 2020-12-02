"""Data base models."""

from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Users table."""

    __tablename__ = 'flask_login_users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False, unique=False)
    created_on = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())
    accepted_balance = db.Column(db.Integer())
    balance_accepted_on = db.Column(db.DateTime())

    def set_password(self, password):
        """Set user password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check user password."""
        return check_password_hash(self.password, password)

    def serialize(self):
        """Serialize user into dict."""
        return {
            'created_on': self.created_on,
            'last_login': self.last_login,
            'accepted_balance': self.accepted_balance,
            'balance_accepted_on': self.balance_accepted_on,
        }


class Month(db.Model):
    """Month data."""

    __tablename__ = 'months'

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    initial_value = db.Column(db.Integer())

    user_id = db.relationship("User", backref="id")


class Category(db.Model):
    """Events category table."""

    __tablename__ = 'operation_category'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), primary_key=True)

    user_id = db.relationship("User", backref="id")


class Event(db.Model):
    """Events table."""

    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    value = db.Column(db.Integer())
    comment = db.Column(db.String(200))
    accepted = db.Column(db.Boolean())

    category = db.relationship("Category", backref="id")
    user_id = db.relationship("User", backref="id")

    def serialize(self):
        """Serialize event into dict."""
        return {
            "id": self.id,
            'date': self.date,
            'value': self.value,
            'comment': self.comment,
            'accepted': self.accepted,
            'category': self.category
        }


class Template(db.Model):
    """Events templates table."""

    __tablename__ = "templates"

    id = db.Column(db.Integer(), primary_key=True)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    cycle = db.Column(db.PickleType())
    value = db.Column(db.Integer())
    comment = db.Column(db.String(200))

    category = db.relationship("Category", backref="id")
    user_id = db.relationship("User", backref="id")
