# """Logging in and co tests."""

import pytest

from .utils import async_session, base_test, TestCase
from .conftest import (
    one_user_db,
    simple_user,
    account_data,
    base_category_data,
)

from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


def user_request():
    return {"name": "TestGuy", "password": "TestPass"}


def user_response():
    return (
        {
            "status": "OK",
            "user": {
                "id": 1,
                "name": "TestGuy",
            },
        },
        200,
    )


# register_while_logged_in
# signup_with_too_long_name
# signup_with_too_long_password
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # create user
            {},
            None,
            user_request(),
            user_response(),
            one_user_db(),
        ),
        TestCase(  # create duplicate user
            one_user_db(),
            None,
            user_request(),
            ({"status": "user exists"}, 200),
            one_user_db(),
        ),
    ],
    ids=["create user", "create duplicate user"],
)
async def test_register(case: TestCase):
    await base_test("/register", case)


# wrong_password
# login_with_non_existant_user
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # normal login
            one_user_db(),
            None,
            user_request(),
            user_response(),
            one_user_db(),
        )
    ],
    ids=["normal login"],
)
async def test_login(case: TestCase):
    await base_test("/login", case)


def change_name_request():
    return {
        "name": "ChangedUser",
        "old_pass": "TestPass",
        "new_pass": "TestPass",
    }


def change_name_response():
    return (
        {
            "status": "OK",
            "user": {
                "id": 1,
                "name": "ChangedUser",
            },
        },
        200,
    )


def changed_name_db():
    return {
        "users": [
            {
                "id": 1,
                "name": "TestGuy",
                "password_hash": "dcf7fb88d38b9cbc0719c4d47af0b9ca",
            }
        ],
        "accounts": [account_data()],
        "categories": [base_category_data()],
        "events": [],
    }


# change_name_into_duplicate
# change_name_into_too_long_one
# change_password_into_too_long_one
# change_password
# change_password_with_wrong_passwod
# change_name_into_itself
# change_password_into_itself
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # change name
            one_user_db(),
            simple_user(),
            change_name_request(),
            change_name_response(),
            changed_name_db(),
        ),
    ],
    ids=["change name"],
)
async def test_edit_user(case: TestCase):
    await base_test("/edit_user", case)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # simple get_data
            one_user_db(),
            simple_user(),
            {},
            user_response(),
            one_user_db(),
        ),
    ],
    ids=["simple get data"],
)
async def test_get_user_data(case: TestCase):
    await base_test("/get_user_data", case)
