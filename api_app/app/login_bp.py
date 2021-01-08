"""Flask blueprint, that handles user operations."""

from . import rpc, LoginManager

from flask import Blueprint, request
from flask_login import login_user, login_required, current_user, logout_user


bp = Blueprint('login_bp', __name__)


@bp.route("/register", methods=['POST'])
def register():
    """Register new user."""
    pass


@bp.route("/login", methods=['POST'])
def login():
    """Log in user."""
    pass


@login_required
@bp.route("/logout", methods=['POST'])
def logout():
    """Log out user."""
    logout_user()
    return {"logged": "out"}


@login_manager.user_loader
def load_user(user_id):
    """Load user handler."""
    pass


@login_manager.unauthorized_handler
def unauthorized():
    """Unauthorized access handler."""
    return {"user_id": None}
