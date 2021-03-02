"""Module contains app web."""

import logging
from functools import wraps

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from . import rpc
from common.debug_tools import log_request


bp = Blueprint('template_bp', __name__)


@bp.route("/create_template", methods=['POST'])
@log_request
@jwt_required()
def create_template():
    """Create new template."""
    pass


@bp.route("/get_template", methods=['POST'])
@log_request
@jwt_required()
def get_template():
    """Get existing template by ID."""


@bp.route("/edit_template", methods=['POST'])
@log_request
@jwt_required()
def edit_template():
    """Edit template."""
    pass


@bp.route("/delete_template", methods=['POST'])
@log_request
@jwt_required()
def delete_template():
    """Get existing template by ID."""
    pass
