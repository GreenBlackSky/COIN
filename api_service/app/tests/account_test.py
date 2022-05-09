"""Accounts stuff tests."""

import pytest
from pytest_lazyfixture import lazy_fixture

from .utils import async_session, base_test
from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


@pytest.fixture
def new_account_request():
    return {"name": "TestAccount"}


@pytest.fixture
def new_account_data():
    return {"id": 2, "user_id": 1, "name": "TestAccount"}


@pytest.fixture
def new_account_response(new_account_data):
    return ({"status": "OK", "account": new_account_data}, 200)


@pytest.fixture
def new_account_db(
    full_user_data,
    account_data,
    new_account_data,
    base_category_data,
    new_category_data,
):
    return {
        "users": [full_user_data],
        "accounts": [account_data, new_account_data],
        "categories": [base_category_data, new_category_data],
        "events": [],
    }


# create_max_accounts
# create_new_account
# create_duplicate_account
# create_with_too_long_name
@pytest.mark.parametrize(
    "db_before,user,request_data,response_data,db_after",
    [
        [  # create account
            lazy_fixture("one_user_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("new_account_request"),
            lazy_fixture("new_account_response"),
            lazy_fixture("new_account_db"),
        ]
    ],
    ids=["create account"],
)
async def test_create_account(
    db_before, user, request_data, response_data, db_after
):
    await base_test(
        "/create_account",
        db_before,
        user,
        request_data,
        response_data,
        db_after,
    )


@pytest.fixture
def get_account_response(account_data, new_account_data):
    return (
        {"status": "OK", "accounts": [account_data, new_account_data]},
        200,
    )


@pytest.mark.parametrize(
    "db_before,user,request_data,response_data,db_after",
    [
        [  # get accounts
            lazy_fixture("new_account_db"),
            lazy_fixture("simple_user"),
            {},
            lazy_fixture("get_account_response"),
            lazy_fixture("new_account_db"),
        ]
    ],
    ids=["get accounts"],
)
async def test_get_accounts(
    db_before, user, request_data, response_data, db_after
):
    await base_test(
        "/get_accounts",
        db_before,
        user,
        request_data,
        response_data,
        db_after,
    )


@pytest.fixture
def rename_account_request():
    return {"account_id": 1, "name": "Renamed Account"}


@pytest.fixture
def renamed_account():
    return {"id": 1, "user_id": 1, "name": "Renamed Account"}


@pytest.fixture
def rename_account_response(renamed_account):
    return ({"status": "OK", "account": renamed_account}, 200)


@pytest.fixture
def renamed_account_db(full_user_data, renamed_account, base_category_data):
    return {
        "users": [full_user_data],
        "accounts": [renamed_account],
        "categories": [base_category_data],
        "events": [],
    }


# rename_non_existant_account
# rename_account_into_duplicate
# rename_with_too_long_name
@pytest.mark.parametrize(
    "db_before,user,request_data,response_data,db_after",
    [
        [  # rename account
            lazy_fixture("one_user_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("rename_account_request"),
            lazy_fixture("rename_account_response"),
            lazy_fixture("renamed_account_db"),
        ]
    ],
    ids=["rename account"],
)
async def test_edit_account(
    db_before, user, request_data, response_data, db_after
):
    await base_test(
        "/edit_account",
        db_before,
        user,
        request_data,
        response_data,
        db_after,
    )


@pytest.fixture
def remove_account_request():
    return {"account_id": 2}


# remove_non_existant_account
# remove_only_account
@pytest.mark.parametrize(
    "db_before,user,request_data,response_data,db_after",
    [
        [  # remove one account
            lazy_fixture("new_account_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("remove_account_request"),
            lazy_fixture("new_account_response"),
            lazy_fixture("one_user_db"),
        ]
    ],
    ids=["remove one account"],
)
async def test_delete_account(
    db_before, user, request_data, response_data, db_after
):
    await base_test(
        "/delete_account",
        db_before,
        user,
        request_data,
        response_data,
        db_after,
    )
