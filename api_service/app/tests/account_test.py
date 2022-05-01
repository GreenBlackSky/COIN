"""Accounts stuff tests."""

import pytest

from .utils import async_session, base_test
from ..utils.database import get_session
from ..main import app

app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


# create_account
# create_max_accounts
# create_new_account
# create_duplicate_account
# create_with_too_long_name
def test_create_account():
    pass


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
