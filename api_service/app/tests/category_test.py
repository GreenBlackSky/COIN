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


# create_category
# create_category_with_name_too_long
# create_category_with_existent_name
# create_too_many_categories
def test_create_category():
    pass


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
