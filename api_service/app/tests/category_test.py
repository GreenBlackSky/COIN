"""Accounts stuff tests."""
import pytest

from .utils import async_session, base_test, TestCase
from .conftest import (
    full_user_data,
    new_category_data,
    base_category_data,
    account_data,
    one_user_db,
    simple_user,
)
from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


def create_category_request():
    return {"account_id": 1, "name": "New category", "color": "12345678"}


def create_category_response():
    return ({"status": "OK", "category": new_category_data()}, 200)


def new_category_db():
    return {
        "users": [full_user_data()],
        "accounts": [account_data()],
        "categories": [base_category_data(), new_category_data()],
        "events": [],
    }


# create_category_with_name_too_long
# create_category_with_existent_name
# create_too_many_categories
# create category on non-existant account
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # create category
            one_user_db(),
            simple_user(),
            create_category_request(),
            create_category_response(),
            new_category_db(),
        )
    ],
    ids=["create category"],
)
async def test_create_category(case: TestCase):
    await base_test("/create_category", case)


def get_categories_request():
    return {"account_id": 1}


def get_categories_response():
    return (
        {
            "status": "OK",
            "categories": [base_category_data(), new_category_data()],
        },
        200,
    )


# get categories with wrong account
# with non existant account
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # get categories
            new_category_db(),
            simple_user(),
            get_categories_request(),
            get_categories_response(),
            new_category_db(),
        )
    ],
    ids=["get categories"],
)
async def test_get_categories(case: TestCase):
    await base_test("/get_categories", case)


def edited_category_data():
    return {
        "user_id": 1,
        "account_id": 1,
        "id": 1,
        "name": "Edited category",
        "color": "87654321",
    }


def edit_category_request():
    request = edited_category_data()
    del request["user_id"]
    request["category_id"] = request.pop("id")
    return request


def edit_category_response():
    return (
        {
            "status": "OK",
            "category": edited_category_data(),
        },
        200,
    )


def edited_category_db():
    return {
        "users": [full_user_data()],
        "accounts": [account_data()],
        "categories": [base_category_data(), edited_category_data()],
        "events": [],
    }


# edit_non_existant_category
# edit_into_duplicate_name
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # edit category
            new_category_db(),
            simple_user(),
            edit_category_request(),
            edit_category_response(),
            edited_category_db(),
        )
    ],
    ids=["edit category"],
)
async def test_edit_category(case: TestCase):
    await base_test("/edit_category", case)


def delete_category_request():
    return {"account_id": 1, "category_id": 1}


# delete_non_existant_category
# delete_only_category
@pytest.mark.parametrize(
    "case",
    [
        TestCase(  # delete category
            new_category_db(),
            simple_user(),
            delete_category_request(),
            create_category_response(),
            one_user_db(),
        )
    ],
    ids=["delete category"],
)
async def test_delete_category(case: TestCase):
    await base_test("/delete_category", case)
