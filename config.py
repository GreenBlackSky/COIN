"""App configuration."""

import redis


class Config:
    """App configuration."""

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

    _redis_config = {
        'password': 'qwerty',
        'host_url': '172.28.1.4',
        'port': '6379'
    }

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url("redis://:{password}@{host_url}:{port}".format(**_redis_config))

    SECRET_KEY = 'dev'
    FLASK_ENV = 'development'
    FLASK_APP = 'auth'
    FLASK_DEBUG = 1
