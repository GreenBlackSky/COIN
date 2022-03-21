"""Accounts stuff tests."""

import pytest

from httpx import AsyncClient
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..utils.models import Base
from ..utils.database import get_session
from ..main import app

engine = create_async_engine(
    "sqlite+aiosqlite:///./test.db", connect_args={"check_same_thread": False}
)
app.dependency_overrides[get_session] = lambda: sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
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
