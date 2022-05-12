"""Flask blueprint, that contains events manipulation methods."""

import datetime as dt

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .event import get_category_total
from .utils.exceptions import LogicException
from .utils.models import (
    UserModel,
    CategoryModel,
    EventModel,
    create_account_entry,
)
from .user import authorized_user
from .utils.database import get_session


router = APIRouter()


class CreateCategoryRequest(BaseModel):
    account_id: int
    name: str
    color: str


@router.post("/create_category")
async def create_category(
    request: CreateCategoryRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Request to create new category."""
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            category = await create_account_entry(
                session,
                CategoryModel,
                user_id=current_user.id,
                account_id=request.account_id,
                name=request.name,
                color=request.color,
            )
            session.add(category)
    return {
        "status": "OK",
        "category": category.to_dict(),
    }


async def get_categories(session: AsyncSession, user_id, account_id):
    """Get all categories user has."""
    query = await session.execute(
        select(CategoryModel)
        .where(CategoryModel.user_id == user_id)
        .where(CategoryModel.account_id == account_id)
    )
    return [category.to_dict() for (category,) in query.all()]


class GetCategoriesRequest(BaseModel):
    account_id: int


@router.post("/get_categories")
async def get_categories_endpoint(
    request: GetCategoriesRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Get all categories user has endpoint."""
    session: AsyncSession
    async with async_session() as session:
        return {
            "status": "OK",
            "categories": await get_categories(
                session, current_user.id, request.account_id
            ),
        }


class EditCategoryRequest(BaseModel):
    account_id: int
    category_id: int
    name: str
    color: str


@router.post("/edit_category")
async def edit_category(
    request: EditCategoryRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Request to edit category."""
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            category: CategoryModel = await session.get(
                CategoryModel,
                (current_user.id, request.account_id, request.category_id),
            )
            if category is None:
                raise LogicException("no such category")

            category.name = request.name
            category.color = request.color

    return {
        "status": "OK",
        "category": category.to_dict(),
    }


class GetTotalsRequest(BaseModel):
    account_id: int
    start_time: int
    end_time: int


@router.post("/get_totals_by_category")
async def get_totals_by_category(
    request: GetTotalsRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Get totals on certain account by categories at certain time."""
    start_time = dt.datetime.fromtimestamp(request.start_time)
    end_time = dt.datetime.fromtimestamp(request.end_time)

    session: AsyncSession
    async with async_session() as session:
        categories = await get_categories(
            session, current_user.id, request.account_id
        )

        totals = {
            category["id"]: await get_category_total(
                session,
                request.account_id,
                category["id"],
                start_time,
                end_time,
            )
            for category in categories
        }
    return {"status": "OK", "totals": totals}


async def delete_category(
    session: AsyncSession,
    user_id: int,
    account_id: int,
    category_id: int,
) -> CategoryModel:
    category: CategoryModel = await session.get(
        CategoryModel,
        (user_id, account_id, category_id),
    )
    if category is None:
        raise LogicException("no such category")

    await session.delete(category)

    await session.execute(
        delete(EventModel)
        .where(EventModel.user_id == user_id)
        .where(EventModel.account_id == account_id)
        .where(EventModel.category_id == category_id)
    )
    return category


class DeleteCategoryRequest(BaseModel):
    account_id: int
    category_id: int


@router.post("/delete_category")
async def delete_category_endpoint(
    request: DeleteCategoryRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Delete existing category."""
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            category = await delete_category(
                session,
                current_user.id,
                request.account_id,
                request.category_id,
            )

    return {
        "status": "OK",
        "category": category.to_dict(),
    }
