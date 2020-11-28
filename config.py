class Config:
    _connection_data = {
        'type': 'postgresql+psycopg2',
        'user': 'user',
        'password': 'qwerty',
        'host': 'postgres',
        'port': '5432',
        'database': 'pgdb'
    }

    SECRET_KEY = 'dev'
    FLASK_ENV = 'development'
    FLASK_APP = 'auth'
    FLASK_DEBUG = 1

    SQLALCHEMY_DATABASE_URI = "{type}://{user}:{password}@{host}:{port}/{database}".format(**_connection_data)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
