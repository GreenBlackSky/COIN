import datetime as dt

import pytest

from ..utils.models import UserModel


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def full_user_data():
    return {
        "id": 1,
        "name": "TestGuy",
        "password_hash": "dcf7fb88d38b9cbc0719c4d47af0b9ca",
    }


@pytest.fixture
def simple_user(full_user_data):
    return UserModel(**full_user_data)


@pytest.fixture
def account_data():
    return {"id": 1, "user_id": 1, "name": "Main Account"}


@pytest.fixture
def base_category_data():
    return {
        "user_id": 1,
        "account_id": 1,
        "id": 0,
        "name": "base",
        "color": "16777215",
    }


@pytest.fixture
def one_user_db(full_user_data, account_data, base_category_data):
    return {
        "users": [full_user_data],
        "accounts": [account_data],
        "categories": [base_category_data],
    }


@pytest.fixture
def new_category_data():
    return {
        "account_id": 2,
        "color": "16777215",
        "id": 0,
        "name": "base",
        "user_id": 1,
    }


@pytest.fixture
def base_event():
    return {
        "user_id": 1,
        "account_id": 1,
        "id": 0,
        "category_id": 1,
        "event_time": dt.datetime.timestamp(dt.datetime(1991, 1, 1)),
        "diff": 1,
        "description": "test"
    }
