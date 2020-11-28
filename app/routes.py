from flask import Blueprint
from flask import current_app as app


bp = Blueprint('main_bp', __name__, template_folder='templates')


@bp.route('/')
def dashboard():
    """Send REST client to user."""
    return {"HELLO": "SAM"}
