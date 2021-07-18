"""Flask blueprint, that contains events manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from ..request_helpers import parse_request_args
from common.debug_tools import log_request


bp = Blueprint('label_bp', __name__)


@bp.post("/create_label")
@jwt_required()
@log_request(request, current_user)
def create_label():
    """Request to create new event."""
    pass


@bp.post("/get_labels")
@jwt_required()
@log_request(request, current_user)
def get_labels():
    """Get all labels user has."""
    pass


@bp.post("/edit_label")
@jwt_required()
@log_request(request, current_user)
def edit_label():
    """Request to edit event."""
    pass


@bp.post("/delete_label")
@jwt_required()
@log_request(request, current_user)
def delete_label():
    """Delete existing event."""
    pass
