"""API app initialization module."""

import os
import logging

from flask import Flask
from flask_login import LoginManager
from flask_nameko import FlaskPooledClusterRpcProxy
from flask_cors import CORS


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

    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        FLASK_ENV=os.environ['FLASK_ENV'],
        FLASK_APP=os.environ['FLASK_APP'],
        FLASK_DEBUG=os.environ['FLASK_DEBUG'],
        NAMEKO_AMQP_URI="amqp://{}:{}@{}:{}".format(
            os.environ['RABBITMQ_DEFAULT_USER'],
            os.environ['RABBITMQ_DEFAULT_PASS'],
            os.environ['RABBITMQ_HOST'],
            os.environ['RABBITMQ_PORT'],
        ),
    )

    login_manager.init_app(app)
    rpc.init_app(app)
    CORS(app)

    with app.app_context():
        from . import api_bp
        from . import test_bp
        from . import login_bp
        app.register_blueprint(api_bp.bp)
        app.register_blueprint(test_bp.bp)
        app.register_blueprint(login_bp.bp)

    return app


app = create_app()
