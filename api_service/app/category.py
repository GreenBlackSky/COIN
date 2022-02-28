"""Flask blueprint, that contains events manipulation methods."""

import datetime as dt
from unicodedata import category
from fastapi import APIRouter, Depends
from pydantic import BaseModel


from .event import (
    delete_events_by_category,
    get_category_total,
    move_events_between_categories,
)
from .exceptions import LogicException
from .model import (
    UserModel,
    session,
    CategoryModel,
    CategorySchema,
    create_account_entry,
)
from .user import authorized_user


router = APIRouter()


class CreateCategoryRequest(BaseModel):
    account_id: int
    name: str
    color: str


@router.post("/create_category")
def create_category(
    request: CreateCategoryRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Request to create new category."""
    category = create_account_entry(
        CategoryModel,
        user_id=current_user.id,
        account_id=request.account_id,
        name=request.name,
        color=request.color,
    )
    session.add(category)
    session.commit()
    return {
        "status": "OK",
        "category": CategorySchema.from_orm(category).dict(),
    }


def get_categories(user_id, account_id):
    """Get all categories user has."""
    query = (
        session.query(CategoryModel)
        .filter(CategoryModel.user_id == user_id)
        .filter(CategoryModel.account_id == account_id)
    )
    return [
        CategorySchema.from_orm(category).dict() for category in query.all()
    ]


class GetCategoriesRequest(BaseModel):
    account_id: int


@router.post("/get_categories")
def get_categories_endpoint(
    request: GetCategoriesRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Get all categories user has endpoint."""
    return {
        "status": "OK",
        "categories": get_categories(current_user.id, request.account_id),
    }


class EditCategoryRequest(BaseModel):
    account_id: int
    category_id: int
    name: str
    color: str


@router.post("/edit_category")
def edit_category(
    request: EditCategoryRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Request to edit category."""
    category = session.query(CategoryModel).get(
        (current_user.id, request.account_id, request.category_id)
    )
    if category is None:
        raise LogicException("no such category")

    category.name = request.name
    category.color = request.color

    session.commit()
    return {
        "status": "OK",
        "category": CategorySchema.from_orm(category).dict(),
    }


class GetTotalsRequest(BaseModel):
    account_id: int
    start_time: int
    end_time: int


@router.post("/get_totals_by_category")
def get_totals_by_category(
    request: GetTotalsRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Get totals on certain account by categories at certain time."""
    start_time = dt.datetime.fromtimestamp(request.start_time)
    end_time = dt.datetime.fromtimestamp(request.end_time)

    categories = get_categories(current_user.id, request.account_id)

    totals = {
        category["id"]: get_category_total(
            request.account_id, category["id"], start_time, end_time
        )
        for category in categories
    }
    return {"status": "OK", "totals": totals}


class DeleteCategoryRequest(BaseModel):
    account_id: int
    category_id: int
    category_to: int


@router.post("/delete_category")
def delete_category(
    request: DeleteCategoryRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Delete existing category."""
    category = session.query(CategoryModel).get(
        (current_user.id, request.account_id, request.category_id)
    )
    if category is None:
        raise LogicException("no such category")

    session.delete(category)
    if request.category_to:
        if (
            session.query(CategoryModel).get(
                (current_user.id, request.account_id, request.category_to)
            )
            is None
        ):
            raise LogicException("No such category")
        move_events_between_categories(
            request.account_id, request.category_id, request.category_to
        )
    else:
        delete_events_by_category(
            current_user.id, request.account_id, request.category_id
        )

    session.commit()
    return {
        "status": "OK",
        "category": CategorySchema.from_orm(category).dict(),
    }
