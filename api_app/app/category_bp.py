"""Module contains app web."""

import logging
from functools import wraps

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from . import rpc
from common.debug_tools import log_request


bp = Blueprint('category_bp', __name__)


@bp.route("/create_category", methods=['POST'])
@log_request
@jwt_required()
def create_category():
    """Create new category."""
    pass


@bp.route("/get_category", methods=['POST'])
@log_request
@jwt_required()
def get_category():
    """Get existing category by ID."""


@bp.route("/edit_category", methods=['POST'])
@log_request
@jwt_required()
def edit_category():
    """Edit category."""
    pass


@bp.route("/delete_category", methods=['POST'])
@log_request
@jwt_required()
def delete_category():
    """Get existing category by ID."""
    pass
