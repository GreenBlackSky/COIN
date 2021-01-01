"""API app initialization module."""

import logging

from flask import Flask
from flask_login import LoginManager
from flask_nameko import FlaskPooledClusterRpcProxy


logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()]
)
logging.info('Started')


login_manager = LoginManager()
rpc = FlaskPooledClusterRpcProxy()


def create_app():
    """Create new flask app."""
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')
    login_manager.init_app(app)
    rpc.init_app(app)

    with app.app_context():
        from . import api
        app.register_blueprint(api.bp)

    return app


app = create_app()
