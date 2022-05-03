"""Accounts stuff tests."""

import pytest
from pytest_lazyfixture import lazy_fixture


from .utils import async_session, base_test, set_current_user
from ..main import app
from ..utils.database import get_session
from ..utils.models import UserModel

app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


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
def one_user_db(full_user_data, account_data):
    return {"users": [full_user_data], "accounts": [account_data]}


@pytest.fixture
def new_account_request():
    return {"name": "TestAccount"}


@pytest.fixture
def new_account_data():
    return {"id": 2, "user_id": 1, "name": "TestAccount"}


@pytest.fixture
def new_account_response(new_account_data):
    return {"status": "OK", "account": new_account_data}


@pytest.fixture
def new_accont_db(full_user_data, account_data, new_account_data):
    return {
        "users": [full_user_data],
        "accounts": [account_data, new_account_data],
    }


# create_max_accounts
# create_new_account
# create_duplicate_account
# create_with_too_long_name
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # create account
            lazy_fixture("one_user_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("new_account_request"),
            200,
            lazy_fixture("new_account_response"),
            lazy_fixture("new_accont_db"),
        ]
    ],
    ids=["create account"],
)
async def test_create_account(
    db_before, user, request_data, response_code, response_data, db_after
):
    with set_current_user(app, user):
        await base_test(
            "/create_account",
            db_before,
            request_data,
            response_code,
            response_data,
            db_after,
        )


# get_accounts
def test_get_accounts():
    pass


# rename_account
# rename_non_existant_account
# rename_account_into_duplicate
# rename_with_too_long_name
def test_edit_account():
    pass


# remove_one_account
# remove_non_existant_account
# remove_only_account
def test_delete_account():
    pass


# main_account_created
