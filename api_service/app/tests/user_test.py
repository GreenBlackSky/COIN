"""Logging in and co tests."""

import pytest
from pytest_lazyfixture import lazy_fixture

from .utils import async_session, base_test
from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


@pytest.fixture
def user_request():
    return {"name": "TestGuy", "password": "TestPass"}


@pytest.fixture
def user_response():
    return {
        "status": "OK",
        "user": {
            "id": 1,
            "name": "TestGuy",
        },
    }


# register_while_logged_in
# signup_with_too_long_name
# signup_with_too_long_password
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # create user
            {},
            None,
            lazy_fixture("user_request"),
            200,
            lazy_fixture("user_response"),
            lazy_fixture("one_user_db"),
        ],
        [  # create duplicate user
            lazy_fixture("one_user_db"),
            None,
            lazy_fixture("user_request"),
            200,
            {"status": "user exists"},
            lazy_fixture("one_user_db"),
        ],
    ],
    ids=["create user", "create duplicate user"],
)
async def test_register(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/register",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


# wrong_password
# login_with_non_existant_user
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # normal login
            lazy_fixture("one_user_db"),
            None,
            lazy_fixture("user_request"),
            200,
            lazy_fixture("user_response"),
            lazy_fixture("one_user_db"),
        ]
    ],
    ids=["normal login"],
)
async def test_login(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/login",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


@pytest.fixture
def chamge_name_user_data():
    return {
        "id": 1,
        "name": "ChangedUser",
    }


@pytest.fixture
def chamge_name_full_user_data():
    return {
        "id": 1,
        "name": "TestGuy",
        "password_hash": "dcf7fb88d38b9cbc0719c4d47af0b9ca",
    }


@pytest.fixture
def change_name_request():
    return {
        "name": "ChangedUser",
        "old_pass": "TestPass",
        "new_pass": "TestPass",
    }


@pytest.fixture
def change_name_response(chamge_name_user_data):
    return {"status": "OK", "user": chamge_name_user_data}


@pytest.fixture
def changed_name_db(
    chamge_name_full_user_data, account_data, base_category_data
):
    return {
        "users": [chamge_name_full_user_data],
        "accounts": [account_data],
        "categories": [base_category_data],
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
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # change name
            lazy_fixture("one_user_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("change_name_request"),
            200,
            lazy_fixture("change_name_response"),
            lazy_fixture("changed_name_db"),
        ]
    ],
    ids=["change name"],
)
async def test_edit_user(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/edit_user",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


# get standart data
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # simple get_data
            lazy_fixture("one_user_db"),
            lazy_fixture("simple_user"),
            {},
            200,
            lazy_fixture("user_response"),
            lazy_fixture("one_user_db"),
        ]
    ],
    ids=["simple get data"],
)
async def test_get_user_data(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/get_user_data",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )
