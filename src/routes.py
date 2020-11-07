from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required, logout_user
from flask import current_app as app


bp = Blueprint('main_bp', __name__, template_folder='templates')


@bp.route('/')
@login_required
def dashboard():
    return render_template(
        'dashboard.html',
        title='Flask-Login Tutorial.',
        current_user=current_user
    )


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
