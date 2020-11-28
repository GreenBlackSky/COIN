"""Core module contains logic of app."""

from datetime import date
from calendar import monthrange
from flask import Blueprint
from flask_login import login_required


bp = Blueprint('api_bp', __name__)


@bp.route("/get_user_data", methods=('POST',))
@login_required
def get_user_data():
    pass


@bp.route("/get_events", methods=('POST',))
@login_required
def get_events():
    pass


@bp.route("/get_month", methods=('POST',))
@login_required
def get_month():
    pass


@bp.route("/get_year", methods=('POST',))
@login_required
def get_year():
    pass


@bp.route("/get_all_years", methods=('POST',))
@login_required
def get_all_years():
    pass


@bp.route("/add_event", methods=('POST',))
@login_required
def add_event():
    pass


@bp.route("/edit_event", methods=('POST',))
@login_required
def edit_event():
    pass


@bp.route("/get_templates", methods=('POST',))
@login_required
def get_templates():
    pass


@bp.route("/add_template", methods=('POST',))
@login_required
def add_template():
    pass


@bp.route("/edit_template", methods=('POST',))
@login_required
def edit_template():
    pass


@bp.route("/get_statistics", methods=('POST',))
@login_required
def get_statistics():
    pass
