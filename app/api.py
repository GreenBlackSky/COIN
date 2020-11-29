"""Core module contains logic of app."""

from datetime import date
from calendar import monthrange
from flask import Blueprint
from flask_login import login_required
from .models import db, User, Category, Event, Template


bp = Blueprint('api_bp', __name__)


# TODO connect to db
@bp.route("/get_user_data", methods=('POST',))
@login_required
def get_user_data():
    return {"method": "get_user_data"}


@bp.route("/get_events", methods=('POST',))
@login_required
def get_events():
    return {"method": "get_events"}


@bp.route("/get_month", methods=('POST',))
@login_required
def get_month():
    return {"method": "get_month"}


@bp.route("/get_year", methods=('POST',))
@login_required
def get_year():
    return {"method": "get_year"}


@bp.route("/get_all_years", methods=('POST',))
@login_required
def get_all_years():
    return {"method": "get_all_years"}


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
