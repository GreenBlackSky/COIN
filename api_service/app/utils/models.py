"""Data base models."""

import datetime as dt

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger

from .exceptions import LogicException


Base = declarative_base()


class Serializable:
    def to_dict(self):
        return {
            key: (
                value.timestamp()
                if isinstance(value := getattr(self, key), dt.datetime)
                else value
            )
            for key in dir(self)
            if (
                not key.startswith("_")
                and key
                not in ("to_dict_safe", "to_dict", "metadata", "registry")
            )
        }


class UserModel(Base, Serializable):
    """Well, it's User."""

    __tablename__ = "users"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    name = Column(String(200), nullable=False)
    password_hash = Column(String(500), nullable=False)

    def to_dict_safe(self):
        user_data = super().to_dict()
        del user_data["password_hash"]
        return user_data


class AccountModel(Base, Serializable):
    """Users account. One user can have multiple accounts."""

    __tablename__ = "accounts"

    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
    )
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)


class CategoryModel(Base, Serializable):
    """Category of transaction."""

    __tablename__ = "categories"

    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
    )
    account_id = Column(Integer, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    color = Column(String(8), nullable=False)


class EventModel(Base, Serializable):
    """Transaction event."""

    __tablename__ = "events"

    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
    )
    account_id = Column(Integer, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    category_id = Column(Integer, nullable=False)
    event_time = Column(DateTime, nullable=False)
    diff = Column(Integer, nullable=False)
    description = Column(String(200), nullable=False)


class SavePointModel(Base, Serializable):
    """Transaction event."""

    __tablename__ = "save_points"

    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
    )
    account_id = Column(Integer, primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    datetime = Column(DateTime, nullable=False)
    total = Column(Integer, nullable=False)


async def create_account(session: AsyncSession, user_id, name) -> AccountModel:
    if await session.get(UserModel, user_id) is None:
        raise LogicException("No such user")

    query = (
        await session.execute(
            select(AccountModel)
            .where(AccountModel.user_id == user_id)
            .order_by(desc(AccountModel.id))
            .limit(1)
        )
    ).first()

    if not query:
        account_id = 1
    else:
        account_id = query[0].id + 1
    return AccountModel(user_id=user_id, id=account_id, name=name)


async def create_account_entry(
    session: AsyncSession, model, user_id, account_id, **data
):
    if not (await session.get(UserModel, user_id)):
        raise LogicException("No such user")

    if not (await session.get(AccountModel, (user_id, account_id))):
        raise LogicException("Invalid account id for given user")

    query = (
        await session.execute(
            select(model)
            .where(model.user_id == user_id)
            .where(model.account_id == account_id)
            .order_by(desc(model.id))
        )
    ).first()
    if not query:
        entry_id = 0
    else:
        entry_id = query[0].id + 1
    return model(user_id=user_id, account_id=account_id, id=entry_id, **data)
