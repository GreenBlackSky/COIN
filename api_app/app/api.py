"""Core module contains logic of app."""

import logging
from flask import Blueprint, request
from flask_login import login_required, current_user


bp = Blueprint('api_bp', __name__)


@bp.route("/get_user_data", methods=('POST',))
@login_required
def get_user_data():
    """Get user data."""
    pass


@bp.route("/get_unaccepted", methods=('POST',))
@login_required
def get_unaccepted():
    """Get all events that are already happend, but were not accepted."""
    pass


@bp.route("/accept_event", methods=('POST',))
@login_required
def accept_event():
    """Accept unaccepted event."""
    pass


@bp.route("/get_day", methods=('POST',))
@login_required
def get_day_events():
    """Get events in one day."""
    pass


@bp.route("/get_month", methods=('POST',))
@login_required
def get_month():
    pass


@bp.route("/get_year", methods=('POST',))
@login_required
def get_year():
    """Get statistics for year."""
    pass


@bp.route("/get_all_years", methods=('POST',))
@login_required
def get_all_years():
    """Get info on all user history."""
    pass


@bp.route("/add_event", methods=('POST',))
@login_required
def add_event():
    return {"method": "add_event"}


@bp.route("/edit_event", methods=('POST',))
@login_required
def edit_event():
    return {"method": "edit_event"}


@bp.route("/get_templates", methods=('POST',))
@login_required
def get_templates():
    return {"method": "get_templates"}


@bp.route("/add_template", methods=('POST',))
@login_required
def add_template():
    return {"method": "add_template"}


@bp.route("/edit_template", methods=('POST',))
@login_required
def edit_template():
    return {"method": "edit_template"}


@bp.route("/get_statistics", methods=('POST',))
@login_required
def get_statistics():
    return {"method": "get_statistics"}
