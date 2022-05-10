import datetime as dt

import pytest

from ..utils.models import UserModel


@pytest.fixture
def anyio_backend():
    return "asyncio"


def full_user_data():
    return {
        "id": 1,
        "name": "TestGuy",
        "password_hash": "dcf7fb88d38b9cbc0719c4d47af0b9ca",
    }


def simple_user():
    return UserModel(**full_user_data())


def account_data():
    return {"id": 1, "user_id": 1, "name": "Main Account"}


def base_category_data():
    return {
        "user_id": 1,
        "account_id": 1,
        "id": 0,
        "name": "base",
        "color": "16777215",
    }


def one_user_db():
    return {
        "users": [full_user_data()],
        "accounts": [account_data()],
        "categories": [base_category_data()],
        "events": [],
    }


def new_account_data():
    return {"id": 2, "user_id": 1, "name": "TestAccount"}


def new_account_category_data():
    return {
        "account_id": 2,
        "color": "16777215",
        "id": 0,
        "name": "base",
        "user_id": 1,
    }


def new_category_data():
    return {
        "user_id": 1,
        "account_id": 1,
        "id": 1,
        "name": "New category",
        "color": "12345678",
    }


def base_event():
    return {
        "user_id": 1,
        "account_id": 1,
        "id": 0,
        "category_id": 1,
        "event_time": dt.datetime.timestamp(dt.datetime(1991, 1, 1)),
        "diff": 1,
        "description": "test",
    }
