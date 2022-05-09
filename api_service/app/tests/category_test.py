"""Accounts stuff tests."""
import pytest
from pytest_lazyfixture import lazy_fixture

from .utils import async_session, base_test
from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


@pytest.fixture
def new_category_data():
    return {
        "user_id": 1,
        "account_id": 1,
        "id": 1,
        "name": "New category",
        "color": "12345678",
    }


@pytest.fixture
def create_category_request():
    return {"account_id": 1, "name": "New category", "color": "12345678"}


@pytest.fixture
def create_category_response(new_category_data):
    return {"status": "OK", "category": new_category_data}


@pytest.fixture
def new_category_db(
    full_user_data, account_data, base_category_data, new_category_data
):
    return {
        "users": [full_user_data],
        "accounts": [account_data],
        "categories": [base_category_data, new_category_data],
        "events": [],
    }


# create_category_with_name_too_long
# create_category_with_existent_name
# create_too_many_categories
# create category on non-existant account
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # create category
            lazy_fixture("one_user_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("create_category_request"),
            200,
            lazy_fixture("create_category_response"),
            lazy_fixture("new_category_db"),
        ]
    ],
    ids=["create category"],
)
async def test_create_category(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/create_category",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


@pytest.fixture
def get_categories_request():
    return {"account_id": 1}


@pytest.fixture
def get_categories_response(base_category_data, new_category_data):
    return {
        "status": "OK",
        "categories": [base_category_data, new_category_data],
    }


# get categories with wrong account
# with non existant account
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # get categories
            lazy_fixture("new_category_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("get_categories_request"),
            200,
            lazy_fixture("get_categories_response"),
            lazy_fixture("new_category_db"),
        ]
    ],
    ids=["get categories"],
)
async def test_get_categories(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/get_categories",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


@pytest.fixture
def edited_category_data():
    return {
        "user_id": 1,
        "account_id": 1,
        "id": 1,
        "name": "Edited category",
        "color": "87654321",
    }


@pytest.fixture
def edit_category_request(edited_category_data):
    request = dict(edited_category_data)
    del request["user_id"]
    request["category_id"] = request.pop("id")
    return request


@pytest.fixture
def edit_category_response(edited_category_data):
    return {
        "status": "OK",
        "category": edited_category_data,
    }


@pytest.fixture
def edited_category_db(
    full_user_data, account_data, base_category_data, edited_category_data
):
    return {
        "users": [full_user_data],
        "accounts": [account_data],
        "categories": [base_category_data, edited_category_data],
        "events": [],
    }


# edit_non_existant_category
# edit_into_duplicate_name
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # edit category
            lazy_fixture("new_category_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("edit_category_request"),
            200,
            lazy_fixture("edit_category_response"),
            lazy_fixture("edited_category_db"),
        ]
    ],
    ids=["edit category"],
)
async def test_edit_category(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/edit_category",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )


@pytest.fixture
def delete_category_request():
    return {"account_id": 1, "category_id": 1}


# delete_non_existant_category
# delete_only_category
@pytest.mark.parametrize(
    "db_before,user,request_data,response_code,response_data,db_after",
    [
        [  # delete category
            lazy_fixture("new_category_db"),
            lazy_fixture("simple_user"),
            lazy_fixture("delete_category_request"),
            200,
            lazy_fixture("create_category_response"),
            lazy_fixture("one_user_db"),
        ]
    ],
    ids=["delete category"],
)
async def test_delete_category(
    db_before, user, request_data, response_code, response_data, db_after
):
    await base_test(
        "/delete_category",
        db_before,
        user,
        request_data,
        response_code,
        response_data,
        db_after,
    )
