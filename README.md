# COIN
Simple budget planner.

What's inside?
* frontend - flutter
* gateway - flask + gunicorn
* backend - nameko microservices + rabbitMQ
* db - postgresql
* cache - redis

All wrapped up in docker containers.

* dev deployment - docker-compose. Run `docker-compose build; docker-compose up` to deploy.
* production deployment - kubernetes

All config values must be stored in `config.env` in project root. It must have folowing values:
* RABBITMQ_USER
* RABBITMQ_PASSWORD
* RABBITMQ_HOST
* RABBITMQ_PORT
* SECRET_KEY
* FLASK_ENV
* FLASK_APP
* FLASK_DEBUG

TODOs
* marshmallow
* redis
* postgres
* core logic
* base container
* flutter
* production deployment
* split into submodules
