"""Data base models."""

import os
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pydantic import BaseModel


connection_string = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ["POSTGRES_USER"],
    os.environ["POSTGRES_PASSWORD"],
    os.environ["POSTGRES_HOST"],
    os.environ["POSTGRES_PORT"],
    os.environ["POSTGRES_DB"],
)

Base = automap_base()
engine = create_engine(connection_string)
Base.prepare(engine, reflect=True)

# fields.DateTime.SERIALIZATION_FUNCS["iso"] = lambda arg: arg.timestamp()
# fields.DateTime.DESERIALIZATION_FUNCS["iso"] = datetime.fromtimestamp
UserModel = Base.classes.users
AccountModel = Base.classes.accounts
SavePointModel = Base.classes.save_points
EventModel = Base.classes.events
CategoryModel = Base.classes.categories

session = Session(engine)


class UserSchema(BaseModel):
    """Well, it's User."""

    id: int
    name: str
    password_hash: str

    class Config:
        orm_mode = True


class AccountSchema(BaseModel):
    """Users account. One user can have multiple accounts."""

    id: int
    user_id: int
    name: str

    class Config:
        orm_mode = True


class SavePointSchema(BaseModel):
    """Transaction event."""

    id: int
    account_id: int
    user_id: int
    datetime: dt.datetime
    total: float

    class Config:
        orm_mode = True


class EventSchema(BaseModel):
    """Transaction event."""

    id: int
    account_id: int
    user_id: int
    category_id: int
    event_time: dt.datetime
    diff: int
    description: str

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    """Category of transaction."""

    id: int
    account_id: int
    user_id: int
    name: str
    color: str

    class Config:
        orm_mode = True
