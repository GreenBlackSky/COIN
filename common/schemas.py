from marshmallow import Schema, fields, post_load
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    password_hash: str

    def get_id(self):
        return self.id


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    password_hash = fields.Str()

    @post_load
    def _make_user(self, data, **kargs):
        return User(**data)
