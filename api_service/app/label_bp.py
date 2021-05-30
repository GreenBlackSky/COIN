"""Flask blueprint, that contains events manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import wrap_request

from . import rpc


bp = Blueprint('label_bp', __name__)


@bp.post("/create_label")
@jwt_required()
@wrap_request()
def create_label():
    """Request to create new event."""
    return rpc.label_service.create_label()


@bp.post("/get_labels")
@jwt_required()
@wrap_request()
def get_labels():
    """Get all labels user has."""
    return rpc.label_service.get_labels()


@bp.post("/edit_label")
@jwt_required()
@wrap_request()
def edit_label():
    """Request to edit event."""
    return rpc.label_service.edit_label()


@bp.post("/delete_label")
@jwt_required()
@wrap_request()
def delete_label():
    """Delete existing event."""
    return rpc.label_service.delete_label()
