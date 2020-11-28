"""Data base models."""

from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'flask_login_users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False, unique=False)
    created_on = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())

    balance_accepted_on = db.Column(db.DateTime())
    balance = db.Column(db.Integer())

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Category(db.Model):
    __tablename__ = 'operation_category'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    user_id = db.relationship("User", backref="id")


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    value = db.Column(db.Integer())
    comment = db.Column(db.String(200))
    accepted = db.Column(db.Boolean())

    category = db.relationship("Category", backref="id")
    user_id = db.relationship("User", backref="id")


class Template(db.Model):
    __tablename__ = "templates"

    id = db.Column(db.Integer(), primary_key=True)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    cycle = db.Column(db.PickleType())
    value = db.Column(db.Integer())
    comment = db.Column(db.String(200))

    category = db.relationship("Category", backref="id")
    user_id = db.relationship("User", backref="id")
