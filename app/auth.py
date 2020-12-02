"""Authentification stuff."""

from datetime import datetime
import logging

from flask import Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from .models import db, User
from . import login_manager


bp = Blueprint('auth_bp', __name__, template_folder='templates')


@bp.route('/signup', methods=('POST',))
def signup():
    """Register new user."""
    name = request.args.get('name')
    password = request.args.get('password')
    if name is None or password is None:
        logging.warning(f"Incomplete sign up request - {request.args}")
        return

    existing_user = User.query.filter_by(name=name).first()
    if existing_user is not None:
        logging.warning(f"Register user that already exist - {name}")
        return

    user = User(
        name=name,
        created_on=datetime.now(),
        last_login=datetime.now()
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    logging.info(f"User {name} signed up and logged in")
    return {'signed up': name}


@bp.route("/login", methods=('POST',))
def login():
    """Log in user."""
    # TODO apply events templates
    # TODO load cache
    name = request.args.get('name')
    password = request.args.get('password')

    if current_user.is_authenticated:
        logging.warning(f"User {current_user.id} is already logged in.")
        return

    if name is None or password is None:
        logging.warning(f"Incomplete args in request - {request.args}")
        return

    user = User.query.filter_by(name=name).first()
    if user is None:
        logging.warning(f"Log in attempt but no such user exist {name}")
        return
    if not user.check_password(password=password):
        logging.info(f"Incorrect password by {name}")
        return

    login_user(user)
    user.last_login = datetime.now()
    db.session.add(user)
    db.session.commit()
    logging.info(f"User {name} logged in")
    return {"logged in": name}


@bp.route("/logout", methods=('POST',))
@login_required
def logout():
    """Log out user."""
    name = current_user.name
    logout_user()
    logging.info(f"User {name} logged out")


@login_manager.user_loader
def load_user(user_id):
    """Get current user (tech)."""
    if user_id is not None:
        return User.query.get(user_id)
    return


@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access."""
    logging.error("Unauthorized access attempt.")
