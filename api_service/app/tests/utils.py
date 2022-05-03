"""Some test utils."""

from contextlib import contextmanager

from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..main import app

from ..utils.models import Base, UserModel, AccountModel
from ..user import authorized_user


engine = create_async_engine(
    "sqlite+aiosqlite:///./test.db", connect_args={"check_same_thread": False}
)
db_models = {"users": UserModel, "accounts": AccountModel}
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


def compare_with_skip(dict_1: dict, dict_2: dict, skipped: set):
    keys_1 = set(dict_1.keys()) - skipped
    keys_2 = set(dict_2.keys()) - skipped
    if keys_1 != keys_2:
        return False

    for key in keys_1:
        val_1 = dict_1[key]
        val_2 = dict_2[key]
        if type(val_1) != type(val_2):
            return False

        if isinstance(val_1, dict):
            if not compare_with_skip(val_1, val_2, skipped):
                return False
        elif isinstance(val_1, list):
            if not all(
                compare_with_skip(elem_1, elem_2, skipped)
                for elem_1, elem_2 in zip(val_1, val_2)
            ):
                return False
        elif val_1 != val_2:
            return False

    return True


async def prepare_db(**values):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    to_add = [
        db_models[table_name](**object_data)
        for table_name, objects in values.items()
        for object_data in objects
    ]
    async with async_session() as session:
        async with session.begin():
            session.add_all(to_add)


async def get_db():
    result = {}
    async with async_session() as session:
        for table_name in db_models:
            rows = await session.execute(select(db_models[table_name]))
            result[table_name] = [
                entity.to_dict() for entity in rows.scalars()
            ]
    return result


@contextmanager
def set_current_user(app: FastAPI, user: UserModel | None):
    if user:
        app.dependency_overrides[authorized_user] = lambda: user
    try:
        yield app
    finally:
        app.dependency_overrides.pop(authorized_user, None)


async def base_test(
    path, db_before, request_data, result_code, response_data, db_after
):
    await prepare_db(**db_before)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(path, json=request_data)
    assert response.status_code == result_code, response.text
    data = response.json()
    assert compare_with_skip(data, response_data, {"access_token"})
    assert (await get_db()) == db_after
