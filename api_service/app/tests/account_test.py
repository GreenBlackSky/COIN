"""Accounts stuff tests."""

import pytest

from .utils import async_session, base_test, TestCase
from .conftest import (
    full_user_data,
    account_data,
    new_account_data,
    base_category_data,
    new_account_category_data,
    one_user_db,
    simple_user,
)

from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


def new_account_request():
    return {"name": "TestAccount"}


def new_account_response():
    return ({"status": "OK", "account": new_account_data()}, 200)


def new_account_db():
    return {
        "users": [full_user_data()],
        "accounts": [account_data(), new_account_data()],
        "categories": [base_category_data(), new_account_category_data()],
        "events": [],
    }


# create_max_accounts
# create_new_account
# create_duplicate_account
# create_with_too_long_name
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # create account
            one_user_db(),
            simple_user(),
            new_account_request(),
            new_account_response(),
            new_account_db(),
        )
    ],
    ids=["create account"],
)
async def test_create_account(case: TestCase):
    await base_test("/create_account", case)


def get_account_response():
    return (
        {"status": "OK", "accounts": [account_data(), new_account_data()]},
        200,
    )


@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # get accounts
            new_account_db(),
            simple_user(),
            {},
            get_account_response(),
            new_account_db(),
        )
    ],
    ids=["get accounts"],
)
async def test_get_accounts(case: TestCase):
    await base_test("/get_accounts", case)


def rename_account_request():
    return {"account_id": 1, "name": "Renamed Account"}


def renamed_account():
    return {"id": 1, "user_id": 1, "name": "Renamed Account"}


def rename_account_response():
    return ({"status": "OK", "account": renamed_account()}, 200)


def renamed_account_db():
    return {
        "users": [full_user_data()],
        "accounts": [renamed_account()],
        "categories": [base_category_data()],
        "events": [],
    }


# rename_non_existant_account
# rename_account_into_duplicate
# rename_with_too_long_name
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # rename account
            one_user_db(),
            simple_user(),
            rename_account_request(),
            rename_account_response(),
            renamed_account_db(),
        )
    ],
    ids=["rename account"],
)
async def test_edit_account(case: TestCase):
    await base_test("/edit_account", case)


def remove_account_request():
    return {"account_id": 2}


# remove_non_existant_account
# remove_only_account
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # remove one account
            new_account_db(),
            simple_user(),
            remove_account_request(),
            new_account_response(),
            one_user_db(),
        )
    ],
    ids=["remove one account"],
)
async def test_delete_account(case: TestCase):
    await base_test("/delete_account", case)
