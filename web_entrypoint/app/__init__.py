"""COIN Web Entry Point initialization module."""


from flask import Flask
import logging


logging.basicConfig(
    filename='coin.log',
    format='%(asctime)s WEP %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG
)
logging.info('Started')


def create_app():
    """Create new WEP app."""
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app


app = create_app()
