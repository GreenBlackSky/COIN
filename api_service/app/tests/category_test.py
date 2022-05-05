"""Accounts stuff tests."""
import pytest
from pytest_lazyfixture import lazy_fixture


from .utils import async_session, base_test
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


# get_categories
def test_get_categories():
    pass


# edit_category
# edit_non_existant_category
# edit_into_duplicate_name
def test_edit_category():
    pass


# delete_category
# delete_non_existant_category
# delete_only_category
def test_delete_category():
    pass


# get_balance
# balance_with_no_events
# balance_after_events
# balance_between_events
# balance_before_events
# events_in_two_months
def test_get_totals_by_category():
    pass
