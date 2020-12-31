"""API app configuration."""


class Config:
    """API app configuration."""

    SECRET_KEY = 'dev'
    FLASK_ENV = 'development'
    FLASK_APP = 'auth'
    FLASK_DEBUG = 1

    NAMEKO_AMQP_URI = 'amqp://localhost:5006'
