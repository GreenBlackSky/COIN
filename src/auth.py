from datetime import datetime
from flask import Blueprint
from flask_login import login_user, current_user, logout_user
from .models import db, User
from . import login_manager

bp = Blueprint('auth_bp', __name__, template_folder='templates')


@bp.route("/signup", methods=('POST',))
def register():
    existing_user = User.query.filter_by(name=form.name.data).first()
    if existing_user is not None:
        return

    user = User(
        name=form.name.data,
        created_on=datetime.now(),
        last_login=datetime.now()
    )
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()

    login_user(user)


@bp.route("/login", methods=('POST',))
def login():
    if current_user.is_authenticated:
        return

    user = User.query.filter_by(name=form.name.data).first()
    if user is None or not user.check_password(password=form.password.data):
        return

    login_user(user)
    user.last_login = datetime.now()
    db.session.add(user)
    db.session.commit()


@bp.route("/logout", methods=('POST',))
@login_required
def logout():
    logout_user()


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return


@login_manager.unauthorized_handler
def unauthorized():
    return
