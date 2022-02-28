"""Data base models."""

import os
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc
from pydantic import BaseModel

from .exceptions import LogicException


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


def create_account(user_id, name) -> AccountModel:
    if session.query(UserModel).get(user_id) is None:
        raise LogicException("No such user")

    account = (
        session.query(AccountModel)
        .filter(AccountModel.user_id == user_id)
        .order_by(desc(AccountModel.id))
        .first()
    )
    if account is None:
        account_id = 1
    else:
        account_id = account.id + 1
    return AccountModel(user_id=user_id, id=account_id, name=name)


def create_account_entry(model, user_id, account_id, **data):
    if session.query(UserModel).get(user_id) is None:
        raise LogicException("No such user")

    if session.query(AccountModel).get((user_id, account_id)) is None:
        raise LogicException("Invalid account id for given user")

    entry = (
        session.query(model)
        .filter(model.user_id == user_id)
        .filter(model.account_id == account_id)
        .order_by(desc(model.id))
        .first()
    )
    if entry is None:
        entry_id = 0
    else:
        entry_id = entry.id + 1
    return model(user_id=user_id, account_id=account_id, id=entry_id, **data)


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
