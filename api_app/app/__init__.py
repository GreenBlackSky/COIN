"""API app initialization module."""

import os
import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_nameko import FlaskPooledClusterRpcProxy
from flask_cors import CORS


logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()]
)
logging.info('Started')


jwt = JWTManager()
rpc = FlaskPooledClusterRpcProxy()


def create_app():
    """Create new flask app."""
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_mapping(
        JWT_SECRET_KEY=os.environ["JWT_SECRET_KEY"],
        SECRET_KEY=os.environ['SECRET_KEY'],
        FLASK_ENV=os.environ['FLASK_ENV'],
        FLASK_APP=os.environ['FLASK_APP'],
        FLASK_DEBUG=os.environ['FLASK_DEBUG'],
        CORS_HEADERS='Content-Type',
        NAMEKO_AMQP_URI="amqp://{}:{}@{}:{}".format(
            os.environ['RABBITMQ_DEFAULT_USER'],
            os.environ['RABBITMQ_DEFAULT_PASS'],
            os.environ['RABBITMQ_HOST'],
            os.environ['RABBITMQ_PORT'],
        ),
    )

    jwt.init_app(app)
    rpc.init_app(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    with app.app_context():
        from . import login_bp
        from . import account_bp
        from . import category_bp
        from . import event_bp
        from . import template_bp
        from . import test_bp
        app.register_blueprint(login_bp.bp)
        app.register_blueprint(account_bp.bp)
        app.register_blueprint(category_bp.bp)
        app.register_blueprint(event_bp.bp)
        app.register_blueprint(template_bp.bp)
        app.register_blueprint(test_bp.bp)

    return app


app = create_app()
