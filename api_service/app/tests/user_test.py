"""Logging in and co tests."""

from httpx import AsyncClient
import pytest
from pytest_lazyfixture import lazy_fixture


from .utils import (
    async_session,
    prepare_db,
    compare_with_skip,
    get_db,
    # current_user,
)
from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


@pytest.fixture
def create_user_request():
    return {"name": "TestGuy", "password": "TestPass"}


@pytest.fixture
def user_data():
    return {
        "id": 1,
        "name": "TestGuy",
        "password_hash": "dcf7fb88d38b9cbc0719c4d47af0b9ca",
    }


@pytest.fixture
def one_user_db(user_data):
    return {"users": [user_data]}


@pytest.fixture
def create_user_response(user_data):
    return {"status": "OK", "user": user_data}


@pytest.fixture
def anyio_backend():
    return "asyncio"


async def base_test(
    path, db_before, request_data, result_code, response_data, db_after
):
    await prepare_db(**db_before)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(path, json=request_data)
    assert response.status_code == result_code, response.text
    data = response.json()
    assert compare_with_skip(data, response_data, {"access_token"})
    assert compare_with_skip((await get_db()), db_after, {"access_token"})


# register_while_logged_in
# signup_with_too_long_name
# signup_with_too_long_password
@pytest.mark.parametrize(
    "db_before,request_data,result_code,response_data,db_after",
    [
        [  # create user
            {},
            lazy_fixture("create_user_request"),
            200,
            lazy_fixture("create_user_response"),
            lazy_fixture("one_user_db"),
        ],
        [  # create duplicate user
            lazy_fixture("one_user_db"),
            lazy_fixture("create_user_request"),
            200,
            {"status": "user exists"},
            lazy_fixture("one_user_db"),
        ],
    ],
    ids=["create user", "create duplicate user"],
)
async def test_register(
    db_before, request_data, result_code, response_data, db_after
):
    await base_test(
        "/register",
        db_before,
        request_data,
        result_code,
        response_data,
        db_after,
    )


# wrong_password
# login_with_wrong_user
@pytest.mark.parametrize(
    "db_before,request_data,result_code,response_data,db_after",
    [
        [  # normal login
            lazy_fixture("one_user_db"),
            lazy_fixture("create_user_request"),
            200,
            lazy_fixture("create_user_response"),
            lazy_fixture("one_user_db"),
        ]
    ],
    ids=["normal login"],
)
async def test_login(
    db_before, request_data, result_code, response_data, db_after
):
    await base_test(
        "/login", db_before, request_data, result_code, response_data, db_after
    )


# change_name
# change_name_into_duplicate
# change_name_into_too_long_one
# change_password_into_too_long_one
# change_password
# change_password_with_wrong_passwod
# change_name_into_itself
# change_password_into_itself
def test_edit_user():
    pass


# get standart data
def test_get_user_data():
    pass
