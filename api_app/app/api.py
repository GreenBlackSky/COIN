"""Core module contains logic of app."""

import json
import logging

from flask import Blueprint, request
from flask_login import login_required, current_user

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


bp = Blueprint('api_bp', __name__)


class APIService:
    """API nameko service."""

    cache_rpc = RpcProxy("cache_service")

    @staticmethod
    def _dispatch_request(request, *keys):
        data = json.loads(request.get_data(as_text=True))
        for key in keys:
            yield data.get(key)

    @http('POST', '/set_test_value')
    def set_test_value(self, request):
        """Test integrety of system by creating new key value pair."""
        key, val = self._dispatch_request(request, 'key', 'val')
        self.cache_rpc.set_test_value(key, val)

    @http('POST', '/get_test_value')
    def get_test_value(self, request):
        """Test integrety of system by getting value by key."""
        key = self._dispatch_request(request, 'key')
        val = self.cache_rpc.get_test_value(key)
        return json.dumps({'val': val})


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
    """Get statistsics for month."""
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
    """Add new event."""
    return {"method": "add_event"}


@bp.route("/edit_event", methods=('POST',))
@login_required
def edit_event():
    """Edit event."""
    return {"method": "edit_event"}


@bp.route("/get_templates", methods=('POST',))
@login_required
def get_templates():
    """Get event templates."""
    return {"method": "get_templates"}


@bp.route("/add_template", methods=('POST',))
@login_required
def add_template():
    """Add new event template."""
    return {"method": "add_template"}


@bp.route("/edit_template", methods=('POST',))
@login_required
def edit_template():
    """Edit event template."""
    return {"method": "edit_template"}


@bp.route("/get_statistics", methods=('POST',))
@login_required
def get_statistics():
    """Get statistic data."""
    return {"method": "get_statistics"}
