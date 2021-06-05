"""Flask blueprint, that contains events manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from ..common import parse_request_args
from ..debug_tools import log_request


bp = Blueprint('label_bp', __name__)


@bp.post("/create_label")
@jwt_required()
@parse_request_args(request)
@log_request
def create_label():
    """Request to create new event."""
    pass


@bp.post("/get_labels")
@jwt_required()
@parse_request_args(request)
@log_request
def get_labels():
    """Get all labels user has."""
    pass


@bp.post("/edit_label")
@jwt_required()
@parse_request_args(request)
@log_request
def edit_label():
    """Request to edit event."""
    pass


@bp.post("/delete_label")
@jwt_required()
@parse_request_args(request)
@log_request
def delete_label():
    """Delete existing event."""
    pass
