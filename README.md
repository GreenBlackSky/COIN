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

`RABBITMQ_DEFAULT_USER RABBITMQ_DEFAULT_PASS RABBITMQ_HOST RABBITMQ_PORT`

`SECRET_KEY FLASK_ENV FLASK_APP FLASK_DEBUG`

`REDIS_PASSWORD REDIS_HOST REDIS_PORT REDIS_INDEX REDIS_REPLICATION_MODE`

`POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB POSTGRES_HOST POSTGRES_PORT`


TODO
* login
* wrap communication with json
* marshmallow schema
* create tables in db by models
* better tests
* base container
* flutter
* remove nameko_flask and nameko_redis
* redis password
* pg admin
* redis admin
* rabbit admin
* production deployment
* split into submodules
