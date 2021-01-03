"""Core module contains logic of app."""

import json
import logging

from flask import Blueprint, request
from flask_login import login_required, current_user

from . import rpc


bp = Blueprint('api_bp', __name__)


@bp.route("/easy_test", methods=['POST'])
def easy_test():
    logging.debug('easy_test')
    ret = {'val': 'easy'}
    return ret


@bp.route("/simple_test", methods=['POST'])
def simple_test():
    logging.debug('simple_test')
    val = rpc.cache_service.simple_test()
    ret = {'val': val}
    return ret


def _dispatch_request(request, *keys):
    logging.debug(f"_dispatch_request {request.args}")
    return [request.args.get(key) for key in keys]


@bp.route("/test_set_redis_value", methods=['POST'])
def test_set_redis_value():
    key, val = _dispatch_request(request, 'key', 'val')
    logging.debug(f'test_set_redis_value setting {key} : {val}')
    rpc.cache_service.test_set_value(key, val)
    logging.debug(f'test_set_redis_value set {key} : {val}')


@bp.route("/test_get_redis_value", methods=['POST'])
def test_get_redis_value():
    key = _dispatch_request(request, 'key')
    logging.debug(f'test_get_redis_value getting {key}')
    val = rpc.cache_service.test_get_value(key)
    logging.debug(f'test_get_redis_value got {key} : {val}')
    return {'val': val}


# @bp.route("/get_user_data", methods=['POST'])
# @login_required
# def get_user_data():
#     """Get user data."""
#     pass


# @bp.route("/get_unaccepted", methods=['POST'])
# @login_required
# def get_unaccepted():
#     """Get all events that are already happend, but were not accepted."""
#     pass


# @bp.route("/accept_event", methods=['POST'])
# @login_required
# def accept_event():
#     """Accept unaccepted event."""
#     pass


# @bp.route("/get_day", methods=['POST'])
# @login_required
# def get_day_events():
#     """Get events in one day."""
#     pass


# @bp.route("/get_month", methods=['POST'])
# @login_required
# def get_month():
#     """Get statistsics for month."""
#     pass


# @bp.route("/get_year", methods=['POST'])
# @login_required
# def get_year():
#     """Get statistics for year."""
#     pass


# @bp.route("/get_all_years", methods=['POST'])
# @login_required
# def get_all_years():
#     """Get info on all user history."""
#     pass


# @bp.route("/add_event", methods=['POST'])
# @login_required
# def add_event():
#     """Add new event."""
#     return {"method": "add_event"}


# @bp.route("/edit_event", methods=['POST'])
# @login_required
# def edit_event():
#     """Edit event."""
#     return {"method": "edit_event"}


# @bp.route("/get_templates", methods=['POST'])
# @login_required
# def get_templates():
#     """Get event templates."""
#     return {"method": "get_templates"}


# @bp.route("/add_template", methods=['POST'])
# @login_required
# def add_template():
#     """Add new event template."""
#     return {"method": "add_template"}


# @bp.route("/edit_template", methods=['POST'])
# @login_required
# def edit_template():
#     """Edit event template."""
#     return {"method": "edit_template"}


# @bp.route("/get_statistics", methods=['POST'])
# @login_required
# def get_statistics():
#     """Get statistic data."""
#     return {"method": "get_statistics"}
