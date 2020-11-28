from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from . import api

        app.register_blueprint(routes.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(api.bp)

        db.create_all()

    return app
