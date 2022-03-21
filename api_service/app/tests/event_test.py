"""Events stuff tests."""

import pytest

from httpx import AsyncClient
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..models import Base
from ..database import get_session
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


# create_event
# balance_changes_on_create
# events_at_months_start
# add_event_at_previous_month
# create_event_with_duplicate_description
# create_event_with_too_long_description
def test_create_event():
    pass


# get_all_events
# filter_events_after
# filter_events_before
# events_with_year_between
def test_get_events():
    pass


# edit_event
# balance_changes_on_edit
# edit_non_existent_event
# edit_event_with_duplicate_description
# edit_event_with_too_long_description
def test_edit_event():
    pass


# delete_event
# balance_changes_on_delete
# delete_non_existant_event
def test_delete_event():
    pass


# get_balance
# balance_with_no_events
# balance_after_events
# balance_between_events
# balance_before_events
# events_in_two_months
def test_get_balance():
    pass
