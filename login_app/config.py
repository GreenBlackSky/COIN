"""LogIn app configuration."""


class Config:
    """LogIn App configuration."""

    _db_connection_data = {
        'type': 'postgresql+psycopg2',
        'user': 'coin_app',
        'password': 'qwerty',
        'host': 'db',
        'port': '5432',
        'database': 'pgdb'
    }

    SQLALCHEMY_DATABASE_URI = "{type}://{user}:{password}@{host}:{port}/{database}".format(**_db_connection_data)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'dev'
    FLASK_ENV = 'development'
    FLASK_APP = 'auth'
    FLASK_DEBUG = 1
