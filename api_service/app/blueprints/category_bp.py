"""Flask blueprint, that contains events manipulation methods."""

from celery_abc import CallerMetaBase
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.celery_utils import celery_app
from common.debug_tools import log_request
from common.interfaces import CategoryService

from ..request_helpers import parse_request_args


class EventCategoryCaller(CategoryService, metaclass=CallerMetaBase):
    pass


bp = Blueprint("category_bp", __name__)
categoryService = EventCategoryCaller(celery_app)


@bp.post("/create_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def create_category(account_id, name, color):
    """Request to create new category."""
    return categoryService.create_category(
        current_user.id, account_id, name, color
    )


@bp.post("/get_categories")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def get_categories(account_id):
    """Get all categories user has."""
    return categoryService.get_categories(current_user.id, account_id)


@bp.post("/edit_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def edit_category(account_id, category_id, name, color):
    """Request to edit category."""
    return categoryService.edit_category(
        current_user.id, account_id, category_id, name, color
    )


@bp.post("/get_totals_by_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def get_totals_by_category(account_id, start_time, end_time):
    """Get totals on certain account by categories at certain time."""
    return categoryService.get_total_by_category(
        current_user.id, account_id, start_time, end_time
    )


@bp.post("/delete_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def delete_category(account_id, category_id, category_to):
    """Delete existing category."""
    return categoryService.delete_category(
        current_user.id, account_id, category_id, category_to
    )
