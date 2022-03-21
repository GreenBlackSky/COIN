"""Logging in and co tests."""
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


async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def clear_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# duplicate_register
# register_while_logged_in
# signup_with_too_long_name
# signup_with_too_long_password
async def test_register():
    await clear_db()
    await prepare_db()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/register",
            json={"name": "TestGuy", "password": "TestPass"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["user"]["name"] == "TestGuy"
        assert "id" in data["user"]
        user_id = data["user"]["id"]

        response = await ac.post(
            "/login", json={"name": "TestGuy", "password": "TestPass"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["user"]["name"] == "TestGuy"
        assert data["user"]["id"] == user_id


# wrong_password
# login_with_wrong_user
# change_name_into_too_long_one
# change_password_into_too_long_one
def test_login():
    pass


# change_name
# change_name_into_duplicate
# change_password
# change_password_with_wrong_passwod
# change_name_into_itself
# change_password_into_itself
def test_edit_user():
    pass
