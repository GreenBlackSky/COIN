"""Flask blueprint, that contains events manipulation methods."""

import datetime as dt

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user


from .account_bp import check_account
from .event_bp import (
    delete_events_by_category,
    get_category_total,
    move_events_between_categories,
)
from .debug_tools import log_request
from .model import session, CategoryModel
from .request_helpers import parse_request_args
from .schemas import CategorySchema


bp = Blueprint("category_bp", __name__)
category_schema = CategorySchema()


@bp.post("/create_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def create_category(account_id, name, color):
    """Request to create new category."""
    category = CategoryModel(
        user_id=current_user.id, account_id=account_id, name=name, color=color
    )
    session.add(category)
    session.commit()
    return {"status": "OK", "category": category_schema.dump(category)}


def get_categories(user_id, account_id):
    """Get all categories user has."""
    query = (
        session.query(CategoryModel)
        .filter(CategoryModel.user_id == user_id)
        .filter(CategoryModel.account_id == account_id)
    )
    return [category_schema.dump(category) for category in query.all()]


@bp.post("/get_categories")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def get_categories_endpoint(account_id):
    """Get all categories user has endpoint."""
    return {
        "status": "OK",
        "categories": [
            category_schema.dump(category)
            for category in get_categories(account_id, current_user.id)
        ],
    }


@bp.post("/edit_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def edit_category(account_id, category_id, name, color):
    """Request to edit category."""
    category = session.get(CategoryModel, category_id)
    if category is None:
        return {"status": "no such category"}
    if category.user_id != current_user.id:
        return {"status": "accessing another users events"}
    if category.account_id != account_id:
        return {"status": "wrong account for category"}

    category.name = name
    category.color = color

    session.commit()
    return {"status": "OK", "category": category_schema.dump(category)}


@bp.post("/get_totals_by_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def get_totals_by_category(account_id, start_time, end_time):
    """Get totals on certain account by categories at certain time."""
    start_time = dt.datetime.fromtimestamp(start_time)
    end_time = dt.datetime.fromtimestamp(end_time)

    categories = get_categories(current_user.id, account_id)

    totals = {
        category["id"]: get_category_total(
            account_id, category["id"], start_time, end_time
        )
        for category in categories
    }
    return {"status": "OK", "totals": totals}


@bp.post("/delete_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def delete_category(account_id, category_id, category_to):
    """Delete existing category."""
    category = session.get(CategoryModel, category_id)
    if category is None:
        return {"status": "no such category"}
    if category.user_id != current_user.id:
        return {"status": "accessing another users events"}
    if category.account_id != account_id:
        return {"status": "wrong account for category"}

    session.delete(category)
    if category_to:
        move_events_between_categories(account_id, category_id, category_to)
    else:
        delete_events_by_category(account_id, category_id)

    session.commit()
    return {"status": "OK", "category": category_schema.dump(category)}
